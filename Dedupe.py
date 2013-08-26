#!/usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals

from collections import OrderedDict
import operator

from Constants import *
import Parser
from Plural import plural
import Printer
import Util

DELTA_TIME = 2000

itunes = Parser.parse()

track_table = {}

for track in itunes[0][TRACKS_FIELD].itervalues():
  key = (track.get(NAME_FIELD, '(no name)'),
         track.get(ARTIST_FIELD, '(no artist'))
  track_table.setdefault(key, []).append(track)

removed = 0
preserved = 0
bad_times = 0

for index, tracks in track_table.iteritems():
  def key(track):
    return track.get(TOTAL_TIME_FIELD, 0)
  tracks.sort(key=key)
  last_time = -1
  segments = []
  for track in tracks:
    time = key(track)
    if not time:
      bad_times += 1
      continue
    if (time - last_time) > DELTA_TIME:
      segment = []
      segments.append(segment)
      last_time = time
    segment.append(track)
  for segment in segments:
    removed += len(segment) - 1
    preserved += 1

print('%s, %s removed, %s preserved, %s' %
      (plural(len(track_table), 'track'),
       removed, preserved,
       plural(bad_times, 'bad time')))

  #Util.write_itunes(Util.itunes_filename() + '.test', itunes,
  #                writer=Printer.pretty_print)
