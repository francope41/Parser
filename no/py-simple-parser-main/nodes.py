class Number:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'{self.value}'


class OpNode():
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.op = None

    def __repr__(self):
        return f'({self.a}{self.op}{self.b})'


class Addition(OpNode):
    def __init__(self, a, b):
        super()
        self.a = a
        self.b = b
        self.op = '+'


class Substraction(OpNode):
    def __init__(self, a, b):
        super()
        self.a = a
        self.b = b
        self.op = '-'


class Multiplication(OpNode):
    def __init__(self, a, b):
        super()
        self.a = a
        self.b = b
        self.op = '*'


class Division(OpNode):
    def __init__(self, a, b):
        super()
        self.a = a
        self.b = b
        self.op = '/'


class Power(OpNode):
    def __init__(self, a, b):
        super()
        self.a = a
        self.b = b
        self.op = '^'
