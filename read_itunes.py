import argparse, datetime, functools, json, operator, plistlib, sys

def dump_json(data, output=sys.stdout, **kwds):
    json.dump(data, output, indent=4, **kwds)


def load_json(filename):
    return json.load(open(filename))


FIELDS = dict(
    album='Album',
    artist='Artist',
    name='Name',
    id='Persistent ID',
    time='Total Time',
    )


def getter(key):
    return lambda d: d.get(key)

GETTER_DICT = {k: getter(v) for k, v in FIELDS.items()}
GET = argparse.Namespace(**GETTER_DICT)

def equal_tracks(x, y):
    return (GET.name(x) == GET.name(y)) and (
        GET.album(x) == GET.album(y)) and (
        GET.artist(x) == GET.artist(y))

def read_tracks(*files):
    result = {}
    for f in files:
        for track in plistlib.load(open(f, 'rb'))['Tracks'].values():
            id = GET.id(track)
            assert id not in result
            result[id] = track
            for k, v in track.items():
                if isinstance(v, datetime.datetime):
                    track[k] = v.isoformat()

    return result


def file_processor(function):
    @functools.wraps(function)
    def process(filename=None, load=load_json, dump=dump_json):
        dump(function(load(filename or sys.argv[1])))

    return process

@file_processor
def summarizer(data):
    def summarize(track):
        result = {}
        for field in FIELDS.values():
            x = track.get(field)
            if x:
                result[field] = x
        return result

    return {k: summarize(track) for k, track in data.items()}

@file_processor
def time_buckets(tracks):
    result = {}
    for t in tracks.values():
        result.setdefault(GET.time(t) or -1, []).append(t)
    return sorted(result.items())


if __name__ == '__main__':
    # dump_json(read_tracks(*sys.argv[1:]))
    # summarizer()
    time_buckets()
