import argparse, operator

FIELDS = dict(
    album='Album',
    artist='Artist',
    name='Name',
    id='Persistent ID',
    time='Total Time',
    )

def getter(key):
    return lambda d: d.get(key, '')

def equal(key):
    g = getter(key)
    return lambda x, y: g(x).lower() == g(y).lower()

GET = argparse.Namespace(**{k: getter(v) for k, v in FIELDS.items()})
EQ = argparse.Namespace(**{k: equal(v) for k, v in FIELDS.items()})
