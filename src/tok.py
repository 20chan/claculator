from enum import Enum
from collections import namedtuple

Token = namedtuple('Token', ['code', 'type'])

def is_split_char(char):
    return char in ' \r\n\t'

def is_operator(char):
    return char in '+-'

class TokenType(Enum):
    NONE = 0
    OPERATOR = 1
    INTEGER = 2
    REAL = 3