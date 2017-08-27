class Node:
    def __init__(self, tok=None, subs=None):
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
