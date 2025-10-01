import terror

from tokenizing.token import Token, UnknownToken, AnyToken

from util import is_valid_token, is_valid_token_type, repr_obj
from _types import valid_tokens

class Node:
    def __init__(self):
        pass
    
    def __repr__(self):
        return repr_obj(self)
    
class TriggerableNode(Node):
    def get_trigger_types() -> list[type[Token]]:
        terror.IsNotImplementedTError().throw_default('get_trigger')

class StructuredNode(Node):
    def __init__(self, required_structure: list[type[Token] | type[UnknownToken] | AnyToken], tokens: list[Token]):
        if not isinstance(required_structure, list):
            terror.IsNotInstanceTError().throw_formatted_single('required_structure', list, required_structure)

        for token in required_structure:
            if not is_valid_token_type(token):
                terror.IsNotInstanceTError().throw_formatted_list_element('required_structure', valid_tokens, token)

        if not isinstance(tokens, list):
            terror.IsNotInstanceTError().throw_formatted_single('tokens', list, tokens)

        for token in tokens:
            if not is_valid_token(token):
                terror.IsNotInstanceTError().throw_formatted_list_element('tokens', valid_tokens, token)

        required_structure_len = len(required_structure)
        missing_token_count = required_structure_len - len(tokens)
        if missing_token_count > 0:
            terror.MissingNodePartTError().throw(f'missing {missing_token_count} tokens, being {', '.join([t.__name__ for t in required_structure[:missing_token_count]])}')

        required_tokens = []
        for t in range(0, required_structure_len):
            token = tokens[t]
            required_type = required_structure[t]

            # skip if it's an anything token
            if required_type == AnyToken: 
                required_tokens.append(token)
                continue
            
            if not isinstance(token, required_type):
                terror.IsNotInstanceTError().throw(f'token at index {t} for {self.__class__.__name__} doesn\'t match required type {required_type.__name__}, found {type(token).__name__}\nrequired structure is: {[s.__name__ for s in required_structure]}')

            required_tokens.append(token)
        
        self.required_structure = required_structure
        self.tokens = required_tokens

    def check_values(self):
        terror.IsNotImplementedTError().throw_default('check_values')

    def get_size(self):
        return len(self.required_structure)

    def __repr__(self):
        return repr_obj(self, hidden_attributes=['required_structure'])