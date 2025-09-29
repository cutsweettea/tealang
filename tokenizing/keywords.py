from .token import Token

# variable type keywords
class Keyword(Token):
    pass

class VariableKeyword(Keyword):
    pass

class I32(VariableKeyword):
    def __init__(self):
        super().__init__('i32')

class String(VariableKeyword):
    def __init__(self):
        super().__init__('string')

class Spill(Keyword):
    def __init__(self):
        super().__init__('spill')

class Gimme(Keyword):
    def __init__(self):
        super().__init__('gimme')