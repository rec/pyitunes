#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals

import os.path
import sys

from Constants import *

import Parser
from Plural import plural
import Printer
import Process
import Unparser

def _write(filename, value, writer=Unparser.unparse):
  with open(filename, 'w') as f:
    writer(value, f)

def _filename():
  if len(sys.argv) == 1:
    itunes_file = ITUNES_FILE
  else:
    itunes_file = sys.argv[1]
  return os.path.expanduser(itunes_file)

itunes_file = _filename()
itunes = Parser.parse(itunes_file)

tracks, playlists, removed, affected = Process.process(itunes[0])

_write(itunes_file + '.out', itunes)

print('Removed %s and %s from %s.' % (
  plural(len(tracks), 'track'),
  plural(removed, 'entry', 'entries'),
  plural(affected, 'playlist')))

print('Remaining %s and %s.' % (
  plural(len(itunes[0][TRACKS_FIELD]), 'track'),
  plural(len(itunes[0][PLAYLISTS_FIELD]), 'playlist')))

itunes[0][TRACKS_FIELD] = tracks
itunes[0][PLAYLISTS_FIELD] = playlists

_write(itunes_file + '.removed', itunes, writer=Printer.pretty_print)
