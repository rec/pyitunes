#!/usr/bin/env python

from __future__ import (
    absolute_import, division, print_function, unicode_literals)


import Constants, Parser, Printer, Process, Unparser
from Util import plural

itunes = Parser.parse()

tracks, playlists, removed, affected = Process.process(itunes[0])

Unparser.write_file(Constants.ITUNES_FILE + '.out', itunes)

print('Removed %s and %s from %s.' % (plural(
    len(tracks), 'track'), plural(removed, 'entry', 'entries'),
                                      plural(affected, 'playlist')))

print('Remaining %s and %s.' % (plural(
    len(itunes[0][Constants.TRACKS_FIELD]), 'track'), plural(
        len(itunes[0][Constants.PLAYLISTS_FIELD]), 'playlist')))

itunes[0][Constants.TRACKS_FIELD] = tracks
itunes[0][Constants.PLAYLISTS_FIELD] = playlists

Util.write_itunes(Constants.ITUNES_FILE + '.removed',
                  itunes,
                  writer=Printer.pretty_print)
