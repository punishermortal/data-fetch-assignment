class BlackCofferException(Exception):
    def __init__(self, message, status_code=500):
        self.message = message
        self.status_code = status_code

    def detail(self):
        return {
            "message": self.message,
            "status_code": self.status_code
        }

class AuthenticationException(BlackCofferException):
    def __init__(self, message):
        super().__init__(message, 401)