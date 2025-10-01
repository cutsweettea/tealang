from tokenizing.token import Token, UnknownToken

from tokenizing.keywords import I32

from parser.nodes import Assign

from _types import valid_tokens

def is_blank(data: str):
    return data.isspace() or len(data) == 0

def is_valid_token(token) -> bool:
    for vt in valid_tokens:
        if isinstance(token, vt):
            return token
    return False

def is_valid_token_type(token) -> bool:
    for vt in valid_tokens:
        if token is vt: 
            return True
    return False

def variable_creation_trigger_keywords():
    return {
        I32: Assign
    }