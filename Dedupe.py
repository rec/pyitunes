#!/usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals

from collections import OrderedDict
import os.path
import sys

from Constants import *
from Plural import plural
import Parser
import Printer
import Process
import Util

DELTA_TIME = 2000


def try_to_print(caption, x):
    try:
        print(caption, x)
    except:
        try:
            print('decode!', caption, x.decode('utf-8'))
        except:
            print('encode!', caption, x.encode('utf-8'))


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
    return track.get(SIZE_FIELD, 0)


def location_key(track):
    return len(track.get(LOCATION_FIELD, ''))


def compare_track(t1, t2):
    return (size_key(t1) - size_key(t2)) or (
        location_key(t1) - location_key(t2))


def find_dupes(track_table):
    removed = 0
    preserved = 0
    bad_times = 0
    dupes = OrderedDict()

    for index, tracks in track_table.iteritems():
        tracks.sort(key=time_key)
        last_time = -1
        segments = []
        for track in tracks:
            time = time_key(track)
            if not time:
                bad_times += 1
                # print('bad time:', track)
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
                segment.sort(cmp=compare_track)
                best = segment.pop()
                dupes[best[TRACK_ID_FIELD]] = segment

    print('%s, %s removed, %s preserved, %s' % (plural(
        len(track_table), 'track'), removed, preserved,
                                                plural(bad_times, 'bad time')))
    return dupes


def remove_dupes_from_database(itunes, dupes):
    dupe_files = []
    inverse_dupes = OrderedDict()
    tracks = itunes[0][TRACKS_FIELD]
    for id, deletions in dupes.iteritems():
        good_track = tracks[str(id)]
        for dtrack in deletions:
            delete_id = dtrack[TRACK_ID_FIELD]
            inverse_dupes[delete_id] = id
            good_track[PLAY_COUNT_FIELD] = (good_track.get(PLAY_COUNT_FIELD, 0)
                                            + dtrack.get(PLAY_COUNT_FIELD, 0))
            del tracks[str(delete_id)]
            dupe_file = Process.get_filename(dtrack)
            if dupe_file:
                dupe_files.append(dupe_file)

    for playlist in itunes[0][PLAYLISTS_FIELD]:
        try:
            items = playlist[ITEMS_FIELD]
        except:
            # print('No items in playlist', playlist.get('Playlist ID', None))
            continue
        for track in items:
            replacement = inverse_dupes.get(track[TRACK_ID_FIELD])
            if replacement is not None:
                track[TRACK_ID_FIELD] = replacement
    return dupe_files


def move_file_dupes(dupe_files, new_directory, output_file):
    with open(output_file, 'w') as out:
        for f in dupe_files:
            path1, fname = os.path.split(f)
            path2, dir1 = os.path.split(path1)
            path3, dir2 = os.path.split(path2)
            dir1 = dir1.decode('utf-8')
            dir2 = dir2.decode('utf-8')
            new_path = os.path.join(new_directory, dir2, dir1)

            mkdir = 'mkdir -p "%s"\n' % new_path
            out.write(mkdir.encode('utf-8'))

            mover = 'mv "%s" "%s"\n' % (f.decode('utf-8'), new_path)
            out.write(mover.encode('utf-8'))


def dedupe(result_directory, result_script):
    itunes = Parser.parse()
    dupes = find_dupes(make_track_table(itunes))
    dupe_files = remove_dupes_from_database(itunes, dupes)
    move_file_dupes(dupe_files, result_directory, result_script)

    Util.write_itunes(Util.itunes_filename() + '.out',
                      itunes,
                      writer=Printer.pretty_print)


if __name__ == '__main__':
    if len(sys.argv) <= 2:
        result_directory = REMOVED_ITUNES_DIRECTORY
    else:
        result_directory = sys.argv[2]

    if len(sys.argv) <= 3:
        result_script = SCRIPT_FILE
    else:
        result_script = sys.argv[3]
    if not os.path.isabs(result_script):
        result_script = os.path.join(result_directory, result_script)

    dedupe(result_directory, result_script)
