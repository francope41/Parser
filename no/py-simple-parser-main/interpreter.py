from nodes import *
from tokens import TokenType


class Interpreter:
    def __init__(self):
        pass

    def Calc(self, node):
        method_name = node.__class__.__name__ + 'Node'
        method = getattr(self, method_name)
        return method(node)

    def NumberNode(self, node):
        return node.value

    def AdditionNode(self, node: OpNode):
        return self.Calc(node.a) + self.Calc(node.b)

    def MultiplicationNode(self, node: OpNode):
        return self.Calc(node.a) * self.Calc(node.b)

    def DivisionNode(self, node: OpNode):
        try:
            return self.Calc(node.a) / self.Calc(node.b)
        except:
            raise Exception('Invalid division')

    def SubstractionNode(self, node: OpNode):
        return self.Calc(node.a) - self.Calc(node.b)

    def PowerNode(self, node: OpNode):
        return self.Calc(node.a) ** self.Calc(node.b)

