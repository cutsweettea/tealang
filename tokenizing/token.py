import logging

from terror import IsNotInstanceTError

class Token:
    """class for representing all tokens within the code
    """
    def __init__(self, context: str):
        if not isinstance(context, str):
            IsNotInstanceTError().throw_formatted_single(str, context)

        self.context = context

    def __repr__(self):
        return f'[{type(self).__name__.upper()}]'
    
# other types of tokens
class UnknownToken:
    def __init__(self, data: str):
        self.data = data

    def __repr__(self):
        return f'[UNK "{self.data}"]'

class TokenRegistrar:
    def __init__(self, *tokens: Token):
        self.logger = logging.getLogger(__name__)
        for s in tokens:
            if not isinstance(s, Token):
                IsNotInstanceTError().throw_formatted_list_element('tokens', Token, s)

        self.tokens = tokens
        self.logger.debug(f'init setup {len(tokens)} token(s)')

    def find_valid_token(self, token_context: str) -> Token | None:
        """method to find a `Token` with a `context` attribute that equals `token_context`

        Args:
            token_context (str): string to find a matching `Token` by it's `context` attribute
        """

        # iterate thru the tokens, check if the token's context attribute is equal to the token_context, returns if so
        for token in self.tokens:
            if token.context == token_context:
                return token
        
        # return None but im not wasting my precious time on a return statement cuz python does that for me