from tokens import TokenType
from nodes import *


class Parser:
    def __init__(self, tokens):
        self.tokens = iter(tokens)
        self.Next()

    def Next(self):
        try:
            self.curr_token = next(self.tokens)
        except StopIteration:
            self.curr_token = None

    def NewNumber(self):
        number = self.curr_token

        if number.type == TokenType.LPAR:
            self.Next()
            result = self.Operation()
            if self.curr_token == None or self.curr_token.type != TokenType.RPAR:
                raise Exception('No right parenthesis for expression!')
            self.Next()
            return result

        if number.type == TokenType.NUMBER:
            self.Next()
            return Number(number.value)

    def NewPow(self):
        result = self.NewNumber()

        while self.curr_token != None and self.curr_token.type == TokenType.POW:
            self.Next()
            result = Power(result, self.NewNumber())

        return result

    def NewTerm(self):
        result = self.NewPow()

        while self.curr_token != None and (self.curr_token.type == TokenType.MULTIPLY or self.curr_token.type == TokenType.DIVISION):
            ttype = self.curr_token.type
            if ttype == TokenType.DIVISION:
                self.Next()
                result = Division(result, self.NewPow())
            elif ttype == TokenType.MULTIPLY:
                self.Next()
                result = Multiplication(result, self.NewPow())

        return result

    def Operation(self):
        result = self.NewTerm()

        while self.curr_token != None and (self.curr_token.type == TokenType.PLUS or self.curr_token.type == TokenType.MINUS):
            ttype = self.curr_token.type
            if ttype == TokenType.PLUS:
                self.Next()
                result = Addition(result, self.NewTerm())
            elif ttype == TokenType.MINUS:
                self.Next()
                result = Substraction(result, self.NewTerm())

        return result

    def Parse(self):
        if self.curr_token == None:
            return None

        res = self.Operation()

        return res
