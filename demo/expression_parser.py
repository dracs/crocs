"""
"""

from crocs.yacc import Lexer, LexMap, LexNode, Rule, Grammar, Struct, Yacc
from crocs.token import Plus, Minus, LP, RP, Mul, Div, Num, Blank

class CalcTokens:
    lexmap = LexMap()
    LexNode(lexmap, r'\+', Plus)
    LexNode(lexmap, r'\-', Minus)
    LexNode(lexmap, r'\(', LP)
    LexNode(lexmap, r'\)', RP)
    LexNode(lexmap, r'\*', Mul)
    LexNode(lexmap, r'\/', Div)

    LexNode(lexmap, r'[0-9]+', Num)
    LexNode(lexmap, r' +', Blank)

class CalcGrammar:
    expression = Grammar(recursive=True)
    term       = Grammar(recursive=True)
    factor     = Grammar()

    r_plus = Rule(expression, Plus, term)
    r_minus = Rule(expression, Minus, term)
    expression.add(term, r_plus,  r_minus)

    r_mul = Rule(term, Mul, factor)
    r_div = Rule(term, Div, factor)
    term.add(factor, r_mul, r_div)

    r_paren = Rule(LP, expression, RP)
    factor.add(r_paren, Num)

    expression.discard(Blank)

class CalcParser(Yacc):
    def __init__(self):
        self.lexer = Lexer(CalcTokens.lexmap)
        super(CalcParser, self).__init__(CalcGrammar.expression)
    
    def calc(self, data):
        self.lexer.feed(data)
        tokens = self.lexer.run()
        return self.build(tokens)

data = '1 + 2 * (3 /(4 - (5 - (6 + (7 + (8 + (9 + (10 + (11 + (12 + (13+(14 * 15 + 16))))))))))))'
parser = CalcParser()
ptree = parser.calc(data)
print('Consumed:', list(ptree))



