#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals

import os.path
import sys

import Parser
import Printer
import Process
import Unparser

ITUNES_FILE = '~/Music/iTunes/iTunes Music Library.xml'

WRITER = Unparser.unparse

if len(sys.argv) == 1:
  itunes_file = ITUNES_FILE
else:
  itunes_file = sys.argv[1]
  if len(sys.argv) > 2:
    writer = Printer.pretty_print

itunes_file = os.path.expanduser(itunes_file)

result = Parser.parse(itunes_file)
removed = Process.process(result[0])

with open(itunes_file + '.out', 'w') as f:
  WRITER(result, f)

with open(itunes_file + '.removed', 'w') as f:
  WRITER(removed, f)
