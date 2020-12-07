class EXXX(Exception):
    """Base Exception"""
    def __init__(self, message='خطای عمومی', details=None):
        self.message = message
        self.details = details
        super().__init__(message)

    def __str__(self):
        return self.message


class E000(EXXX):
    """000: Connection Error"""
    def __init__(self, message='عدم اتصال به سرویس ابری', details=None):
        super().__init__(message, details)


class E400(EXXX):
    """400: BadInput Error"""
    def __init__(self, message='داده های ورودی به ابر اشتباه است', details=None):
        super().__init__(message, details)


class E401(EXXX):
    """401: Authorization Error"""
    def __init__(self, message='توکن اشتباه است یا منقضی شده است', details=None):
        super().__init__(message, details)


class E403(EXXX):
    """403: Access Denied"""
    def __init__(self, message='دسترسی به سرویس ابری کافی نیست', details=None):
        super().__init__(message, details)


class E409(EXXX):
    """409: API Error"""
    def __init__(self, message='خطایی در سرویس ابری رخ داده است', details=None):
        super().__init__(message, details)


class E429(EXXX):
    """429: Limit Reach"""
    def __init__(self, message='محدودیت درخواست از ابر. دوباره تلاش کنید', details=None):
        super().__init__(message, details)


class E5XX(EXXX):
    """5xx: Server Error"""
    def __init__(self, message='خطای داخلی سرویس ابر', details=None):
        super().__init__(message, details)
