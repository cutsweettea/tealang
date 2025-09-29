from .token import Token

# variable type keywords
class Keyword(Token):
    pass

class I32(Keyword):
    def __init__(self):
        super().__init__('i32')

class String(Keyword):
    def __init__(self):
        super().__init__('string')

class Spill(Keyword):
    def __init__(self):
        super().__init__('spill')

class Gimme(Keyword):
    def __init__(self):
        super().__init__('gimme')