import terror

from parser.types import StructuredNode, TriggerableNode
from parser.evaluator import Evaluator

from tokenizing.token import Token, UnknownToken, AnyToken
from tokenizing.keywords import VariableKeyword, I32
from tokenizing.operators import Assign

class AssignNode(StructuredNode, TriggerableNode):
    def __init__(self, tokens: list[Token], evaluator: Evaluator):
        super().__init__([VariableKeyword, UnknownToken, Assign, AnyToken], tokens, evaluator)

        tokens = self.get_tokens()
        tokens_len = len(tokens)
        var_type, var_name, var_value = [None for n in range(3)]

        for ti in range(tokens_len):
            token = tokens[ti]
            if ti == 0: var_type = token
            elif ti == 1: var_name = token
            elif ti == 3: var_value = token

        if var_type == None:
            terror.InternalMissingTokenTError().throw('var_type is still None after token grabbing')
        elif var_name == None:
            terror.InternalMissingTokenTError().throw('var_name is still None after token grabbing')
        elif var_value == None:
            terror.InternalMissingTokenTError().throw('var_value is still None after token grabbing')

        var_obj = evaluator.env.register_assign(var_type, var_name, var_value)
        self.var_type = var_obj.var_type
        self.name = var_obj.name
        self.value = var_obj.value

    def get_trigger_types() -> list[type[Token]]:
        return [I32]