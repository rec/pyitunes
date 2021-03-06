import argparse, copy, os.path, urllib
from . import Constants, Types


def get_filename(track):
    location = track['Location']
    if location.startswith(FILE_PREFIX):
        return urllib.url2pathname(location[len(Constants.FILE_PREFIX):])


def _exists(track):
    filename = get_filename(track)
    return (not filename) or os.path.exists(filename)


def remove_non_existent_files(itunes):
    removed_tracks = Types.DictClass()
    tracks = itunes[Constants.TRACKS_FIELD]

    to_remove = Types.ArrayClass()
    for key, track in tracks.items():
        if not _exists(track):
            to_remove.append([key, track])

    for key, track in to_remove:
        del tracks[key]
        removed_tracks[key] = track

    return removed_tracks


def remove_missing_tracks_from_playlists(itunes):
    removed_count = 0
    playlists_affected = 0
    removed_playlists = Types.ArrayClass()

    tracks = itunes[Constants.TRACKS_FIELD]
    for playlist in itunes[Constants.PLAYLISTS_FIELD]:
        kept, removed = Types.ArrayClass(), Types.ArrayClass()
        try:
            items = playlist[Constants.ITEMS_FIELD]
        except KeyError:
            continue
        for item in items:
            exists = str(item[Constants.TRACK_ID_FIELD]) in tracks
            (kept if exists else removed).append(item)
        if removed:
            playlist[Constants.ITEMS_FIELD] = kept
            removed_playlist = copy.copy(playlist)
            removed_playlist[Constants.ITEMS_FIELD] = removed
            removed_playlists.append(removed_playlist)
            removed_count += len(removed)
            playlists_affected += 1

    return removed_playlists, removed_count, playlists_affected


def process(itunes):
    removed = copy.copy(itunes)
    tracks = remove_non_existent_files(itunes)
    playlists, removed_playlists, playlists_affected = (
        remove_missing_tracks_from_playlists(itunes))

    return argparse.Namespace(
        tracks=tracks,
        playlists=playlists,
        removed_playlists=removed_playlists,
        playlists_affected=playlists_affected)
