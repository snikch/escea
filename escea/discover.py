import socket
import binascii

from escea.message import (
)

from escea.error import (ConnectionTimeout)


class Fire(object):
    UDP_PORT = 3300

    def __init__(self, ip):
        super(Fire, self).__init__()
        self._ip = ip
        self._prefix = '47'
        self._suffix = '46'

    def start(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', Fire.UDP_PORT))

    def stop(self):
        self.sock.close()

    def send(self, message):
        data = ''
        try:
            self.sock.sendto(message.payload(), (self._ip, Fire.UDP_PORT))
            self.sock.settimeout(2)
            data, _ = self.sock.recvfrom(1024)
            data = binascii.hexlify(data)
        except socket.timeout:
            raise ConnectionTimeout

        response = Response(data)
        message.assert_code(response.get(1))
        return response

    def status(self):
        return StatusResponse(self.send(StatusRequest(self._prefix, self._suffix)))

    def set_temp(self, target):
        self.send(SetTempRequest(self._prefix, self._suffix, target))

    def power_on(self):
        self.send(PowerOnRequest(self._prefix, self._suffix))

    def power_off(self):
        self.send(PowerOffRequest(self._prefix, self._suffix))

    def flame_effect_on(self):
        self.send(FlameEffectOnRequest(self._prefix, self._suffix))

    def flame_effect_off(self):
        self.send(FlameEffectOffRequest(self._prefix, self._suffix))

    def fan_boost_on(self):
        self.send(FanBoostOnRequest(self._prefix, self._suffix))

    def fan_boost_off(self):
        self.send(FanBoostOffRequest(self._prefix, self._suffix))
