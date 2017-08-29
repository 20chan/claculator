from tok import Token
from typing import List

class Node:
    def __init__(self, tok: Token = None, subs: List['Node'] = None):
        self.tok = tok
        self.subs = [] if subs is None else subs

    def __eq__(self, other):
        return self.tok == other.tok and self.subs == other.subs

class ProgramNode(Node):
    pass

class ValueNode(Node):
    pass

class OpNode(Node):
    pass

class TermNode(Node):
    pass
