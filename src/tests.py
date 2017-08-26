import unittest
from lexer import parse
from tok import Token, TokenType

class LexerTest(unittest.TestCase):
    def test_integer(self):
        self.assertEqual(parse('1'), [Token('1', TokenType.INTEGER)])

if __name__ == '__main__':
    unittest.main()
