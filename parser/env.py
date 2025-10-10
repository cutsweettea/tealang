import terror
import logging

from tokenizing.token import BaseToken, UnknownToken
from tokenizing.keywords import VariableKeyword

class Environment:
    class _variable:
        def __init__(self, var_type: VariableKeyword, var_name: BaseToken, var_val: BaseToken):
            if not isinstance(var_type, VariableKeyword):
                terror.IsNotInstanceTError().throw_formatted_single(f'var_type', VariableKeyword, var_type)

            if not isinstance(var_name, BaseToken):
                terror.IsNotInstanceTError().throw_formatted_single(f'var_name', BaseToken, var_name)

            if not isinstance(var_val, BaseToken):
                terror.IsNotInstanceTError().throw_formatted_single(f'var_val', BaseToken, var_val)

            required_type = var_type.relevant_type()
            try:
                value = required_type(var_val.extract_data())
            except Exception as ex:
                terror.IsNotImplementedTError().throw(f'threw {ex.__class__.__name__}; variable value must be of type required by {var_type.__class__.__name__}, which is {required_type.__name__}')

            self._type = required_type
            self._name = var_name.extract_data()
            self._value = value

        @property
        def var_type(self):
            return self._type
        
        @property
        def name(self):
            return self._name
        
        @property
        def value(self):
            return self._value
        
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._variables = []
        self.logger.debug(f'started environment')
    
    def register_assign(self, variable_type: VariableKeyword, variable_name: BaseToken, variable_value: BaseToken) -> _variable:
        new_var = self._variable(variable_type, variable_name, variable_value)
        self._variables.append(new_var)
        self.logger.debug(f'registered new variable "{new_var.name}" of type {new_var.var_type.__name__} w/ value {new_var.value}')
        return new_var

    def find_match(self, token: UnknownToken):
        if not isinstance(token, UnknownToken):
            terror.IsNotInstanceTError().throw_formatted_single(f'token', UnknownToken, token)

        token_val = token.extract_data()
        for var in self._variables:
            if var.name == token_val:
                return var.value