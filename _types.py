from tokenizing.token import Token, UnknownToken, AnyToken
from tokenizing.keywords import VariableKeyword
from tokenizing.operators import Assign
from tokenizing.data import DataToken

valid_tokens = (Token, UnknownToken, VariableKeyword, DataToken, Assign, AnyToken)