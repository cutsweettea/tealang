from tokenizing.keywords import I32

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

_ALL_BUILTINS = [
    '__class__',
    '__delattr__',
    '__dict__',
    '__dir__',
    '__doc__',
    '__eq__',
    '__firstlineno__',
    '__format__',
    '__ge__',
    '__getattribute__',
    '__getstate__',
    '__gt__',
    '__hash__',
    '__init__',
    '__init_subclass__',
    '__le__',
    '__lt__',
    '__module__',
    '__ne__',
    '__new__',
    '__reduce__',
    '__reduce_ex__',
    '__repr__',
    '__setattr__',
    '__sizeof__',
    '__static_attributes__',
    '__str__',
    '__subclasshook__',
    '__weakref__',
]

def repr_obj(obj: any, *, hidden_attributes: list[str] = [], force_show: list[str] = []):
    obj_dir = dir(obj)
    filtered = []

    for v in obj_dir:
        if v in force_show:
            filtered.append(v)
            continue

        if v in _ALL_BUILTINS:
            continue
        
        if v in hidden_attributes:
            continue
        
        if callable(getattr(obj, v)):
            continue
        
        filtered.append(v)

    return f'<{obj.__class__.__name__} {', '.join([f'{v}={getattr(obj, v)}' for v in filtered])}>'