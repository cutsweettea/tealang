import terror

from tokenizing.token import Token, UnknownToken, AnyToken

from parser.node import Node
from parser.evaluator import Evaluator

from util import is_valid_token, repr_obj, valid_token_names

class StructuredNode(Node):
    def __init__(self, required_structure: list[type[Token] | type[UnknownToken] | AnyToken], tokens: list[Token], evaluator: Evaluator):
        if not isinstance(required_structure, list):
            terror.IsNotInstanceTError().throw_formatted_single('required_structure', list, required_structure)

        if not isinstance(tokens, list):
            terror.IsNotInstanceTError().throw_formatted_single('tokens', list, tokens)

        for token in tokens:
            if not is_valid_token(token):
                terror.IsNotInstanceTError().throw_formatted_list_element('tokens', valid_token_names, token)

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
        
        self._required_structure = required_structure
        self._tokens = required_tokens
        self._evaluator = evaluator

    def check_values(self):
        terror.IsNotImplementedTError().throw_default('check_values')

    def get_size(self):
        return len(self._required_structure)
    
    def get_tokens(self):
        return self._tokens

    def __repr__(self):
        return repr_obj(self, hidden_attributes=['required_structure'])