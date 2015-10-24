from __future__ import absolute_import, division, print_function, unicode_literals


def plural(value, name, plural=None):
    if value != 1:
        name = plural or (name + 's')
    return '%d %s' % (value, name)
