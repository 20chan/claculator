import struct
from typing import List, Tuple
import node as Node
from tok import TokenType
import opcodes

class Compiler:
    def __init__(self, node: Node.ProgramNode):
        self.node = node

    def convert_to_bytecode(self):
        return self.visit(self.node)

    def visit(self, node) -> List[Tuple[int, bytes]]:
        if isinstance(node, Node.ProgramNode):
            if len(node.subs) != 1:
                raise Exception()
            return self.visit(node.subs[0])
        elif isinstance(node, Node.OpNode):
            l = self.visit(node.subs[0])
            r = self.visit(node.subs[1])
            op = {
                '+': opcodes.BIN_ADD,
                '-': opcodes.BIN_SUB,
                '*': opcodes.BIN_MUL,
                '/': opcodes.BIN_DIV,
                '**': opcodes.BIN_POW,
            }[node.tok.code]
            return [*l, *r, (op, b'')]

        elif isinstance(node, Node.TermNode):
            subn = self.visit(node.subs[0])
            if node.tok.code == '-':
                return [*subn, (opcodes.TERM_MINUS, b'')]
            else:
                return [*subn, (opcodes.TERM_PLUS, b'')]
        elif isinstance(node, Node.ValueNode):
            if node.tok.type == TokenType.INTEGER:
                return [(opcodes.PUSH_CONST_INT, num_to_bytes(int(node.tok.code)))]
            elif node.tok.type == TokenType.REAL:
                return [(opcodes.PUSH_CONST_REAL, num_to_bytes(float(node.tok.code)))]


def combine_opcodes(codes: List[Tuple[int, bytes]]):
    pass

def num_to_bytes(x):
    if isinstance(x, int):
        return x.to_bytes(4, 'big')
    elif isinstance(x, float):
        # TODO: 바이트 배열의 크기 고정
        return struct.pack('f', x)

if __name__ == '__main__':
    from builder import build
    c = Compiler(build('1+1'))
    res = c.convert_to_bytecode()
    print(res)
