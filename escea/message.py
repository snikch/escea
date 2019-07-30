import binascii
import struct

from escea.error import (CRCInvalid, InvalidTemp, UnexpectedResponse)

START_BYTE = 0x47
END_BYTE = 0x46
STATUS_PLEASE = 0x31
POWER_ON = 0x39
POWER_OFF = 0x3A
SEARCH_FOR_FIRES = 0x50
FAN_BOOST_ON = 0x37
FAN_BOOST_OFF = 0x38
FLAME_EFFECT_ON = 0x56
FLAME_EFFECT_OFF = 0x55
NEW_SET_TEMP = 0x57
STATUS = 0x80
POWER_ON_ACK = 0x8D
POWER_OFF_ACK = 0x8F
FAN_BOOST_ON_ACK = 0x89
FAN_BOOST_OFF_ACK = 0x8B
FLAME_EFFECT_ON_ACK = 0x61
FLAME_EFFECT_OFF_ACK = 0x60
NEW_SET_TEMP_ACK = 0x66
I_AM_A_FIRE = 0x90

MIN_TEMP = 3
MAX_TEMP = 31


class Message(object):
    def __init__(self):
        super(Message, self).__init__()
        self._parts = bytearray(15)
        self._expected_code = ''

    def set(self, index, value):
        self._parts[index] = value

    def get(self, index):
        return self._parts[index]

    def __str__(self):
        return self._parts.hex()

    def payload(self):
        self._parts[13] = self.crc()
        return self._parts

    def crc(self):
        return sum(self._parts[1:12]) % 256

    def assert_code(self, code):
        if code != self._expected_code:
            raise UnexpectedResponse(
                "Received unexpected code {} (expected {})".format(
                    code, self._expected_code))


class RequestMessage(Message):
    def __init__(self):
        super(RequestMessage, self).__init__()
        self.set(0, START_BYTE)
        self.set(14, END_BYTE)

    def command(self, value):
        self._parts[1] = value

    def expect_code(self, value):
        self._expected_code = value


class SearchForFiresRequest(RequestMessage):
    def __init__(self):
        super(SearchForFiresRequest, self).__init__()
        self.command(SEARCH_FOR_FIRES)
        self.expect_code(I_AM_A_FIRE)


class StatusRequest(RequestMessage):
    def __init__(self):
        super(StatusRequest, self).__init__()
        self.command(STATUS_PLEASE)
        self.expect_code(STATUS)


class SetTempRequest(RequestMessage):
    def __init__(self, temp):
        super(SetTempRequest, self).__init__()
        if temp < MIN_TEMP or temp > MAX_TEMP:
            raise InvalidTemp(temp, MIN_TEMP, MAX_TEMP)

        self.command(NEW_SET_TEMP)
        self.expect_code(NEW_SET_TEMP_ACK)
        self.set(2, 0x01)
        self.set(3, temp.to_bytes(1, byteorder='big', signed=True)[0])


class PowerOnRequest(RequestMessage):
    def __init__(self):
        super(PowerOnRequest, self).__init__()
        self.command(POWER_ON)
        self.expect_code(POWER_ON_ACK)


class PowerOffRequest(RequestMessage):
    def __init__(self):
        super(PowerOffRequest, self).__init__()
        self.command(POWER_OFF)
        self.expect_code(POWER_OFF_ACK)


class FanBoostOnRequest(RequestMessage):
    def __init__(self):
        super(FanBoostOnRequest, self).__init__()
        self.command(FAN_BOOST_ON)
        self.expect_code(FAN_BOOST_ON_ACK)


class FanBoostOffRequest(RequestMessage):
    def __init__(self):
        super(FanBoostOffRequest, self).__init__()
        self.command(FAN_BOOST_OFF)
        self.expect_code(FAN_BOOST_OFF_ACK)


class FlameEffectOnRequest(RequestMessage):
    def __init__(self):
        super(FlameEffectOnRequest, self).__init__()
        self.command(FLAME_EFFECT_ON)
        self.expect_code(FLAME_EFFECT_ON_ACK)


class FlameEffectOffRequest(RequestMessage):
    def __init__(self):
        super(FlameEffectOffRequest, self).__init__()
        self.command(FLAME_EFFECT_OFF)
        self.expect_code(FLAME_EFFECT_OFF_ACK)


class StatusResponse(Message):
    BOOL = {0: False, 1: True}

    def __init__(self, message):
        super(StatusResponse, self).__init__()
        self._parts = message._parts
        self.state = {
            "target_temp": message.get(7),
            "current_temp": message.get(8),
            "on": self.bool(message.get(4)),
            "fan_boost": self.bool(message.get(5)),
            "flame_effect": self.bool(message.get(6)),
        }

    def bool(self, value):
        return StatusResponse.BOOL[value]


class Response(Message):
    def __init__(self, data):
        super(Response, self).__init__()
        self._parts = data
        if self.crc() != self._parts[13]:
            raise CRCInvalid("Invalid CRC {} for data {}".format(
                self.crc(), self._parts))

    def serial(self):
        # unsigned long
        return struct.unpack('>L', self._parts[3:7])[0]

    def pin(self):
        # unsigned short
        return struct.unpack('>H', self._parts[7:9])[0]
