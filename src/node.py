class Node:
    def __init__(self, tok=None, subs=None):
        self.tok = tok
        self.subs = [] if subs is None else subs

class ProgramNode(Node):
    pass

class ValueNode(Node):
    pass

class OpNode(Node):
    pass

class TermNode(Node):
    pass
