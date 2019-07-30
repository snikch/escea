class EsceaError(Exception):
    pass


class ConnectionTimeout(EsceaError):
    pass


class UnexpectedResponse(EsceaError):
    pass


class CRCInvalid(EsceaError):
    pass


class InvalidTemp(EsceaError):
    def __init__(self, temp, min, max):
        super(InvalidTemp, self).__init__(
            "Invalid Temperature Supplied. {} is not within {} < °C < {}.".
            format(temp, min, max))
