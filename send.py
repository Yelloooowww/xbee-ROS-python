# Copyright 2017, Digi International Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from digi.xbee.devices import XBeeDevice
from digi.xbee.util import utils
from digi.xbee.models.address import XBee64BitAddress
from digi.xbee.models.status import PowerLevel
from digi.xbee.models.status import NetworkDiscoveryStatus
from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice

# TODO: Replace with the serial port where your local module is connected to.
PORT = "/dev/ttyUSB0"
# TODO: Replace with the baud rate of your local module.
BAUD_RATE = 9600

PARAM_VALUE_PAN_ID = bytearray(b'\x01\x23')
PARAM_DESTINATION_ADDR = XBee64BitAddress.BROADCAST_ADDRESS
PARAM_POWER_LEVEL = PowerLevel.LEVEL_HIGH


def main():
    device = XBeeDevice(PORT, BAUD_RATE)

    try:
        device.open(force_settings=True)
        remote = RemoteXBeeDevice(
            device,
            x64bit_addr=XBee64BitAddress.from_hex_string("0013A20041AF1A91"),
            node_id="manually_added")
        device.send_data(remote, "Hello XBee!")

    finally:
        if device is not None and device.is_open():
            device.close()


if __name__ == '__main__':
    main()
