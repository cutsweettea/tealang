from .token import Token

class Operator(Token):
    pass

class Separate(Operator):
    def __init__(self):
        super().__init__(',')

class Assign(Operator):
    def __init__(self):
        super().__init__('=')