import socket
import binascii

from escea.message import (
    FanBoostOffRequest,
    FanBoostOnRequest,
    FlameEffectOffRequest,
    FlameEffectOnRequest,
    PowerOffRequest,
    PowerOnRequest,
    Response,
    SearchForFiresRequest,
    SetTempRequest,
    StatusRequest,
    StatusResponse,
)

from escea.error import (ConnectionTimeout, UnexpectedResponse)


def fires(timeout=1):
    # Create a socket to send/recv on
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(('0.0.0.0', Fire.UDP_PORT))
    fires = []
    try:
        message = SearchForFiresRequest()
        sock.sendto(message.payload(), ('<broadcast>', Fire.UDP_PORT))
        # Each recv should have the full timeout period to complete
        sock.settimeout(timeout)
        while True:
            # Get some packets from the network
            data, (address, _) = sock.recvfrom(1024)
            response = Response(data)
            # Confirm it's an I_AM_A_FIRE response
            try:
                message.assert_code(response.get(1))
                fires.append(Fire(address, response.serial(), response.pin()))
            except UnexpectedResponse:
                pass
    except socket.timeout:
        # This will always happen, a timeout occurs when we no longer hear from any fires
        # This is the required flow to break out of the `while True:` statement above.
        pass
    finally:
        # Always close the socket
        sock.close()

    return fires


class Fire(object):
    UDP_PORT = 3300

    def __init__(self, ip, serial='', pin=''):
        super(Fire, self).__init__()
        self._ip = ip
        self._serial = serial
        self._pin = pin

    def send(self, message):
        # Create a socket to send/recv on
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0', Fire.UDP_PORT))
        data = ''
        try:
            # All socket calls within a try block
            sock.sendto(message.payload(), (self._ip, Fire.UDP_PORT))
            sock.settimeout(2)
            data, _ = sock.recvfrom(1024)
        except socket.timeout:
            raise ConnectionTimeout
        finally:
            # Always close the socket
            sock.close()

        response = Response(data)
        message.assert_code(response.get(1))
        return response

    def status(self):
        return StatusResponse(self.send(StatusRequest()))

    def set_temp(self, target):
        self.send(SetTempRequest(target))

    def power_on(self):
        self.send(PowerOnRequest())

    def power_off(self):
        self.send(PowerOffRequest())

    def flame_effect_on(self):
        self.send(FlameEffectOnRequest())

    def flame_effect_off(self):
        self.send(FlameEffectOffRequest())

    def fan_boost_on(self):
        self.send(FanBoostOnRequest())

    def fan_boost_off(self):
        self.send(FanBoostOffRequest())

    def pin(self):
        return self._pin

    def serial(self):
        return self._serial
