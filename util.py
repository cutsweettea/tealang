from tokenizing.token import Token, UnknownToken

from tokenizing.keywords import I32

from _types import valid_tokens

def is_blank(data: str):
    return data.isspace() or len(data) == 0

def is_valid_token(token) -> bool:
    token_type = type(token)
    return isinstance(token_type, Token) or isinstance(token_type, UnknownToken)

def variable_creation_trigger_keywords():
    return [
        I32
    ]