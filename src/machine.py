import sys
import struct
import opcodes
import operator

class Machine:
    def __init__(self, bytecodes: bytes):
        self.codes = bytecodes
        self._index = 0
        self._stack = []

    def get_op(self):
        return struct.unpack('b', self.get_bytes(1))[0]

    def get_int(self):
        return struct.unpack('i', self.get_bytes(4))[0]

    def get_real(self):
        return struct.unpack('f', self.get_bytes(4))[0]

    def get_bytes(self, i):
        res = self.codes[self._index:self._index+i]
        self._index += i
        return res

    def push(self, val):
        self._stack.append(val)

    def pop(self):
        return self._stack.pop(0)

    def execute(self):
        val = None
        while val is None:
            val = self.execute_one()
        return val

    def execute_one(self):
        cur = self.get_op()
        if cur == opcodes.PUSH_CONST_INT:
            self.push(self.get_int())
        elif cur == opcodes.PUSH_CONST_REAL:
            self.push(self.get_real())
        elif opcodes.BIN_ADD <= cur <= opcodes.BIN_OR:
            left = self.pop()
            right = self.pop()
            self.push({opcodes.BIN_ADD: operator.add,
                    opcodes.BIN_SUB: operator.sub,
                    opcodes.BIN_MUL: operator.mul,
                    opcodes.BIN_DIV: operator.truediv,
                    opcodes.BIN_POW: operator.pow,
                    opcodes.BIN_LSHIFT: operator.lshift,
                    opcodes.BIN_RSHIFT: operator.rshift,
                    opcodes.BIN_AND: operator.and_,
                    opcodes.BIN_XOR: operator.xor,
                    opcodes.BIN_OR: operator.or_}[cur](left, right))
        elif cur == opcodes.TERM_PLUS:
            pass
        elif cur == opcodes.TERM_MINUS:
            self.push(-self.pop())
        elif cur == opcodes.RET_VAL:
            return self.pop()


def run(bytecodes):
    return Machine(bytecodes).execute()

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('Input file path should be given as argument.')
        exit(-1)
    with open(sys.argv[1], 'rb') as f:
        print(run(f.read()))
