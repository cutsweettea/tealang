import logging

from tokenizing.token import Token
from tokenizing.keywords import I32

from .nodes.assign import AssignNode
from .nodes.spill import SpillNode

from .node import Node, NodeRegistrar

from util import is_valid_token, valid_token_names

from terror import *

class AST:
    def __init__(self, tokens: list[Token]):
        if not isinstance(tokens, list):
            IsNotInstanceTError().throw_formatted_single('tokens', list, tokens)
        
        for t in tokens:
            if not is_valid_token(t):
                IsNotInstanceTError().throw_formatted_list_element('tokens', valid_token_names, t)

        self.tokens = tokens
        self.node_registrar = NodeRegistrar(
            AssignNode,
            SpillNode
        )
        
        self.logger = logging.getLogger(__name__)

    def parse(self):
        self.logger.debug('AST parsing started...')
        trigger_pairs = self.node_registrar.find_trigger_node_matches()

        nodes = []

        tokens_len = len(self.tokens)
        t = 0
        while t < tokens_len:
            token = self.tokens[t]
            token_type = type(token)

            # print debug info on triggerable stuff
            # i forgot about this really cool python feature i gotta use this more
            if (pair := trigger_pairs.get(token_type)) != None:
                self.logger.debug(f'found triggerable token {token_type.__name__} with correlating node {pair.__name__}')
                stmt = pair(self.tokens[t:])
                self.logger.debug(f'appended assign: {stmt}')
                nodes.append(stmt)
                t += stmt.get_size()
            else: t += 1

        return nodes