import socket
import sys

# Create a UDP socket
LOCAL_IP = "192.168.0.107"
FIRE_IP = '192.168.0.130'

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

    def stateRequest(self):
        return StateRequest(self.prefix, self.suffix)

    def send(self, message):
        self.sock.sendto(message.hex(), (self.ip, Fire.UDP_PORT))
        data, server = self.sock.recvfrom(1024)
        return ResponseMessage(data.encode('hex')).Response()


class Message(object):

    def __init__(self):
        super(Message, self).__init__()
        self.parts = [ '00' for y in range( 15 ) ]

    def set(self, index, value):
        self.parts[index] = value

    def get(self, index):
        return self.parts[index]

    def string(self):
        str = ''
        for y in self.parts:
            str += y
        return str

    def hex(self):
        return self.string().decode('hex')

class RequestMessage(Message):
    def __init__(self, prefix, suffix):
        super(RequestMessage, self).__init__()
        self.set(0, prefix)
        self.set(14, suffix)

    def command(self, value):
        self.parts[1] = value
        self.parts[13] = value

class StateRequest(RequestMessage):
    def __init__(self, prefix, suffix):
        super(StateRequest, self).__init__(prefix, suffix)
        self.command('31')

class UnknownResponse(object):
    def __init__(self, message):
        super(UnknownResponse, self).__init__()
        self.message = message

class StateResponse(object):
    BOOL={'00': False, '01': True}

    def __init__(self, message):
        super(StateResponse, self).__init__()
        self.state = {
            "target_temp": self.int(message.get(7)),
            "current_temp": self.int(message.get(8)),
            "on": self.bool(message.get(4)),
            "fan_boost": self.bool(message.get(5)),
            "flame_effect": self.bool(message.get(6)),
        }

    def int(self, value):
        return int(value, base=16)

    def bool(self, value):
        return StateResponse.BOOL[value]

class ResponseMessage(Message):
    MESSAGES={'80': StateResponse}
    def __init__(self, message):
        super(ResponseMessage, self).__init__()
        parts = map(''.join, zip(*[iter(message)]*2))
        i = 0
        for part in parts:
            self.set(i, part)
            i += 1

    def Response(self):
        try:
            klass = self.MESSAGES[self.get(1)]
        except KeyError, e:
            return UnknownResponse(self)
        return klass(self)


try:

    fire = Fire(FIRE_IP, '47', '46')
    fire.start(LOCAL_IP)

    resp = fire.send(fire.stateRequest())
    print >>sys.stderr, resp.state

finally:
    fire.stop()
