from tokenizing.token import Token, UnknownToken

# removing this removes the ImportError??
from parser.nodes import *

def is_blank(data: str):
    return data.isspace() or len(data) == 0

def is_valid_token(token) -> bool:
    token_type = type(token)
    return isinstance(token_type, Token) or isinstance(token_type, UnknownToken)

def all_triggerable_nodes():
    return []