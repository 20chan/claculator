import node
import tok

class Builder:
    def __init__(self, toks):
        self.toks = toks
        self.toks.append(tok.Token('', tok.TokenType.EOF))

    def pop(self):
        return self.toks.pop(0)

    @property
    def top(self):
        return self.toks[0]

    def parse(self) -> node.ProgramNode:
        res = []
        while self.top.type != tok.TokenType.EOF:
            res.append(self.parse_arith())
        return node.ProgramNode(subs=res)

    def parse_arith(self) -> node.Node:
        lexpr = self.parse_factor()
        if self.top.code in ['+', '-']:
            op = self.pop()
            rexpr = self.parse_arith()
            return node.OpNode(op, [lexpr, rexpr])
        else:
            return lexpr

    def parse_factor(self) -> node.Node:
        if self.top.code in ['+', '-']:
            return node.TermNode(self.pop(), [self.parse_factor()])
        else:
            return self.parse_atom()

    def parse_atom(self) -> node.ValueNode:
        return node.ValueNode(self.pop())

def build(code):
    return Builder(__import__('lexer').parse(code)).parse()
