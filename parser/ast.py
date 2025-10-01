import logging

from tokenizing.token import Token
from tokenizing.keywords import I32

from .nodes.assign import AssignNode

from .node import Node

from util import is_valid_token
from _types import valid_tokens

from terror import *

class AST:
    def __init__(self, tokens: list[Token]):
        if not isinstance(tokens, list):
            IsNotInstanceTError().throw_formatted_single('tokens', list, tokens)
        
        for t in tokens:
            if not is_valid_token(t):
                IsNotInstanceTError().throw_formatted_list_element('tokens', valid_tokens, t)

        self.tokens = tokens
        self.logger = logging.getLogger(__name__)
        self.parse()

    def parse(self):
        self.logger.debug('AST parsing started...')
        trigger_pairs = self.trigger_keyword_node_pairs()
        nodes = []

        tokens_len = len(self.tokens)
        t = 0
        while t < tokens_len:
            token = self.tokens[t]
            token_type = type(token)
            print(f'token={token}, t={t}')

            # print debug info on triggerable stuff
            # i forgot about this really cool python feature i gotta use this more
            if (node_type := trigger_pairs.get(token_type)) != None:
                self.logger.debug(f'found triggerable token {token_type.__name__} with correlating node {node_type.__name__}')
                stmt = node_type(self.tokens[t:])
                self.logger.debug(f'appended assign: {stmt}')
                nodes.append(stmt)
                t += stmt.get_size()
                continue

            t += 1

    @staticmethod
    def trigger_keyword_node_pairs() -> dict[Token, Node]:
        return {
            I32: AssignNode
        }