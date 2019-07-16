
class CustomAPIException(Exception):
    default_message = 'A server error occurred.'
    default_code = 00000

    def __init__(self, code=None, message=None, data=None):
        self.code = code
        if code is None:
            self.code = self.default_code
        self.message = message
        if message is None:
            self.message = self.default_message
        self.data = data
        if data is None:
            self.data = {}

    def __str__(self):
        return '({} : {} :{})'.format(self.code, self.message, repr(self.data))

    def get_code(self):
        return self.code

    def get_message(self):
        return self.message

    def get_data(self):
        return self.data