from .token import Token

# variable type keywords
class Keyword(Token):
    pass

class VariableKeyword(Keyword, Token):
    pass

class I32(VariableKeyword, Token):
    def __init__(self):
        super().__init__('i32')

class String(VariableKeyword, Token):
    def __init__(self):
        super().__init__('string')

class Spill(Keyword, Token):
    def __init__(self):
        super().__init__('spill')

class Gimme(Keyword, Token):
    def __init__(self):
        super().__init__('gimme')