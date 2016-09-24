import sys
from pyitunes import Parser

if __name__ == '__main__':
    fname = sys.argv[1] if len(sys.argv) > 1 else 'SampleLibrary.xml'
    result = Parser.parse(fname)

    from pyitunes import Printer
    Printer.pretty_print(result)
