import terror
import logging

from parser.node import Node

from parser.nodes.assign import AssignNode
from parser.nodes.spill import SpillNode

from walker.standards import get_node_code, MapCode

class Compiler:
    def __init__(self, nodes: list[Node]):
        self.logger = logging.getLogger(__name__)
        self.logger.debug(f'started compiler w/ {len(nodes)} nodes')
        if isinstance(nodes, list):
            for node in nodes:
                if not isinstance(node, Node):
                    terror.IsNotInstanceTError().throw_formatted_list_element('nodes', Node, node)
        else:
            terror.IsNotInstanceTError().throw_formatted_single('nodes', list, nodes)

        self.nodes = nodes

    def _node_contains_var(self, variable_name: str):
        # currently blank b/c any case where a node uses a variable is compiled
        return False
    
    def compile(self):
        byte_arr_map = bytearray()
        byte_arr_code = bytearray()
        valid_nodes = []
        for node in self.nodes:
            # check if variable, name is used anywhere within the compiled nodes
            if isinstance(node, AssignNode):
                if not self._node_contains_var(node.name):
                    continue
            
            valid_nodes.append(node)

        self.logger.debug(f'filtered nodes down to {len(valid_nodes)}')
        for node in valid_nodes:
            if not isinstance(node, Node):
                terror.InternalNotInstanceTError().throw('alr man')

            byte_arr_map.append(MapCode.End.value)

            byte_repr = get_node_code(node)
            byte_arr_map.append(byte_repr)

            byte_arr_code.append(node.export_bytes())

            self.logger.debug(f'node={node}, byte_repr={byte_repr}, map={byte_arr_map}, code={byte_arr_code}')

        length = 0
        lengths = []
        for b in range(len(byte_arr_code)):
            byte = byte_arr_code[b]
            #print(f'{b}{''.join(' ' for _ in range(len(str(len(byte_arr_code)))-len(str(b))))} {byte}:{''.join(' ' for _ in range(3-len(str(byte))))} {chr(byte)}')

        byte_arr_map.append(MapCode.Eos.value)

        exit(0)
        return byte_arr_map + byte_arr_code