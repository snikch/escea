import socket
import binascii

from escea.message import (
    ErrorResponse,
    ResponseMessage,
    StateRequest,
    SetTempRequest,
    TurnOnRequest,
    TurnOffRequest,
    FlameEffectOnRequest,
    FlameEffectOffRequest,
    FanBoostOnRequest,
    FanBoostOffRequest,
)


class Fire(object):
    UDP_PORT = 3300
    def __init__(self, ip, prefix, suffix):
        super(Fire, self).__init__()
        self.ip = ip
        self.prefix = prefix
        self.suffix = suffix

    def start(self, ip):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', Fire.UDP_PORT))

    def stop(self):
        self.sock.close()

    def send(self, message):
        data = ''
        try:
            self.sock.sendto(message.payload(), (self.ip, Fire.UDP_PORT))
            self.sock.settimeout(2)
            data, server = self.sock.recvfrom(1024)
            data = binascii.hexlify(data)
        except socket.timeout:
            return ErrorResponse('timeout')

        return ResponseMessage(data).Response()

    def state(self):
        return self.send(StateRequest(self.prefix, self.suffix)).state

    def setTemp(self, target):
        return self.send(SetTempRequest(self.prefix, self.suffix, target)).state

    def turnOn(self):
        return self.send(TurnOnRequest(self.prefix, self.suffix)).state

    def turnOff(self):
        return self.send(TurnOffRequest(self.prefix, self.suffix)).state

    def flameEffectOn(self):
        return self.send(FlameEffectOnRequest(self.prefix, self.suffix)).state

    def flameEffectOff(self):
        return self.send(FlameEffectOffRequest(self.prefix, self.suffix)).state

    def fanBoostOn(self):
        return self.send(FanBoostOnRequest(self.prefix, self.suffix)).state

    def fanBoostOff(self):
        return self.send(FanBoostOffRequest(self.prefix, self.suffix)).state
