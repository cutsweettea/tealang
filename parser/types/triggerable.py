import terror

from tokenizing.token import Token

from parser.node import Node

class TriggerableNode(Node):
    def get_trigger_types() -> list[type[Token]]:
        terror.IsNotImplementedTError().throw_default('get_trigger')