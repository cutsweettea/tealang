import terror

from tokenizing.token import Token, UnknownToken

from util import is_valid_token

class Node:
    def __init__(self):
        pass
    
class TriggerableNode:
    def get_trigger_type() -> Token:
        terror.IsNotImplementedTError().throw_default('get_trigger')

class StructuredNode(Node):
    def __init__(self, required_structure: list[type[Token] | type[UnknownToken]], tokens: list[Token]):
        if not isinstance(required_structure, list):
            terror.IsNotInstanceTError().throw_formatted_single('required_structure', list, required_structure)

        for token in required_structure:
            if not is_valid_token(token):
                terror.IsNotInstanceTError().throw_formatted_list_element('required_structure', (Token, UnknownToken), token)

        if not isinstance(tokens, list):
            terror.IsNotInstanceTError().throw_formatted_single('tokens', list, tokens)

        for token in tokens:
            if not is_valid_token(token):
                terror.IsNotInstanceTError().throw_formatted_list_element('tokens', (Token, UnknownToken), token)

        for t in range(0, 5 if len(tokens) > 5 else len(tokens)):
            token = tokens[t]
            print(f'{t}: {self.required_structure[t]}')
        
        self.required_structure = required_structure