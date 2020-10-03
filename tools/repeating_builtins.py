

class Reapeating:

    def __init__(self):
        pass

    def Try(self, function, data=None, *args, **kwargs):
        try:
            data = function(*args, **kwargs)
        except Exception as e:
            print(e, type(e))
        finally:
            return data


