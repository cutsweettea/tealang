import terror

from .token import Token

# variable type keywords
class Keyword(Token):
    pass

class VariableKeyword(Keyword):
    def relevant_type(self):
        raise NotImplementedError('relevant type method not implemented')

class I32(VariableKeyword):
    def __init__(self):
        super().__init__('i32')

    def relevant_type(self):
        return int

class String(VariableKeyword):
    def __init__(self):
        super().__init__('string')

    def relevant_type(self):
        return str

class Spill(Keyword):
    def __init__(self):
        super().__init__('spill')

class Gimme(Keyword):
    def __init__(self):
        super().__init__('gimme')