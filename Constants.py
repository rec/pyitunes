DEFAULT_ITUNES_FILE = '/Users/tom/Music/iTunes/iTunes Music Library.xml'
REMOVED_ITUNES_DIRECTORY = '/Volumes/Zog/Documents/removed_itunes/'
SCRIPT_FILE = 'remove_old.sh'
FILE_PREFIX = 'file://localhost'

ARTIST_FIELD = 'Artist'
ITEMS_FIELD = 'Playlist Items'
LOCATION_FIELD = 'Location'
NAME_FIELD = 'Name'
PLAYLISTS_FIELD = 'Playlists'
PLAY_COUNT_FIELD = 'Play Count'
SIZE_FIELD = 'Size'
TOTAL_TIME_FIELD = 'Total Time'
TRACKS_FIELD = 'Tracks'
TRACK_ID_FIELD = 'Track ID'

def _itunes_filename():
    import sys

    if len(sys.argv) == 1:
        itunes_file = DEFAULT_ITUNES_FILE
    else:
        itunes_file = sys.argv[1]
    return os.path.expanduser(itunes_file)

ITUNES_FILENAME = _itunes_filename()
