import terror
import logging

from tokenizing.token import Token, TokenRegistrar, UnknownToken
from tokenizing.data import StringData

from tokenizing.keywords import *
from tokenizing.operators import *

from util import is_blank

class Tokenizer:
    def __init__(self, file_data: str):
        if not isinstance(file_data, str):
            terror.IsNotInstanceTError().throw_formatted_single('file_data', str, file_data)

        self.file_data = file_data
        self.logger = logging.getLogger(__name__)

        # setup tokens
        self.token_registrar = TokenRegistrar(
            I32(),
            Spill(),
            Gimme(),
            Separate(),
            Assign(),
            OpenParentheses(),
            CloseParentheses(),
            Concatenate()
        )

        # setup process vars
        self._comment = False
        self._string = False
        self._current_token = ''
        self._line_no = 0
        self._char_index = 0
    
    def process_token(self, token: str):
        if not isinstance(token, str):
            terror.IsNotInstanceTError().throw_formatted_single('token', str, token)

        t = self.token_registrar.find_valid_token(token)
        return UnknownToken(token) if t == None else t
    
    def _formatted_line_info(self):
        return f'{self._line_no}:{self._char_index}'
    
    def toggle_comment(self):
        self._comment = not self._comment
        if self._comment:
            self.logger.debug(f'started comment @ {self._formatted_line_info()}')
        else:
            self.logger.debug(f'ended comment @ {self._formatted_line_info()}')

    def toggle_string(self) -> Token | None:
        self._string = not self._string
        if self._string:
            self.logger.debug(f'started string @ {self._formatted_line_info()}')
        else:
            self.logger.debug(f'ended string @ {self._formatted_line_info()} w/ data "{self._current_token}"')
            data = StringData(self._current_token)

            self._current_token = ''
            return data
        
    def disable_comment(self):
        if not self._comment: 
            return
        
        return self.toggle_comment()
    
    def newline(self):
        self._char_index = 0
        self.disable_comment()

    def process(self) -> list[Token]:
        self.logger.debug('Tokenizing started...')
        tokens = []
        file_data_lines = self.file_data.splitlines()

        for l in range(len(file_data_lines)): 
            self._line_no = l+1
            line = file_data_lines[l]
            
            for c in range(len(line)):
                self._char_index = c
                char = line[c]

                # check if code is currently creating a string
                if self._string:
                    # if string ends, append string data and continue to new token
                    if char == '"':
                        token_str = self.toggle_string()
                        if token_str != None: tokens.append(token_str)
                        continue
                    
                    # if string continues, add to current token and continue
                    self._current_token += char
                    continue

                # check if code is currently being commented, and end comment if a newline starts
                if self._comment:
                    if ord(char) == 10:
                        self.toggle_comment()
                    continue
                
                # checks if the character is a double quote, if so, start string and continue
                if char == '"':
                    self.toggle_string()
                    continue
                
                # checks if the character is a hashtag (comment), if so, start comment and continue
                if char == '#':
                    self.toggle_comment()
                    continue
                
                # checks whether the current character is a valid token (mostly for operators)
                char_token = self.token_registrar.find_valid_token(char)
                if char_token != None:
                    # if current char is a valid token, process and add the current token
                    # to the tokens. then, add whatever the char's token is, and continue
                    current_token = self.process_token(self._current_token)
                    if not is_blank(self._current_token):
                        self.logger.debug(f'adding complete unknown (current): "{self._current_token}", {current_token}')
                        tokens.append(current_token)

                    self.logger.debug(f'adding complete unknown (char): "{char}", {char_token}')
                    tokens.append(char_token)
                    self._current_token = ''
                    continue
                
                # if the self.current_token is invalid, check if the current character is a space
                if char == ' ' or char == ';':
                    # if the current character is a space, then check if the self.current_token is a space, if so, continue
                    if is_blank(self._current_token):
                        continue
                    
                    # add an unknown token if self.current_token isn't valid, and it's not just whitespace
                    unknown_token = UnknownToken(self._current_token)
                    self.logger.debug(f'adding unknown: "{self._current_token}", {unknown_token}')
                    tokens.append(unknown_token)
                    self._current_token = ''
                    continue

                # add current char to self.current_token, and try to find a valid token
                self._current_token += char
                token = self.token_registrar.find_valid_token(self._current_token)

                # if the self.current_token is valid, add it to the token list, resets the self.current_token and continue
                if token != None:
                    self.logger.debug(f'adding known: "{self._current_token}", {token}')
                    tokens.append(token)
                    self._current_token = ''
                    continue
                
            self.newline()

        if not is_blank(self._current_token):
            tokens.append(self.process_token(self._current_token))
        return tokens