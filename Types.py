from __future__ import absolute_import, division, print_function, unicode_literals

from collections import OrderedDict


class _Class(object):
    CDATA = True
    LIST = False
    DICT = False


class DataClass(str, _Class): pass
class DateClass(str, _Class): pass
class FloatClass(float, _Class): pass
class IntegerClass(int, _Class): pass
class KeyClass(str, _Class): pass

class _List(_Class):
    CDATA = False
    LIST = True


class ArrayClass(list, _List): pass
class PlistClass(list, _List): pass


class _Bool(_Class):
    CDATA = False

    def __nonzero__(self):
        return self.VALUE

    def __repr__(self):
        return repr(self.VALUE)


class TrueClass(_Bool):  VALUE = True
class FalseClass(_Bool): VALUE = False


class DictClass(OrderedDict, _Class):
    CDATA = False
    DICT = True

    def append(self, value):
        key = self.pop('__key', None)
        self[key or '__key'] = value


class StringClass(bytes, _Class):
    def __str__(self):
        return self.decode('utf-8')



SUFFIX = 'Class'


def get_type(name):
    return globals()[name.capitalize() + SUFFIX]


def get_name(value):
    return value.__class__.__name__[:-len(SUFFIX)].lower()
