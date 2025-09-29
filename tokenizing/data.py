from .token import Token
from .keywords import Keyword, String

from enum import Enum
from typing import TypeVar
from terror import IsNotInstanceTError, IsNotSubclassTError

DataT = TypeVar('DataT')

class DataType(Enum):
    STRING = str

class DataToken:
    def __init__(self, respective_keyword: Keyword, data_type: DataType, value: DataT):
        if not issubclass(respective_keyword, Keyword):
            IsNotSubclassTError().throw_formatted_single('respective_keyword', Keyword)

        if not isinstance(data_type, DataType):
            IsNotInstanceTError().throw_formatted_single('data_type', DataType, data_type)

        self.respective_keyword = respective_keyword
        self.data_type = data_type
        self.value = value

    def __repr__(self):
        return f'[{self.data_type.name.upper()} "{self.value}"]'

class StringData(DataToken):
    def __init__(self, value: DataT):
        super().__init__(String, DataType.STRING, value)
        if not isinstance(value, self.data_type.value):
            IsNotInstanceTError().throw(f'string value is not of respective type {self.data_type.value.__name__}')