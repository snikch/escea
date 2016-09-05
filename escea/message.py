import binascii

class Message(object):
    def __init__(self):
        super(Message, self).__init__()
        self.parts = [ '00' for y in range( 15 ) ]

    def set(self, index, value):
        self.parts[index] = value

    def get(self, index):
        return self.parts[index]

    def __str__(self):
        str = ''
        for y in self.parts:
            str += y
        return str

    def payload(self):
        return binascii.unhexlify(self.__str__())

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

class SetTempRequest(RequestMessage):
    def __init__(self, prefix, suffix, temp):
        super(SetTempRequest, self).__init__(prefix, suffix)
        self.command('57')
        self.set(2, '01')
        self.set(3, format(int(temp), 'x'))

class TurnOnRequest(RequestMessage):
    def __init__(self, prefix, suffix):
        super(TurnOnRequest, self).__init__(prefix, suffix)
        self.command('39')

class TurnOffRequest(RequestMessage):
    def __init__(self, prefix, suffix):
        super(TurnOffRequest, self).__init__(prefix, suffix)
        self.command('3a')

class FanBoostOnRequest(RequestMessage):
    def __init__(self, prefix, suffix):
        super(FanBoostOnRequest, self).__init__(prefix, suffix)
        self.command('37')

class FanBoostOffRequest(RequestMessage):
    def __init__(self, prefix, suffix):
        super(FanBoostOffRequest, self).__init__(prefix, suffix)
        self.command('38')

class FlameEffectOnRequest(RequestMessage):
    def __init__(self, prefix, suffix):
        super(FlameEffectOnRequest, self).__init__(prefix, suffix)
        self.command('56')

class FlameEffectOffRequest(RequestMessage):
    def __init__(self, prefix, suffix):
        super(FlameEffectOffRequest, self).__init__(prefix, suffix)
        self.command('55')

class UnknownResponse(object):
    def __init__(self, message):
        super(UnknownResponse, self).__init__()
        self.state = message

class ErrorResponse(object):
    def __init__(self, message):
        super(ErrorResponse, self).__init__()
        self.message = message
        self.state = 'Error'

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
        self.message = message
        if message != None:
            parts = map(''.join, zip(*[iter(message.decode())]*2))
            i = 0
            for part in parts:
                self.set(i, part)
                i += 1

    def Response(self):
        if self.message == None:
            return ErrorResponse(self)
        try:
            klass = self.MESSAGES[self.get(1)]
        except KeyError as e:
            return UnknownResponse(self)
        return klass(self)
