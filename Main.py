#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals

import sys

import Parser
import Printer
import Unparser

ITUNES_FILE = '/Users/tom/Music/iTunes/iTunes Music Library.xml'
UNPARSE = True

if len(sys.argv) == 1:
  itunes_file = ITUNES_FILE
else:
  itunes_file = sys.argv[1]
  if len(sys.argv) > 2:
    UNPARSE = False

result = Parser.parse(itunes_file)

if UNPARSE:
  Unparser.unparse(result)
else:
  Printer.pretty_print(result)
