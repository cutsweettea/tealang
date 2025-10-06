from parser.types import FunctionNode, TriggerableNode

from tokenizing.token import Token
from tokenizing.keywords import Spill
from tokenizing.operators import Assign

class SpillNode(FunctionNode, TriggerableNode):
    def __init__(self, tokens: list[Token]):
        super().__init__(tokens)

    def get_trigger_types() -> list[type[Token]]:
        return [Spill]