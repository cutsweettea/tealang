import terror
import logging

from tokenizing.operators import Concatenate
from tokenizing.token import UnknownToken, BaseToken
from tokenizing.data import StringData

from parser.env import Environment

class Evaluator():
    def _int_concat(self, int1: int, int2: any):
        pass

    def _str_concat(self, str1: StringData | str, str2: any):
        if isinstance(str1, StringData):
            str1 = str1.value
        elif isinstance(str1, str):
            pass
        else:
            terror.IsNotInstanceTError().throw(f'value on left must be a str, not {type(str1).__name__}')

        if isinstance(str2, StringData):
            str2 = str2.value
        elif isinstance(str2, str):
            pass
        elif isinstance(str2, int) or isinstance(str2, float):
            str2 = str(str2)
        else:
            terror.IsNotInstanceTError().throw(f'value on right must be a str, not {type(str2).__name__}')

        return StringData(str1 + str2)
    
    def __init__(self, env: Environment):
        self.logger = logging.getLogger(__name__)
        self.env = env

    def evaluate(self, tokens: list):
        tokens_len = len(tokens)
        self.logger.debug(f'new evaluation started for: {tokens}, len={tokens_len}')
        if tokens_len == 1:
            return tokens

        ti = 0
        while ti < tokens_len:
            tokens_len = len(tokens)
            if ti > tokens_len:
                self.logger.debug(f'returning b/c token index exceeds tokens length ({ti}>{tokens_len})')
                return tokens
            
            self.logger.debug(f'checking @ index {ti} in {tokens}, len={tokens_len}')
            token = tokens[ti]
            
            if isinstance(token, Concatenate):
                self.logger.debug(f'found concatenate at index {ti} w/ {ti} skipped')
                # check if token index <= 0 b/c cannot concatenate w/o value on left
                if ti <= 0:
                    terror.MissingConcatenatePartTError().throw(f'missing value on left side to concatenate')

                # check if token index + 1 >= length of tokens b/c cannot concatenate w/o value on right
                if ti+1 >= tokens_len:
                    terror.MissingConcatenatePartTError().throw(f'missing value on right side to concatenate')

                # check if tokens have stored data / typed data, if so, check if types match / can concatenate
                token_left = tokens[ti-1]
                token_right = tokens[ti+1]

                if isinstance(token_left, UnknownToken):
                    token_left = self.env.find_match(token_left)
                
                if isinstance(token_right, UnknownToken):
                    token_right = self.env.find_match(token_right)

                if isinstance(token_left, StringData):
                    concat_res = self._str_concat(token_left.value, token_right)
                    minus_offset = 1
                    idx = ti-minus_offset

                    # 3 - 1 cuz its popping 1 value to the left, the array updates each time and moves the object i wanna remove in the same spot
                    # so idx is constant, 3 is cuz its removing 3 values, so pls work
                    rem1, rem2, rem3 = tokens.pop(idx), tokens.pop(idx), tokens.pop(idx)
                    ti -= (3-minus_offset)

                    tokens.insert(idx, concat_res)
                    self.logger.debug(f'popped tokens; {rem1}, {rem2}, {rem3}, added; {concat_res} @ index {idx}')
                    self.evaluate(tokens)

            ti += 1

        return tokens