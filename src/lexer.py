import tok

class ParseException(Exception):
    def __init__(self, msg=''):
        super().__init__(self)
        self.msg = msg

class Lexer:
    def __init__(self, code):
        self.code = code
        self._index = 0

    @property
    def cur(self):
        return self.code[self._index]

    def is_eof(self):
        return self._index == len(self.code)

    def get_next_token(self) -> tok.Token:
        if tok.is_operator(self.cur):
            return self.get_operator()
        if str.isdigit(self.cur):
            return self.get_number()
        raise ParseException('알 수 없는 토큰')

    def get_operator(self) -> tok.Token:
        self._index += 1
        return tok.Token(self.cur, tok.TokenType.OPERATOR)

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

def parse(code):
    l = Lexer(code)
    def parse_iter():
        while not l.is_eof:
            yield l.get_next_token()
    return list(parse_iter())
