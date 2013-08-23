from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import os.path

_PREFIX = 'file://localhost'
_TRACKS = 'Tracks'
_PLAYLISTS = 'Playlists'
_ITEMS = 'Playlist Items'
_TRACK_ID = 'Track ID'

def _exists(track):
  location = track['Location']
  if location.startswith(_PREFIX):
    filename = location[len(_PREFIX):].replace('%20', ' ')
    assert '%' not in filename, filename
    return os.path.exists(filename)

def remove_non_existent_files(itunes):
  removed_tracks = {}
  tracks = itunes[_TRACKS]

  to_remove = []
  for key, track in tracks.iteritems():
    if not _exists(track):
      to_remove.append([key, track])

  for key, track in to_remove:
    del tracks[key]
    removed_tracks[key] = track

  return removed_tracks

def remove_missing_tracks_from_playlists(itunes):
  removed_playlists = []

  tracks = itunes[_TRACKS]
  for playlist in itunes[_PLAYLISTS]:
    kept, removed = [], []
    items = playlist[_ITEMS]
    for item in items:
      (kept if str(item[_TRACK_ID]) in tracks else removed).append(item)
    if removed:
      playlist[_ITEMS] = kept
      removed_playlist = copy.copy(playlist)
      removed_playlist[_ITEMS] = removed
      removed_playlists.append(removed_playlist)

  return removed_playlists

def process(itunes):
  tracks = remove_non_existent_files(itunes)
  playlists = remove_missing_tracks_from_playlists(itunes)
  return tracks, playlists
