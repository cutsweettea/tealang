from enum import Enum

from parser.node import Node

# repr by 1 byte (255 int max)
# 0-99:        basic lang stuff
# 100-199:     builtin funcs
# 200-255:     other
class NodeCode(Enum):
    AssignNode = 0
    SpillNode = 100

class MapCode(Enum):
    End = 0
    Sep = 1
    Eos = 255

def get_node_code(node: Node):
    class_name = type(node).__name__
    for nc in NodeCode.__members__:
        if class_name == nc:
            return NodeCode[nc].value
    return None