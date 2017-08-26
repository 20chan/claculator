import node

class Builder:
    def __init__(self, toks):
        self.toks = toks

    def pop(self):
        return self.toks.pop(0)

    @property
    def top(self):
        return self.toks[0]

    def parse(self) -> node.ProgramNode:
        pass

def build(code):
    return Builder(__import__('lexer').parse(code)).parse()
