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

from __future__ import annotations

from typing import TYPE_CHECKING

from bumble.controller import Controller

if TYPE_CHECKING:
    from asyncio.subprocess import Process
    from typing import Awaitable

    from bumble.link import LocalLink
    from bumble.transport import Transport


class BumbledProcess:
    """A virtual device that contains the application/program under test.

    Thid device puts the application/program under test in a python asyncio
    Process as the bluetooth host, and creates a bumble bluetooth controller
    and connects them with a transport method that bumble supports (like TCP,
    fifos, etc.).

    Generally, users should use some helper function to create this object.

    It is recommended to use `async with` on the object to ensure predictable
    object cleanup, though alternatively using `init()` to start and `close()`
    to clean-up is also valid. Some bad things might happen if `init()` is
    called but `close()` isn't.
    """

    _initializer: Awaitable[None]
    _closed: bool

    transport: Transport | None
    controller: Controller | None
    process: Process | None

    def __init__(self, name: str, link: LocalLink, transport: Awaitable[Transport], process: Awaitable[Process]):
        async def init():
            try:
                self.transport = await transport
                self.controller = Controller(
                    name, link=link, host_source=self.transport.source, host_sink=self.transport.sink
                )
                self.process = await process
            except:
                await self.close()
                raise

        self._initializer = init()
        self._closed = False
        self.transport = None
        self.controller = None
        self.process = None

    async def __aenter__(self):
        await self.init()
        return self

    async def __aexit__(self, *args):
        await self.close()

    async def init(self):
        initializer, self._initializer = self._initializer, None
        if initializer:
            await initializer

    async def close(self):
        if self.process:
            self.process.terminate()
            await self.process.wait()
            self.process = None
        if self.controller:
            self.controller = None
        if self.transport:
            await self.transport.close()
            self.transport = None
