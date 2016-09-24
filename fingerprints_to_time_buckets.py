import collections, json, sys

def fingerprints_to_time_buckets(fname):
    time_to_track = {}
    for track in json.load(open(fname)):
        tt = track.get('Total Time', -1)
        time_to_track.setdefault(tt, []).append(track)
    sorted_dict = collections.OrderedDict(sorted(time_to_track.items()))
    for time, track in sorted_dict.items():
        print(time, json.dumps(track, indent=4))
    #json.dump(time_to_track, sys.stdout, indent=4)


if __name__ == '__main__':
    fingerprints_to_time_buckets(sys.argv[1])
