import argparse, sys, xml.parsers.expat
from . import Util, Types

CHAR_COUNT = 40
PRINTED_CHARS = frozenset('!')

class NodeHandler(object):
    def __init__(self, debug=False):
        self.stack = []
        self.element_count = 0
        self.char_count = 0
        if debug:
            self.debug = print
        else:
            def none(*a, **kwd): pass
            self.debug = none

    def StartElementHandler(self, name, attributes):
        self._msg('+')
        self.debug('name:', name)
        self.element_count += 1

        frame = argparse.Namespace()
        frame.handler = Types.get_type(name)
        if not frame.handler.CDATA:
            frame.value = frame.handler()
        self.stack.append(frame)

    def CharacterDataHandler(self, data):
        frame = self.stack[-1]
        if frame.handler.CDATA:
            self._msg('.')
            frame.value = frame.handler(data.encode('utf-8'))

    def EndElementHandler(self, name):
        self._msg('-')
        self.debug('/', name, self.stack)
        value = self.stack.pop().value
        if self.stack:
            frame = self.stack[-1]
            frame.handler.append(frame.value, value)
        else:
            self.return_value = value  # We're done!

    def _msg(self, m):
        if m in PRINTED_CHARS:
            sys.stderr.write(m)
            self.char_count += len(m)
            if self.char_count > CHAR_COUNT:
                sys.stderr.write('\n')
                self.char_count = 0

    def parse(self, filename):
        parser = xml.parsers.expat.ParserCreate()
        parser.StartElementHandler = self.StartElementHandler
        parser.EndElementHandler = self.EndElementHandler
        parser.CharacterDataHandler = self.CharacterDataHandler

        fn = open(filename, encoding='UTF-8')
        for i, line in enumerate(fn):
            parser.Parse(line)
        parser.Parse('', True)
        return self.return_value


def parse(filename):
    return NodeHandler().parse(filename)
