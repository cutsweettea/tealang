import logging

from parser.node import Node
from parser.nodes.assign import AssignNode
from parser.nodes.spill import SpillNode

from version import ver

# format for binary
# first 2 bytes are 67 and 41 to indicate its a tea file
# next 4 are version indicators, the first 2 bytes are the major, and the last 2 are the minor
# the rest is the exec

class Compiler:
    def __init__(self, nodes: list[Node]):
        self.logger = logging.getLogger(__name__)
        self.__nodes = nodes
        self.__reprs = {
            AssignNode: (1, ['var_type', 'name', 'value']),
            SpillNode: (2, ['strings'])
        }

        self.__var_create_nodes = [
            AssignNode
        ]

    @property
    def nodes(self):
        return self.__nodes

    @property
    def reprs(self):
        return self.__reprs

    def compile(self):
        bts = [67, 41, *[int(x) for x in ver]]
        var_num = 0
        self.logger.debug(f'compiling {len(self.nodes)} nodes...')
        for n in self.nodes:
            node_repr = self.reprs.get(n.__class__)
            if n.__class__ in self.__var_create_nodes:
                self.logger.debug(f'increasing variable count +1 {var_num}->{var_num+1}')
                var_num += 1

            bts.extend([node_repr[0], *n.bexport(var_num), 0])

        return bytes([i ^ 5 for i in bts])