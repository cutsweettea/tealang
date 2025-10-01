import terror

from tokenizing.token import Token, UnknownToken

from util import is_valid_token, is_valid_token_type
from _types import valid_tokens

class Node:
    def __init__(self):
        pass
    
class TriggerableNode:
    def get_trigger_types() -> list[type[Token]]:
        terror.IsNotImplementedTError().throw_default('get_trigger')

class StructuredNode(Node):
    def __init__(self, required_structure: list[type[Token] | type[UnknownToken]], tokens: list[Token]):
        if not isinstance(required_structure, list):
            terror.IsNotInstanceTError().throw_formatted_single('required_structure', list, required_structure)

        for token in required_structure:
            print(f'token={token}')
            if not is_valid_token_type(token):
                terror.IsNotInstanceTError().throw_formatted_list_element('required_structure', valid_tokens, token)

        if not isinstance(tokens, list):
            terror.IsNotInstanceTError().throw_formatted_single('tokens', list, tokens)

        for token in tokens:
            if not is_valid_token(token):
                terror.IsNotInstanceTError().throw_formatted_list_element('tokens', valid_tokens, token)

        required_structure_len = len(required_structure)
        for t in range(0, required_structure_len if len(tokens) > required_structure_len else len(tokens)):
            token = tokens[t]
            required_type = required_structure[t]
            print(f'{t}: {required_type}: {isinstance(token, required_type)}')
            if not isinstance(token, required_type):
                terror.IsNotInstanceTError().throw(f'token at index {t} for {self.__class__.__name__} doesn\'t match required type {required_type.__name__}, found {type(token).__name__}\nrequired structure is: {[s.__name__ for s in required_structure]}')
        
        self.required_structure = required_structure

    def check_values(self):
        terror.IsNotImplementedTError().throw_default('check_values')