import terror
import logging

from parser.node import Node
from parser.evaluator import Evaluator
from parser.env import Environment

from tokenizing.token import Token
from tokenizing.operators import OpenParentheses, CloseParentheses

from util import is_valid_token, valid_token_names

class FunctionNode(Node):
    def __init__(self, tokens: list[Token], evaluator: Evaluator):
        self._logger = logging.getLogger(__name__)
        if not isinstance(tokens, list):
            terror.IsNotInstanceTError().throw_formatted_single('tokens', list, tokens)

        for token in tokens:
            if not is_valid_token(token):
                terror.IsNotInstanceTError().throw_formatted_list_element('tokens', valid_token_names, token)

        # check for open parentheses at first index (required)
        if not isinstance(tokens[1], OpenParentheses):
            terror.IsNotInstanceTError().throw(f'token at first index of a function node must be {OpenParentheses.__name__}, not {tokens[0].__class__.__name__}')

        self._cutoff = 2
        tokens = tokens[self._cutoff:]

        final_tokens = []
        inc = self._cutoff
        self._logger.debug(f'open parentheses found, starting function info at index {inc}')
        for ti in range(len(tokens)):
            inc += 1
            token = tokens[ti]

            if isinstance(token, CloseParentheses):
                self._logger.debug(f'close parentheses found, ending function info at index {inc}')
                break
            
            final_tokens.append(token)

        evaluated_tokens = evaluator.evaluate(final_tokens)
        self._logger.debug(f'evaluated tokens: {evaluated_tokens}')

        self._final_tokens = evaluated_tokens
        self._length = inc
        self._evaluator = evaluator

    def get_size(self):
        return self._length