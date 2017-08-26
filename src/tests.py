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

if __name__ == '__main__':
    unittest.main()
