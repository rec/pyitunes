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

def make_track_table(itunes):
  track_table = {}

  for track in itunes[0][TRACKS_FIELD].itervalues():
    key = (track.get(NAME_FIELD, '(no name)'),
           track.get(ARTIST_FIELD, '(no artist'))
    track_table.setdefault(key, []).append(track)
  return track_table

def time_key(track):
  return track.get(TOTAL_TIME_FIELD, 0)

def size_key(track):
  try:
    return track[SIZE_FIELD]
  except:
    print('No size in track %s' % track[TRACK_ID_FIELD])
    return 0

def find_dupes(track_table):
  removed = 0
  preserved = 0
  bad_times = 0
  dupes = {}

  for index, tracks in track_table.iteritems():
    tracks.sort(key=time_key)
    last_time = -1
    segments = []
    for track in tracks:
      time = time_key(track)
      if not time:
        bad_times += 1
        print('bad time:', track)
        continue
      if (time - last_time) > DELTA_TIME:
        segment = []
        segments.append(segment)
        last_time = time
      segment.append(track)
    for segment in segments:
      removed += len(segment) - 1
      preserved += 1
      if len(segment) > 1:
        segment.sort(key=size_key)
        best = segment.pop()
        dupes[best[TRACK_ID_FIELD]] = segment


  print('%s, %s removed, %s preserved, %s' %
        (plural(len(track_table), 'track'),
         removed, preserved,
         plural(bad_times, 'bad time')))
  return dupes

def remove_dupes(itunes, dupes):
  pass

itunes = Parser.parse()
dupes = find_dupes(make_track_table(itunes))
remove_dupes(itunes, dupes)

  #Util.write_itunes(Util.itunes_filename() + '.test', itunes,
  #                writer=Printer.pretty_print)
