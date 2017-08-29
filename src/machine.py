from tok import TokenType
from builder import build
from operator import add, sub, mul, truediv as div
import node as Node

class Machine:
    def __init__(self, node: Node.ProgramNode):
        self.node = node

    def execute(self):
        return self.visit(self.node)

    def visit(self, node):
        if isinstance(node, Node.ProgramNode):
            if len(node.subs) != 1:
                raise Exception()
            return self.visit(node.subs[0])
        elif isinstance(node, Node.OpNode):
            l = self.visit(node.subs[0])
            r = self.visit(node.subs[1])
            return {'+': add, '-': sub, '*': mul, '/': div}[node.tok.code](l, r)
        elif isinstance(node, Node.TermNode):
            subn = self.visit(node.subs[0])
            return subn * (-1 if node.tok.code == '-' else 1)
        elif isinstance(node, Node.ValueNode):
            if node.tok.type == TokenType.INTEGER:
                return int(node.tok.code)
            else:
                return float(node.tok.code)

def execute(code):
    return Machine(build(code)).execute()
