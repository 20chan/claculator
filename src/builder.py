from typing import List
import node
import tok
from lexer import ParseException

class Builder:
    def __init__(self, toks: List[tok.Token]):
        self.toks = toks
        self.toks.append(tok.Token('', tok.TokenType.EOF))

    def pop(self) -> tok.Token:
        return self.toks.pop(0)

    @property
    def top(self) -> tok.Token:
        return self.toks[0]

    def parse(self) -> node.ProgramNode:
        res = []
        while self.top.type != tok.TokenType.EOF:
            res.append(self.parse_expr())
        return node.ProgramNode(subs=res)

    def parse_expr(self) -> node.Node:
        return self.parse_arith()

    def parse_arith(self) -> node.Node:
        lexpr = self.parse_term()
        if self.top.code in ['+', '-']:
            op = self.pop()
            rexpr = self.parse_arith()
            return node.OpNode(op, [lexpr, rexpr])
        else:
            return lexpr

    def parse_term(self) -> node.Node:
        lexpr = self.parse_factor()
        if self.top.code in ['*', '/']:
            op = self.pop()
            rexpr = self.parse_term()
            return node.OpNode(op, [lexpr, rexpr])
        else:
            return lexpr

    def parse_factor(self) -> node.Node:
        if self.top.code in ['+', '-']:
            return node.TermNode(self.pop(), [self.parse_factor()])
        else:
            return self.parse_atom()

    def parse_atom(self) -> node.Node:
        if self.top.code == '(':
            self.pop()
            expr = self.parse_expr()
            if self.pop().code != ')':
                raise ParseException('괄호 파싱 에러')
            return expr
        return node.ValueNode(self.pop())

def build(code) -> node.ProgramNode:
    return Builder(__import__('lexer').parse(code)).parse()
