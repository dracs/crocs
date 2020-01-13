"""
"""

from crocs.yacc import Lexer, Yacc, LexMap, LexNode, Rule, Grammar, TokVal, Struct, XSpec
from crocs.token import Token, Blank

class WordTokens(XSpec):
    expr = LexMap()
    LexNode(expr, r'[a-zA-Z]+', type=Token)
    LexNode(expr, r' +', type=Blank)
    root = expr

class WordGrammar(Grammar):
    expr = Struct()
    r_phrase0  = Rule(TokVal('alpha'), TokVal('beta'))
    r_phrase1  = Rule(TokVal('gamma'), TokVal('zeta'))
    expr.add(r_phrase0, r_phrase1)

    root = expr
    discard = [Blank]

data = 'alpha beta gamma zeta'
lexer = Lexer(WordTokens)
yacc  = Yacc(WordGrammar)
lexer.feed(data)
tokens = lexer.run()
ptree  = yacc.build(tokens)
print(list(ptree))
