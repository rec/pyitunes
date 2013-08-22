#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals

import Parser
import Printer

ITUNES_FILE = '/Users/tom/Music/iTunes/iTunes Music Library.xml'

Printer.pretty_print(Parser.parse(ITUNES_FILE))
