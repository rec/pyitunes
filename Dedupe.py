#!/usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals

from collections import OrderedDict

from Constants import *
from Plural import plural
import Parser
import Printer
import Process
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
  to_remove = []
  inverse_dupes = {}
  tracks = itunes[0][TRACKS_FIELD]
  for id, deletions in dupes.iteritems():
    good_track = tracks[str(id)]
    for dtrack in deletions:
      delete_id = dtrack[TRACK_ID_FIELD]
      inverse_dupes[delete_id] = id
      good_track[PLAY_COUNT_FIELD] = (good_track.get(PLAY_COUNT_FIELD, 0) +
                                      dtrack.get(PLAY_COUNT_FIELD, 0))
      del tracks[str(delete_id)]
      to_remove.append(Process.get_filename(dtrack))

  for playlist in itunes[0][PLAYLISTS_FIELD]:
    for track in playlist[ITEMS_FIELD]:
      replacement = inverse_dupes.get(track[TRACK_ID_FIELD])
      if replacement is not None:
        track[TRACK_ID_FIELD] = replacement
  return to_remove


itunes = Parser.parse()
dupes = find_dupes(make_track_table(itunes))
print('to_remove:', remove_dupes(itunes, dupes))

Util.write_itunes(Util.itunes_filename() + '.test', itunes,
                writer=Printer.pretty_print)
