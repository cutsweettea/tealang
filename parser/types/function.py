import terror
import logging

from parser.node import Node

from tokenizing.token import Token
from tokenizing.operators import OpenParentheses, CloseParentheses

from util import is_valid_token, valid_token_names

class FunctionNode(Node):
    def __init__(self, tokens: list[Token]):
        self._logger = logging.getLogger(__name__)
        if not isinstance(tokens, list):
            terror.IsNotInstanceTError().throw_formatted_single('tokens', list, tokens)

        for token in tokens:
            if not is_valid_token(token):
                terror.IsNotInstanceTError().throw_formatted_list_element('tokens', valid_token_names, token)

        # check for open parentheses at first index (required)
        if not isinstance(tokens[1], OpenParentheses):
            terror.IsNotInstanceTError().throw(f'token at first index of a function node must be {OpenParentheses.__name__}, not {tokens[0].__class__.__name__}')

        tokens = tokens[2:]

        final_tokens = []
        inc = 0
        for ti in range(len(tokens)):
            inc += 1
            token = tokens[ti]

            print(f'token={token}')
            if isinstance(token, CloseParentheses):
                self._logger.debug(f'close parentheses found, ending node')
                break
            
            final_tokens.append(token)

        self.final_tokens = final_tokens
        self._length = inc

    def get_size(self):
        return self._length