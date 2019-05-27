import datetime, json, plistlib, sys

def read_tracks(*files):
    result = {}
    for f in files:
        for track in plistlib.load(open(f, 'rb'))['Tracks'].values():
            id = fields.get.id(track)
            assert id not in result
            result[id] = track
            for k, v in track.items():
                if isinstance(v, datetime.datetime):
                    track[k] = v.isoformat()
    return result


if __name__ == '__main__':
    json.dump(read_tracks(*sys.argv[1:]), sys.stdout, indent=4)
