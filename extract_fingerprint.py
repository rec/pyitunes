import json, plistlib, sys

def field_extractor(fields):
    _none = object()

    def f(d):
        result = {}
        for field in fields:
            x = d.get(field, _none)
            if x is not _none:
                result[field] = x
        return result
    return f

SONG_FIELDS = (
    'Album Album',
    'Album',
    'Artist',
    'Name',
    'Persistent ID',
    'Sort Artist',
    'Total Time',
    'Track ID',
    )

SONG_EXTRACTOR = field_extractor(SONG_FIELDS)

def extract_fingerprints(fname, output=sys.stdout):
    result = []
    pl = plistlib.load(open(fname, 'rb'))
    for track in pl['Tracks'].values():
        result.append(SONG_EXTRACTOR(track))

    json.dump(result, output, indent=4)


if __name__ == '__main__':
    extract_fingerprints(sys.argv[1])
