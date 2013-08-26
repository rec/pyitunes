#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals

from Constants import *

import Parser
from Plural import plural
import Printer
import Process
import Util

itunes = Parser.parse()

tracks, playlists, removed, affected = Process.process(itunes[0])

Util.write_itunes(itunes_file + '.out', itunes)

print('Removed %s and %s from %s.' % (
  plural(len(tracks), 'track'),
  plural(removed, 'entry', 'entries'),
  plural(affected, 'playlist')))

print('Remaining %s and %s.' % (
  plural(len(itunes[0][TRACKS_FIELD]), 'track'),
  plural(len(itunes[0][PLAYLISTS_FIELD]), 'playlist')))

itunes[0][TRACKS_FIELD] = tracks
itunes[0][PLAYLISTS_FIELD] = playlists

Util.write_itunes(itunes_file + '.removed', itunes, writer=Printer.pretty_print)
