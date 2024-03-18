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

import asyncio
from unittest.mock import AsyncMock, MagicMock

import pytest
from bumble.link import LocalLink

# Easy to use as if it is a fake transport.
from bumble.transport.pty import open_pty_transport

from bluet.process import BumbledProcess


@pytest.mark.asyncio
async def test_not_crash(fake_process):
    transport_fut = open_pty_transport("")

    fake_process.register(["fake-command"])
    process_fut = asyncio.create_subprocess_exec("fake-command")

    bumbled_process = BumbledProcess("test-name", link=LocalLink(), transport=transport_fut, process=process_fut)
    async with bumbled_process:
        pass


@pytest.mark.asyncio
async def test_transport_closed_if_process_creation_failed():
    transport = await open_pty_transport("")
    mock_close = AsyncMock(side_effect=transport.close)
    transport.close = mock_close

    transport_fut = asyncio.Future()
    transport_fut.set_result(transport)

    async def create_process() -> asyncio.subprocess.Process:
        msg = "TestError345"
        raise RuntimeError(msg)

    bumbled_process = BumbledProcess("test-name", link=LocalLink(), transport=transport_fut, process=create_process())
    with pytest.raises(RuntimeError) as exc:
        await bumbled_process.init()
    assert str(exc.value) == "TestError345", f"Actually: {exc.value!s}"
    mock_close.assert_awaited_once()


@pytest.mark.asyncio
async def test_process_terminated(fake_process):
    transport_fut = open_pty_transport("")

    fake_process.register(["fake-command"])
    process = await asyncio.create_subprocess_exec("fake-command")
    mock_terminate = MagicMock(side_effect=process.terminate)
    process.terminate = mock_terminate

    process_fut = asyncio.Future()
    process_fut.set_result(process)

    bumbled_process = BumbledProcess("test-name", link=LocalLink(), transport=transport_fut, process=process_fut)
    async with bumbled_process:
        pass
    mock_terminate.assert_called_once()
