from __future__ import absolute_import, division, print_function, unicode_literals

from collections import OrderedDict

class _BoolClass(object):
  CDATA = False
  def __nonzero__(self):
    return self.VALUE

  def __repr__(self):
    return repr(self.VALUE)

class ArrayClass(list):
  CDATA = False

class DataClass(str):
  CDATA = True

class DateClass(str):
  CDATA = True

class DictClass(OrderedDict):
  CDATA = False

  def append(self, value):
    key = self.pop('__key', None)
    self[key or '__key'] = value

class FalseClass(_BoolClass):
  VALUE = False

class FloatClass(float):
  CDATA = True

class IntegerClass(int):
  CDATA = True

class KeyClass(str):
  CDATA = True

class PlistClass(list):
  CDATA = False

class StringClass(bytes):
  CDATA = True

  def __str__(self):
    return self.decode('utf-8')

class TrueClass(_BoolClass):
  VALUE = True

SUFFIX = 'Class'

def get_type(name):
  return globals()[name.capitalize() + SUFFIX]

def get_name(value):
  return value.__class__.__name__[:-len(SUFFIX)].lower()

def is_list(value):
  return isinstance(value, (ArrayClass, PlistClass))

def is_dict(value):
  return isinstance(value, DictClass)
