"""
"""

from crocs.lexer import XSpec, Lexer, LexMap, SeqNode, LexNode, LexSeq
from crocs.token import Token, Keyword, Identifier, RP, LP, Colon, Blank

class KeywordTokens(XSpec):
    lexmap = LexMap()
    t_keyword = LexSeq(SeqNode(r'if', type=Keyword),
    SeqNode(r'\s+', type=Blank))

    t_blank = LexNode(r' +', type=Blank)
    t_lp = LexNode(r'\(', type=LP)
    t_rp = LexNode(r'\)', type=RP)
    t_colon = LexNode(r'\:', type=Colon)

    t_id = LexNode(r'[a-zA-Z0-9]+', type=Identifier)
    lexmap.add(t_keyword, t_blank, t_lp, t_rp, t_colon, t_id)
    root = lexmap

lex = Lexer(KeywordTokens)
data = 'if ifnum: foobar()'
tokens = lex.feed(data)
print('Consumed:', list(tokens))
