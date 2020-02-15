from crocs.token import *
import re

class LexError(Exception):
    pass

class XSpec:
    pass

class Lexer:
    def __init__(self, xspec, no_errors=False):
        """
        """
        self.root   = xspec.root
        self.data   = ''
        self.offset = 0
        self.no_errorss = no_errors

    def run(self):
        """
        """

        yield Sof('')
        while True:
            tseq = self.consume(self.data)
            self.data = self.data[tseq.clen():]
            if tseq:
                yield from tseq
            else:
                break

        # The loop stops on eof. It is useful for
        # some rules.
        yield Eof('')

    def consume(self, data):
        """
        """
        tseq = self.root.consume(data)
        if not tseq and data:
            self.handle_error()
        return tseq

    def handle_error(self):
        msg = 'Unexpected token: %s' % repr(self.data[:30])
        raise LexError(msg)

    def feed(self, data):
        """
        """
        self.data = data
        self.offset = 0

class LexMap(XNode):
    def __init__(self):
        """
        """
        self.children = []
        super(LexMap, self).__init__()

    def register(self, xnode):
        self.children.append(xnode)

    def consume(self, data):
        """
        """
        if not data:
            return TSeq()

        for ind in self.children:
            tseq = ind.consume(data)
            if tseq:
                return tseq
        return TSeq()

    def __repr__(self):
        return 'LexMap(%s)' % self.children

class LexSeq(XNode):
    """
    """
    def __init__(self, lexmap, *args, type=None):
        self.lexmap = lexmap
        self.xnodes = []
        self.type   = type
        self.xnodes.extend(args)
        lexmap.register(self)

    def consume(self, data):
        """
        """
        tseq = TSeq()
        for ind in self.xnodes:
            slice = data[tseq.clen():]
            token = ind.consume(slice)
            if token:
                tseq.extend(token)
            else:
                return TSeq()
        pass

        if self.type:
            return TSeq(self.type(tseq))
        return tseq
        
    def __repr__(self):
        return 'LexSeq(%s)' % self.xnodes

class SeqNode(XNode):
    def __init__(self, regstr, type=Token, cast=None):
        """
        """

        super(XNode, self).__init__()
        self.regex = re.compile(regstr)
        self.regstr = regstr
        self.type  = type
        self.cast  = cast

    def consume(self, data):
        """
        """

        regobj = self.regex.match(data)
        if regobj:
            return self.mktoken(regobj)
                        
    def mktoken(self, regobj):
        tokval = regobj.group(0)
        token  = self.type(tokval, self.cast)
        return TSeq(token)

    def __repr__(self):
        return 'SeqNode(%s(%s))' % (
            self.type.__name__, repr(self.regstr))

class LexNode(SeqNode):
    def __init__(self, lexmap, regstr, type=Token, cast=None):
        """
        """

        super(LexNode, self).__init__(regstr, type, cast)
        self.lexmap = lexmap
        self.lexmap.register(self)

class LexRef(XNode):
    def __init__(self, xnode):
        self.xnode = xnode
        super(LexRef, self).__init__()
        """
        """

    def consume(self, data):
        """
        """

        tseq = TSeq()
        while True:
            slice = data[tseq.clen():]
            token = self.xnode.consume(slice)
            if not token:
                break
            else:
                tseq.extend(token)
        return tseq
