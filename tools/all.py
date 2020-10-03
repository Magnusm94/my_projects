
class Tools:

    def __init__(self):
        # import tools here
        from tools.mathematics import Math
        from tools.postgresql import Postgresql
        from tools.repeating_builtins import Reapeating

        # define names here
        self.math = Math()
        self.pg = Postgresql()
        self.repeating = Reapeating
        
