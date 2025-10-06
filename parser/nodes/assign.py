from parser.types import StructuredNode, TriggerableNode

from tokenizing.token import Token, UnknownToken, AnyToken
from tokenizing.keywords import VariableKeyword, I32
from tokenizing.operators import Assign

class AssignNode(StructuredNode, TriggerableNode):
    def __init__(self, tokens: list[Token]):
        super().__init__([VariableKeyword, UnknownToken, Assign, AnyToken], tokens)

    def get_trigger_types() -> list[type[Token]]:
        return [I32]