import terror

from byterepr import ByteReprable

from parser.types import FunctionNode, TriggerableNode
from parser.evaluator import Evaluator

from tokenizing.token import BaseToken
from tokenizing.keywords import Spill
from tokenizing.data import StringData

class SpillNode(FunctionNode, TriggerableNode, ByteReprable):
    def __init__(self, tokens: list[BaseToken], evaluator: Evaluator):
        super().__init__(tokens, evaluator)

        strings = []
        for ti in range(len(self._final_tokens)):
            token = self._final_tokens[ti]
            if not isinstance(token, StringData):
                terror.IsNotInstanceTError().throw_formatted_list_element('tokens', StringData, token)

            strings.append(token.extract_data())

        self.__string = ''.join(strings)

    @property
    def string(self):
        return self.__string

    def bexport(self, *vals) -> bytes:
        return self._repr_vals([
            self.string
        ])

    def get_trigger_types() -> list[type[BaseToken]]:
        return [Spill]