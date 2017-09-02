from typing import List
import tok

class ParseException(Exception):
    def __init__(self, msg=''):
        super().__init__(self)
        self.msg = msg

class Lexer:
    def __init__(self, code: str):
        self.code = code
        self._index = 0

    @property
    def cur(self) -> str:
        return self.code[self._index]

    def is_eof(self) -> bool:
        return self._index == len(self.code)

    def get_next_token(self) -> tok.Token:
        while tok.is_split_char(self.cur):
            self._index += 1

        if tok.is_operator(self.cur):
            return self.get_operator()
        if str.isdigit(self.cur):
            return self.get_number()
        if self.cur in ['(', ')']:
            return self.get_paren()
        raise ParseException('알 수 없는 토큰')

    def get_operator(self) -> tok.Token:
        i = self._index
        while len(self.code) > i and tok.is_operator(self.code[self._index:i + 1]):
            i += 1
        res = tok.Token(self.code[self._index:i], tok.TokenType.OPERATOR)
        self._index = i
        return res

    def get_number(self) -> tok.Token:
        return_type = tok.TokenType.INTEGER
        start = self._index
        while not self.is_eof():
            if self.cur == '.':
                if return_type == tok.TokenType.REAL:
                    raise ParseException('숫자 파싱중 에러')
                return_type = tok.TokenType.REAL
            elif not str.isdigit(self.cur):
                break
            self._index += 1
        return tok.Token(self.code[start:self._index], return_type)

    def get_paren(self) -> tok.Token:
        res = tok.Token(self.cur, tok.TokenType.PAREN)
        self._index += 1
        return res

def parse(code) -> List[tok.Token]:
    l = Lexer(code)
    def parse_iter():
        while not l.is_eof():
            yield l.get_next_token()
    return list(parse_iter())
