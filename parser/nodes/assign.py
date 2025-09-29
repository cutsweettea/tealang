from parser.node import StructuredNode, TriggerableNode

from tokenizing.token import Token, UnknownToken
from tokenizing.keywords import VariableKeyword, Gimme
from tokenizing.operators import Assign

from typing import TypeVar

T = TypeVar('T')

class AssignNode(StructuredNode, TriggerableNode):
    def __init__(self, tokens: list[Token]):
        super().__init__([VariableKeyword, UnknownToken, Assign, UnknownToken], tokens)

    def get_trigger_type() -> type[Token]:
        return Gimme