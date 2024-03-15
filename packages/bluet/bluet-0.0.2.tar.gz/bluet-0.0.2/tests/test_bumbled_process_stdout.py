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


import asyncio.subprocess
from textwrap import dedent

import pytest
from bumble.link import LocalLink

# Easy to use as if it is a fake transport.
from bumble.transport.pty import open_pty_transport

from bluet.process import BumbledProcess


@pytest.mark.asyncio
async def test_smoke(fake_process):
    transport_fut = open_pty_transport("")
    out = """\
    line 1
    line 2
    line 3
    """
    fake_process.register(["test-command"], stdout=dedent(out).encode("utf-8"))
    process_fut = asyncio.create_subprocess_exec("test-command", stdout=asyncio.subprocess.PIPE)
    async with BumbledProcess("test-name", link=LocalLink(), transport=transport_fut, process=process_fut) as bp:
        bp.start_monitoring_stdout()
        for _i in range(10):
            await asyncio.sleep(0)


@pytest.mark.asyncio
async def test_read_lines(fake_process):
    transport_fut = open_pty_transport("")
    out = """\
    line 1
    line 2
    line 3
    """
    fake_process.register(["test-command"], stdout=dedent(out).encode("utf-8"))
    process_fut = asyncio.create_subprocess_exec("test-command", stdout=asyncio.subprocess.PIPE)

    lines_processed = []

    def process_line(line):
        lines_processed.append(f"<{line.rstrip()}>")

    async with BumbledProcess("test-name", link=LocalLink(), transport=transport_fut, process=process_fut) as bp:
        bp.start_monitoring_stdout(process_line)
        for _i in range(10):
            await asyncio.sleep(0)
    assert lines_processed == ["<line 1>", "<line 2>", "<line 3>"]
