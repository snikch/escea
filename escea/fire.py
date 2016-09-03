import socket

class Fire(object):
    UDP_PORT = 3300
    def __init__(self, ip, prefix, suffix):
        super(Fire, self).__init__()
        self.ip = ip
        self.prefix = prefix
        self.suffix = suffix

    def start(self, ip):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((ip, Fire.UDP_PORT))

    def stop(self):
        self.sock.close()

    def send(self, message):
        self.sock.sendto(message.hex(), (self.ip, Fire.UDP_PORT))
        data, server = self.sock.recvfrom(1024)
        return ResponseMessage(data.encode('hex')).Response()

    def state(self):
        return self.send(StateRequest(self.prefix, self.suffix)).state

    def increaseTemp(self):
        return self.send(IncreateTempRequest(self.prefix, self.suffix)).state

    def decreaseTemp(self):
        return self.send(DecreaseTempRequest(self.prefix, self.suffix)).state

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