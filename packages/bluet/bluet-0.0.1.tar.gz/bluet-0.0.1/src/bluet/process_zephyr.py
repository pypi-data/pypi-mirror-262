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

import asyncio.subprocess
import errno
import os.path
import sys
from typing import TYPE_CHECKING

from bumble.transport.tcp_server import open_tcp_server_transport

from bluet.process import BumbledProcess

if TYPE_CHECKING:
    from typing import Awaitable

    from bumble.link import LocalLink
    from bumble.transport.common import Transport


def _open_transport(*arg) -> Awaitable[Transport]:
    return open_tcp_server_transport(*arg)


def create_bumbled_process_for_zephyr(
    controller_name: str,
    link: LocalLink,
    port: int,
    zephyr_program: str | None = None,
    extra_program_args: list[str] | None = None,
) -> BumbledProcess:
    """Creates a BumbledProcess with a zephyr executable.

    This `zephyr` executable is assumed to be built with `native_sim`, which
    compiles in the whole bluetooth software stack EXCLUDING the controller.
    It has a flag '--bt-dev=...' to designate either a TCP server or a USB
    device. This function will make a bumble controller on the TCP server end,
    and let the zephyr binary act as the TCP client.

    If argument `zephyr_program` is not explicitly given, one will be searched
    for, assuming the pytest command is initiated by `west twister`.

    TODO: remove explicit `port` and use the `socket` library to open a socket
    with an arbitrary unused port. Pending on
        https://github.com/google/bumble/pull/435
    """
    if zephyr_program is None:
        zephyr_program = find_zephyr_binary_from_env()
    transport = _open_transport(f"_:{port}")
    process = asyncio.create_subprocess_exec(
        zephyr_program,
        f"--bt-dev=127.0.0.1:{port}",
        *(extra_program_args or []),
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
    )
    return BumbledProcess(controller_name, link, transport, process)


def find_zephyr_binary_from_env() -> str:
    """Finds the zephyr executable binary.

    The command line arguments is assumed to set by `west twister`.
    """
    build_dir_arg_prefix = "--build-dir"

    def find_build_dir(args) -> str:
        for i, arg in enumerate(args):
            if arg.startswith(build_dir_arg_prefix):
                value = arg[len(build_dir_arg_prefix) :]
                if not value:
                    return args[i + 1]
                if value[0] == "=":
                    return value[1:]
        msg = f"Cannot find flag: {build_dir_arg_prefix}"
        raise RuntimeError(msg)

    bin_path = os.path.join(find_build_dir(sys.argv), "zephyr", "zephyr.exe")
    if not os.path.exists(bin_path):
        raise FileNotFoundError(errno.ENOENT, "Cannot find zephyr binary.", bin_path)
    return bin_path
