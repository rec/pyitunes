import datetime, json, plistlib, sys

class AutoJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return obj.isoformat()
        except AttributeError:
            return JSONEncoder.default(self, obj)

def read_itunes(fname, output=sys.stdout):
    result = {}
    for track in plistlib.load(open(fname, 'rb'))['Tracks'].values():
        result[track['Persistent ID']] = track
    json.dump(result, output, indent=4, cls=AutoJSONEncoder)


if __name__ == '__main__':
    read_itunes(sys.argv[1])
