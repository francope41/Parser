from enum import Enum


class TokenType(Enum):
    NUMBER = 0
    MINUS = 1
    PLUS = 2
    DIVISION = 3
    MULTIPLY = 4
    POW = 5
    LPAR = 6
    RPAR = 6


class Token:
    def __init__(self, type: TokenType, value=None):
        self.type = type
        self.value = value
        self.precedence = type.value

    def __repr__(self):
        if self.type == TokenType.NUMBER:
            return f'{self.type.name}: {self.value}'
        else:
            return f'{self.type.name}'
