import inspect as i


class inspect:

    def __init__(self, code=None):
        self.code = code

    def __call__(self, code=False):
        if not code:
            lines = i.getsource(self.code)
            print(lines)
        else:
            lines = i.getsource(code)
            print(lines)
