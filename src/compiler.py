import argparse
import sys
import struct
from typing import List, Tuple
import node as Node
from tok import TokenType
import opcodes

class Compiler:
    def __init__(self, node: Node.ProgramNode):
        self.node = node

    def convert_to_bytecode(self):
        return self.visit(self.node) + [(opcodes.RET_VAL, b'')]

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
    res = b''
    for op, arg in codes:
        res += bytes([op]) + arg
    return res

def num_to_bytes(x):
    if isinstance(x, int):
        return struct.pack('i', x)
    elif isinstance(x, float):
        return struct.pack('f', x)

def compile2bytes(code):
    from builder import build
    return combine_opcodes(Compiler(build(code)).convert_to_bytecode())

if __name__ == '__main__':
    if len(sys.argv) == 0:
        print('Expression should be given as argument.')
        exit(-1)
    output_file = 'compiled.cla'
    parser = argparse.ArgumentParser()
    parser.add_argument('exp', help='Expression to compile', type=str)
    parser.add_argument('-o', '--out', help='Set output file name', type=str)
    args = parser.parse_args()
    if args.out:
        output_file = args.out
    res = compile2bytes(args.exp)
    with open(output_file, 'wb') as f:
        f.write(res)
    print('done!')
