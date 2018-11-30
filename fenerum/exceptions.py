
class FenerumError(Exception):
    pass


class FenerumConnectionError(FenerumError):
    pass


class FenerumNotFoundError(FenerumError):
    pass


class FenerumCriticalError(FenerumError):
    pass


class FenerumValidationError(FenerumError):
    pass
