import terror
import logging

from util import is_valid_node

class Node: 
    def __repr__(self):
        _ALL_BUILTINS = [
            '__class__',
            '__delattr__',
            '__dict__',
            '__dir__',
            '__doc__',
            '__eq__',
            '__firstlineno__',
            '__format__',
            '__ge__',
            '__getattribute__',
            '__getstate__',
            '__gt__',
            '__hash__',
            '__init__',
            '__init_subclass__',
            '__le__',
            '__lt__',
            '__module__',
            '__ne__',
            '__new__',
            '__reduce__',
            '__reduce_ex__',
            '__repr__',
            '__setattr__',
            '__sizeof__',
            '__static_attributes__',
            '__str__',
            '__subclasshook__',
            '__weakref__',
        ]
        
        obj_dir = dir(self)
        filtered = []

        for v in obj_dir:
            if v in _ALL_BUILTINS:
                continue
            
            if callable(getattr(self, v)):
                continue
            
            if v.startswith('_'):
                continue
            
            filtered.append(v)

        return f'<{self.__class__.__name__} {', '.join([f'{v}={getattr(self, v)}' for v in filtered])}>'

class NodeRegistrar:
    def __init__(self, *nodes: Node):
        self.logger = logging.getLogger(__name__)
        for node in nodes:
            if not is_valid_node(node):
                terror.IsNotInstanceTError().throw_formatted_list_element('nodes', Node, node)

        self.nodes = nodes
        self.logger.debug(f'init setup {len(nodes)} node(s)')

    def find_trigger_node_matches(self):
        matches = {}
        for node in self.nodes:
            if 'TriggerableNode' in [b.__name__ for b in node.__bases__]:
                for t in node.get_trigger_types():
                    matches.update({t: node})
        return matches