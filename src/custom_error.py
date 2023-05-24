class InvalidToken(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f'Wrong hash error, {self.message}'
        else:
            return 'Wrong hash error has been raised'


class TkAppClosed(Exception):
    pass


class MaxRetriesExceededError(Exception):
    pass
