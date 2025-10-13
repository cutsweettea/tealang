import os
import terror
import logging
import json

from tokenizing.tokenizer import Tokenizer

from parser.node import Node
from parser.ast import AST

class Teaterpreter:
    def __init__(self, file_path: str):
        self.logger = logging.getLogger(__name__)
        if not isinstance(file_path, str):
            terror.IsNotInstanceTError().throw_formatted_single('file_path', str, file_data)

        if not os.path.exists(file_path):
            terror.FileDoesNotExistTError().throw(f'file at path {os.path.join(os.getcwd(), file_path)} does not exist')

        with open(file_path, 'r') as f:
            self.file_data = f.read()

        self.logger.debug(f'loaded {file_path} into teaterpreter')
        self.tokenizer = Tokenizer(self.file_data)

    def compile(self, file_path: str):
        tokens = self.tokenizer.process()
        self.logger.debug(f'found tokens; {tokens}')
        
        ast_bytes = AST(tokens).compile()
        self.logger.debug(f'found bytes; {ast_bytes}')

        with open(file_path, 'wb') as f:
            f.write(ast_bytes)

        self.logger.debug(f'wrote compiled file to {file_path}')