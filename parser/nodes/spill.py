import terror

from parser.types import FunctionNode, TriggerableNode
from parser.evaluator import Evaluator

from tokenizing.token import BaseToken
from tokenizing.keywords import Spill
from tokenizing.data import StringData

from walker.standards import MapCode

class SpillNode(FunctionNode, TriggerableNode):
    def __init__(self, tokens: list[BaseToken], evaluator: Evaluator):
        super().__init__(tokens, evaluator)

        self.strings = []
        for ti in range(len(self._final_tokens)):
            token = self._final_tokens[ti]
            if not isinstance(token, StringData):
                terror.IsNotInstanceTError().throw_formatted_list_element('tokens', StringData, token)

            self.strings.append(token.extract_data())

    def get_trigger_types() -> list[type[BaseToken]]:
        return [Spill]
    
    def export_bytes(self):
        for s in self.strings