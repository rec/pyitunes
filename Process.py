from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import os.path
import urllib

import Types

_PREFIX = 'file://localhost'
_TRACKS = 'Tracks'
_PLAYLISTS = 'Playlists'
_ITEMS = 'Playlist Items'
_TRACK_ID = 'Track ID'

def _exists(track):
  location = track['Location']
  if not location.startswith(_PREFIX):
    return True

  filename = urllib.url2pathname(location[len(_PREFIX):])
  return os.path.exists(filename)

def remove_non_existent_files(itunes):
  removed_tracks = Types.DictClass()
  tracks = itunes[_TRACKS]

  to_remove = Types.ArrayClass()
  for key, track in tracks.iteritems():
    if not _exists(track):
      to_remove.append([key, track])

  for key, track in to_remove:
    del tracks[key]
    removed_tracks[key] = track

  return removed_tracks

def remove_missing_tracks_from_playlists(itunes):
  removed_playlists = Types.ArrayClass()

  tracks = itunes[_TRACKS]
  for playlist in itunes[_PLAYLISTS]:
    kept, removed = Types.ArrayClass(), Types.ArrayClass()
    try:
      items = playlist[_ITEMS]
    except KeyError:
      continue
    for item in items:
      (kept if str(item[_TRACK_ID]) in tracks else removed).append(item)
    if removed:
      playlist[_ITEMS] = kept
      removed_playlist = copy.copy(playlist)
      removed_playlist[_ITEMS] = removed
      removed_playlists.append(removed_playlist)

  return removed_playlists

def process(itunes):
  removed = copy.copy(itunes)
  removed[_TRACKS] = remove_non_existent_files(itunes)
  removed[_PLAYLISTS] = remove_missing_tracks_from_playlists(itunes)

  return removed
