import logging

from tokenizing.token import Token

from util import is_valid_token

from terror import *

class AST:
    def __init__(self, tokens: list[Token]):
        if not isinstance(tokens, list):
            IsNotInstanceTError().throw_formatted_single('tokens', list, tokens)
        
        for t in tokens:
            if is_valid_token(t):
                IsNotInstanceTError().throw_formatted_list_element('tokens', Token, t)

        self.tokens = tokens
        self.logger = logging.getLogger(__name__)
        self.parse()

    def parse(self):
        self.logger.debug('AST parsing started...')
        for t in self.tokens:
            self.logger.debug(t)