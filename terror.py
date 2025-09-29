import logging
import sys
import traceback
import sys

from enum import Enum

class TErrorType(Enum):
    FileDoesNotExist = 1000
    IsNotInstance = 1001
    IsNotSubclass = 1002
    IsNotImplemented = 1003

class TError(Exception):
    """Tea error, AKA terror
    """
    def __init__(self, terror_type: TErrorType):
        self.logger = logging.getLogger(__name__)
        if not isinstance(terror_type, TErrorType):
            self.logger.critical(f'type variable passed to TError must be of type {type(TErrorType).__name__}, not {type(terror_type).__name__}')

        self.terror_type = terror_type

    def throw(self, message: str = None):
        traceback.print_stack()
        print(f'{type(self).__name__}{'' if message is None else f': {message}'}', file=sys.stderr)
        sys.exit(self.terror_type.value)

class FileDoesNotExistTError(TError):
    def __init__(self):
        super().__init__(TErrorType.FileDoesNotExist)

class IsNotImplementedTError(TError):
    def __init__(self):
        super().__init__(TErrorType.IsNotImplemented)

    def throw_default(self, not_implemented_item_name: str):
        super().throw(f'{not_implemented_item_name} is not implemented yet')

class IsNotInstanceTError(TError):
    def __init__(self):
        super().__init__(TErrorType.IsNotInstance)

    def throw_formatted_single(self, variable_name: str, required_type: type | tuple[type], variable_passed):
        correct_type = variable_passed
        if not isinstance(type(correct_type), type): correct_type = type(correct_type)
        super().throw(f'{variable_name} must be of type {' or '.join(t.__name__ for t in required_type) if isinstance(required_type, tuple) else required_type}, not {correct_type.__name__}')

    def throw_formatted_list_element(self, list_name: str, required_type: str | tuple, variable_passed):
        correct_type = variable_passed
        if not isinstance(type(correct_type), type): correct_type = type(correct_type)
        super().throw(f'every {required_type.__name__} within list {list_name} must be of type {' or '.join(t.__name__ for t in required_type) if isinstance(required_type, tuple) else required_type}, not {type(correct_type).__name__}')

class IsNotSubclassTError(TError):
    def __init__(self):
        super().__init__(TErrorType.IsNotSubclass)

    def throw_formatted_single(self, variable_name: str, required_type: type | tuple[type]):
        super().throw(f'{variable_name} must be a subclass of {' or '.join(t.__name__ for t in required_type) if isinstance(required_type, tuple) else required_type}')