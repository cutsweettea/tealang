import logging

from tokenizing.token import Token

from .nodes.assign import AssignNode

from util import is_valid_token, variable_creation_trigger_keywords

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
        all_trigger_types = variable_creation_trigger_keywords()
        nodes = []
        for t in range(len(self.tokens)):
            token = self.tokens[t]
            if type(token) in all_trigger_types:
                assign_stmt = AssignNode(self.tokens[t:])
                print(f'appended assign: {assign_stmt}')
                nodes.append(assign_stmt)