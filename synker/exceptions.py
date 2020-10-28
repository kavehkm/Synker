# provider exceptions
class EXXX(Exception):
    """Base Exception"""
    def __init__(self, message=''):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message


class E000(EXXX):
    """000: Connection Error"""
    pass


class E400(EXXX):
    """400: BadInput Error"""
    pass


class E401(EXXX):
    """401: Authorization Error"""
    pass


class E403(EXXX):
    """403: Access Denied"""
    pass


class E409(EXXX):
    """409: API Error"""
    pass


class E429(EXXX):
    """429: Limit Reach"""
    pass


class E5XX(EXXX):
    """5xx: Server Error"""
    pass
