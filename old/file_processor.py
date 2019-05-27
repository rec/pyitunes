import functools, itertools, json, plistlib, sys
import fields, group_times

def file_processor(function):
    @functools.wraps(function)
    def process(filename=None):
        data = json.load(open(filename or sys.argv[1]))
        result = function(data)
        print('output size', len(result), file=sys.stderr)
        json.dump(data, sys.stdout, indent=4)

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


def group_by_time(track_dict, radius):
    groups = {}
    for t in track_dict.values():
        groups.setdefault(fields.get.time(t) or -1, []).append(t)

    empties = groups.pop(-1, None)
    if empties:
        yield empties

    for times in group_times.group_times(groups.keys().sorted(), radius):
        yield list(itertools.chain(groups[t] for t in times))


def dedupe_processor(equals):
    @file_processor
    @functools.wraps(equals)
    def simple_dupes(buckets):
        results = []
        for tracks in buckets:
            dupes = []
            for x, y in itertools.combinations(tracks, 2):
                if equals(x, y):
                    (x not in dupes) and dupes.append(x)
                    (y not in dupes) and dupes.append(y)
            dupes and results.append(dupes)
        return results

    return simple_dupes

EQ = fields.EQ

@dedupe_processor
def equal_tracks(x, y):
    return EQ.name(x, y) and EQ.artist(x, y) and EQ.album(x, y)

@dedupe_processor
def name_artist_equal(x, y):
    return EQ.name(x, y) and EQ.artist(x, y)

@dedupe_processor
def name_artist_equal_only(x, y):
    return EQ.name(x, y) and EQ.artist(x, y) and not EQ.album(x, y)

if __name__ == '__main__':
    # dump_json(read_tracks(*sys.argv[1:]))
    # summarizer()
    # time_buckets()
    #equal_tracks()
    name_artist_equal()
