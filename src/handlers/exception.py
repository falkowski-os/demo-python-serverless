class UnauthorizedException(Exception):
    def __init__(self):
        super().__init__("Unauthorized")
