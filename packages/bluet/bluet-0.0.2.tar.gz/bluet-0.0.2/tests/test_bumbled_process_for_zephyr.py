# Copyright 2024 Cheng Sheng
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
from unittest.mock import patch

import pytest
from bumble.link import LocalLink

# Easy to use as if it is a fake transport.
from bumble.transport.pty import open_pty_transport

from bluet.process_zephyr import (
    create_bumbled_process_for_zephyr,
    find_zephyr_binary_from_env,
)


def test_find_zephyr_binary_build_dir1():
    with (
        patch.object(sys, "argv", ["cmd", "--build-dir", "/abc/def"]),
        patch("os.path.exists", return_value=True) as mock_exists,
    ):
        mock_exists.return_value = True
        value = find_zephyr_binary_from_env()
    assert value == "/abc/def/zephyr/zephyr.exe", f"Actually: {value}"
    mock_exists.assert_called_once_with(value)


def test_find_zephyr_binary_build_dir2():
    with (
        patch.object(sys, "argv", ["cmd", "--build-dir=/abc/def"]),
        patch("os.path.exists", return_value=True) as mock_exists,
    ):
        value = find_zephyr_binary_from_env()
    assert value == "/abc/def/zephyr/zephyr.exe", f"Actually: {value}"
    mock_exists.assert_called_once_with(value)


def test_find_zephyr_binary_no_binary():
    with (
        patch.object(sys, "argv", ["cmd", "--build-dir=/abc/def"]),
        patch("os.path.exists", return_value=False) as mock_exists,
        pytest.raises(FileNotFoundError) as exc,
    ):
        find_zephyr_binary_from_env()
    assert "/abc/def/zephyr/zephyr.exe" in str(exc.value), f"Actually: {exc.value!s}"
    mock_exists.assert_called_once_with("/abc/def/zephyr/zephyr.exe")


def test_find_zephyr_binary_no_build_dir():
    with patch.object(sys, "argv", ["cmd"]), pytest.raises(RuntimeError) as exc:
        find_zephyr_binary_from_env()
    assert "Cannot find flag" in str(exc.value), f"Actually: {exc.value!s}"


def _patch_open_transport():
    return patch("bluet.process_zephyr._open_transport", side_effect=lambda _: open_pty_transport(""))


@pytest.mark.asyncio
async def test_create_bumbled_process_for_zephyr_normal(fake_process):
    fake_process.register([fake_process.any()])
    with _patch_open_transport() as mock_open:
        process = create_bumbled_process_for_zephyr(
            "test-name", link=LocalLink(), port=12345, zephyr_program="fake-command"
        )
    mock_open.assert_called_once_with("_:12345")
    async with process:
        pass
    assert ["fake-command", "--bt-dev=127.0.0.1:12345"] in fake_process.calls, f"Actually: {fake_process.calls!s}"


@pytest.mark.asyncio
async def test_create_bumbled_process_for_zephyr_extra_args(fake_process):
    fake_process.register([fake_process.any()])
    with _patch_open_transport():
        process = create_bumbled_process_for_zephyr(
            "test-name",
            link=LocalLink(),
            port=12345,
            zephyr_program="fake-command",
            extra_program_args=["arg3", "arg2", "arg1"],
        )
    async with process:
        pass
    assert [
        "fake-command",
        "--bt-dev=127.0.0.1:12345",
        "arg3",
        "arg2",
        "arg1",
    ] in fake_process.calls, f"Actually: {fake_process.calls!s}"


@pytest.mark.asyncio
async def test_create_bumbled_process_for_zephyr_with_default_zephyr(fake_process):
    fake_process.register([fake_process.any()])
    with (
        _patch_open_transport(),
        patch("bluet.process_zephyr.find_zephyr_binary_from_env", return_value="foobar-command") as mock_find,
    ):
        process = create_bumbled_process_for_zephyr("test-name", link=LocalLink(), port=12345)
    async with process:
        pass
    mock_find.assert_called_once()
    assert len(fake_process.calls) == 1, f"Actual: {len(fake_process.calls)}"
    assert fake_process.calls[0][0] == "foobar-command", "Actual: fake_process.calls[0][0]"
