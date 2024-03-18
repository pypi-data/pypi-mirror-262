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

import pytest
import pytest_asyncio
from bumble.device import Device, DeviceConfiguration
from bumble.link import LocalLink

from bluet.central import scan_and_connect
from bluet.peripheral import advertise_until_connected
from bluet.tester_device import create_tester_device


@pytest.fixture
def link():
    return LocalLink()


@pytest_asyncio.fixture
async def peripheral_device(link) -> Device:
    config = DeviceConfiguration()
    config.load_from_dict(
        {
            "name": "peripheral_device",
            "advertising_interval": 10,  # ms
        }
    )
    device = create_tester_device("peripheral_device", link=link, device_config=config)
    await device.power_on()
    return device


@pytest_asyncio.fixture
async def central_device(link) -> Device:
    device = create_tester_device("central_device", link=link)
    await device.power_on()
    return device


@pytest.mark.asyncio
async def test_advertise_until_connected_no_reply(peripheral_device):
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(advertise_until_connected(peripheral_device), timeout=1.0)


@pytest.mark.asyncio
async def test_advertise_until_connected_normal(peripheral_device, central_device):
    conn1, (conn2, _) = await asyncio.gather(
        advertise_until_connected(peripheral_device), scan_and_connect(central_device)
    )
    assert conn1.self_address == peripheral_device.random_address
    assert conn1.peer_address == central_device.random_address
    assert conn2.self_address == central_device.random_address
    assert conn2.peer_address == peripheral_device.random_address
