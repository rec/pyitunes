import datetime, functools, json, plistlib, sys

def dump_json(data, output=sys.stdout, **kwds):
    json.dump(data, output, indent=4, **kwds)


def load_json(filename):
    return json.load(open(filename))


def read_tracks(*files):
    result = {}
    for f in files:
        for track in plistlib.load(open(f, 'rb'))['Tracks'].values():
            id = track['Persistent ID']
            assert id not in result
            result[id] = track
            for k, v in track.items():
                if isinstance(v, datetime.datetime):
                    track[k] = v.isoformat()

    return result


def file_processor(function):
    @functools.wraps(function)
    def process(filename, load=load_json, dump=dump_json):
        dump(function(load(filename)))

    return process


SUMMARY_FIELDS = (
#    'Album Artist',
    'Album',
    'Artist',
#    'Location',
    'Name',
    'Persistent ID',
    'Sort Artist',
    'Sort Name',
    'Total Time',
    )

@file_processor
def summarizer(data):
    def summarize(track):
        result = {}
        for field in SUMMARY_FIELDS:
            x = track.get(field)
            if x:
                result[field] = x
        return result

    return {k: summarize(track) for k, track in data.items()}


if __name__ == '__main__':
    # dump_json(read_tracks(*sys.argv[1:]))
    summarizer(sys.argv[1])
