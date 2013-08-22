from __future__ import absolute_import, division, print_function, unicode_literals

from collections import OrderedDict

def add_to_dict(parent, value):
  key = parent.pop('__key', None)
  parent[key or '__key'] = value


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

class StringClass(str):
  CDATA = True

class TrueClass(_BoolClass):
  VALUE = True

NAME_TO_TYPE = {
  'array':   {'class': ArrayClass, 'start': ArrayClass, 'append': ArrayClass.append},
  'data':    {'class': DataClass, 'cdata': DataClass},
  'date':    {'class': DateClass, 'cdata': DateClass},
  'dict':    {'class': DictClass, 'start': DictClass, 'append': DictClass.append},
  'false':   {'class': FalseClass, 'start': FalseClass},
  'integer': {'class': IntegerClass, 'cdata': IntegerClass},
  'key':     {'class': KeyClass, 'cdata': KeyClass},
  'plist':   {'class': PlistClass, 'start': PlistClass, 'append': PlistClass.append},
  'real':    {'class': FloatClass, 'cdata': FloatClass},
  'string':  {'class': StringClass, 'cdata': StringClass},
  'true':    {'class': TrueClass, 'start': TrueClass},
}

def get_type(name):
  return globals()[name.capitalize() + 'Class']
