from micropython import const
from adafruit_bus_device.spi_device import SPIDevice

# _________________________________________________________________
# |                         Command Byte                          |
# |---------------------------------------------------------------|
# |     0 |     1 |     0 |     0 |     0 |    A1 |    A0 |   R/W |
# |---------------------------------------------------------------|
# |                         Address Byte                          |
# |---------------------------------------------------------------|
# |   A07 |   A06 |   A05 |   A04 |   A03 |   A02 |   A01 |   A00 |
# |---------------------------------------------------------------|
# |                           Data Bits                           |
# |---------------------------------------------------------------|
# |   D07 |   D06 |   D05 |   D04 |   D03 |   D02 |   D01 |   D00 |
# -----------------------------------------------------------------

# MCP23S08 - 8-channel GPIO
# MCP23S17 - 16-channel GPIO

_MCP23S08_IODIR = const(0x00)
_MCP23S08_IPOL = const(0x01)
_MCP23S08_GPINTEN = const(0x02)
_MCP23S08_DEFVAL = const(0x03)
_MCP23S08_INTCON = const(0x04)
_MCP23S08_IOCON = const(0x04)
_MCP23S08_GPPU = const(0x06)
_MCP23S08_INTF = const(0x07)
_MCP23S08_INTCAP = const(0x08)
_MCP23S08_GPIO = const(0x09)
_MCP23S08_OLAT = const(0x0A)

_MCP23S08_START_BYTE = const(0x40)
_MCP23S08_ADDR_MASK = const(0x06)

_MCP23S08_MAX_SCLK = const(10000000)

class MCP23S08:
    command_buf = bytearray(1)
    dir_buf = bytearray(1)
    input_buf = bytearray(1)
    output_buf = bytearray(1)

    def __init__(self, spi, cs, addr=0x00):
        self.spi_device = SPIDevice(spi, cs, baudrate=_MCP23S08_MAX_SCLK, polarity=0, phase=0)
        self.device_addr = addr

    def setDirection(self, channel, dir):
        buffer = bytearray(3)
        buffer[0] = _MCP23S08_START_BYTE | (_MCP23S08_ADDR_MASK & self.device_addr) & 0xFE
        buffer[1] = _MCP23S08_IODIR
        if dir == 0:
            self.dir_buf = self.dir_buf & (~(0x01 << channel))
        else:
            self.dir_buf = self.dir_buf | (0x01 << channel)
        buffer[2] = self.dir_buf
        with self.spi_device as spi:
            spi.write(buffer)

    def digitalOut(self, channel, val):
        buffer = bytearray(3)
        buffer[0] = _MCP23S08_START_BYTE | (_MCP23S08_ADDR_MASK & self.device_addr) & 0xFE
        buffer[1] = _MCP23S08_GPIO
        if val == 0:
            self.output_buf = self.output_buf & (~(0x01 << channel))
        else:
            self.output_buf = self.output_buf | (0x01 << channel)
        buffer[2] = self.output_buf
        with self.spi_device as spi:
            spi.write(buffer)

