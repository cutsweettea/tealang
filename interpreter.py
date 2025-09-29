import os
import terror
import logging

from tokenizing.token import TokenRegistrar, Token
from tokenizing.unknown import UnknownToken
from tokenizing.data import StringData

from util import is_blank

class Teaterpreter:
    def __init__(self, file_path: str, token_registrar: TokenRegistrar):
        self.logger = logging.getLogger(__name__)
        if not isinstance(file_path, str):
            terror.IsNotInstanceTError().throw_formatted_single('file_path', str, file_data)

        if not isinstance(token_registrar, TokenRegistrar):
            terror.IsNotInstanceTError().throw_formatted_single('token_registrar', str, token_registrar)

        if not os.path.exists(file_path):
            terror.FileDoesNotExistTError().throw(f'file at path {os.path.join(os.getcwd(), file_path)} does not exist')

        with open(file_path, 'r') as f:
            self.file_data = f.read()

        self.logger.debug(f'loaded {file_path} into teaterpreter')
        self.token_registrar = token_registrar

    def process_token(self, token: str):
        if not isinstance(token, str):
            terror.IsNotInstanceTError().throw_formatted_single('token', str, token)

        t = self.token_registrar.find_valid_token(token)
        return UnknownToken(token) if t == None else t

    def process(self) -> list[Token]:
        tokens = []
        current_token = ''
        comment = False
        string = False
        for c in range(len(self.file_data)): 
            char = self.file_data[c]

            # check if code is currently creating a string
            if string:
                # if string ends, append string data and continue to new token
                if char == '"':
                    print(f'ended string @ index {c} w/ data {current_token}')
                    string = False
                    tokens.append(StringData(current_token))
                    current_token = ''
                    continue
                
                # if string continues, add to current token and continue
                current_token += char
                continue

            # check if code is currently being commented, and end comment if a newline starts
            if comment:
                if ord(char) == 10:
                    print(f'ended comment @ index {c}')
                    comment = False
                continue
            
            # checks if the character is a double quote, if so, end comment and continue
            if char == '"':
                print(f'started string @ index {c}')
                string = True
                continue
            
            # checks if the character is a hashtag (comment), if so, end comment and continue
            if char == '#':
                print(f'started comment @ index {c}')
                comment = True
                continue
            
            # checks whether the current character is a valid token (mostly for operators)
            char_token = self.token_registrar.find_valid_token(char)
            if char_token != None:
                # if current char is a valid token, process and add the current token
                # to the tokens. then, add whatever the char's token is, and continue
                if not is_blank(current_token):
                    tokens.append(self.process_token(current_token))
                tokens.append(char_token)
                current_token = ''
                continue
            
            # if the current_token is invalid, check if the current character is a space
            if char == ' ' or char == '\n':
                # if the current character is a space, then check if the current_token is a space, if so, continue
                if is_blank(current_token):
                    print(f'skipping blank {current_token}')
                    continue
                
                # add an unknown token if current_token isn't valid, and it's not just whitespace
                tokens.append(UnknownToken(current_token))
                print(f'adding unknown: {current_token}, {UnknownToken(current_token)}')
                current_token = ''
                continue

            # add current char to current_token, and try to find a valid token
            current_token += char
            token = self.token_registrar.find_valid_token(current_token)
            print(f'{ord(char)}: {current_token}, {token}')

            # if the current_token is valid, add it to the token list, resets the current_token and continue
            if token != None:
                tokens.append(token)
                current_token = ''
                continue
            
            # check if EOF, adds final token if so
            if c == len(self.file_data)-1:
                tokens.append(UnknownToken(current_token) if token == None else token)

        return tokens