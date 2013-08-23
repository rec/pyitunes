#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals

import sys

import Parser
import Printer
import Process
import Unparser

ITUNES_FILE = '/Users/tom/Music/iTunes/iTunes Music Library.xml'
UNPARSE = False

if len(sys.argv) == 1:
  itunes_file = ITUNES_FILE
else:
  itunes_file = sys.argv[1]
  if len(sys.argv) > 2:
    UNPARSE = True

result = Parser.parse(itunes_file)
tracks, playlists = Process.process(result[0])

if UNPARSE:
  Unparser.unparse(result)
else:
  Printer.pretty_print(result)
