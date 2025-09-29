# other types of tokens
class UnknownToken:
    def __init__(self, data: str):
        self.data = data

    def __repr__(self):
        return f'[UNK {self.data}]'