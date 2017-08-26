import unittest
from lexer import parse
from tok import Token, TokenType

class LexerTest(unittest.TestCase):
    def test_integer(self):
        self.assertEqual(parse('1'), [Token('1', TokenType.INTEGER)])
        self.assertEqual(parse('234'), [Token('234', TokenType.INTEGER)])
        self.assertEqual(parse('1 23 456'), [
            Token('1', TokenType.INTEGER),
            Token('23', TokenType.INTEGER),
            Token('456', TokenType.INTEGER),
        ])

    def test_real(self):
        self.assertEqual(parse('1.1'), [Token('1.1', TokenType.REAL)])
        self.assertEqual(parse('03.1415'), [Token('03.1415', TokenType.REAL)])
        self.assertEqual(parse('1.1 2.2 3.3'), [
            Token('1.1', TokenType.REAL),
            Token('2.2', TokenType.REAL),
            Token('3.3', TokenType.REAL),
        ])

    def test_operator(self):
        self.assertEqual(parse('+'), [Token('+', TokenType.OPERATOR)])
        self.assertEqual(parse('-'), [Token('-', TokenType.OPERATOR)])
        self.assertEqual(parse('+ - + -'), [
            Token('+', TokenType.OPERATOR),
            Token('-', TokenType.OPERATOR),
            Token('+', TokenType.OPERATOR),
            Token('-', TokenType.OPERATOR),
        ])

    def test_numeric_expression(self):
        self.assertEqual(parse('1+1'), [
            Token('1', TokenType.INTEGER),
            Token('+', TokenType.OPERATOR),
            Token('1', TokenType.INTEGER),
        ])
        self.assertEqual(parse('+-3.14 + 1'), [
            Token('+', TokenType.OPERATOR),
            Token('-', TokenType.OPERATOR),
            Token('3.14', TokenType.REAL),
            Token('+', TokenType.OPERATOR),
            Token('1', TokenType.INTEGER),
        ])
        self.assertEqual(parse('1+++--2.2---+1'), [
            Token('1', TokenType.INTEGER),
            Token('+', TokenType.OPERATOR),
            Token('+', TokenType.OPERATOR),
            Token('+', TokenType.OPERATOR),
            Token('-', TokenType.OPERATOR),
            Token('-', TokenType.OPERATOR),
            Token('2.2', TokenType.REAL),
            Token('-', TokenType.OPERATOR),
            Token('-', TokenType.OPERATOR),
            Token('-', TokenType.OPERATOR),
            Token('+', TokenType.OPERATOR),
            Token('1', TokenType.INTEGER),
        ])

if __name__ == '__main__':
    unittest.main()
