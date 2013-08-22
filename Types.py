from __future__ import absolute_import, division, print_function, unicode_literals

from collections import OrderedDict

def add_to_dict(parent, value):
  key = parent.pop('__key', None)
  parent[key or '__key'] = value

class DataClass(str): pass
class DateClass(str): pass
class KeyClass(str): pass

class TrueClass(object):
  def __nonzero__(self):
    return True

class FalseClass(object):
  def __nonzero__(self):
    return True

NAME_TO_TYPE = {
  'array':   {'start': lambda: [], 'add': list.append},
  'data':    {'cdata': DataClass},
  'date':    {'cdata': DateClass},
  'dict':    {'start': lambda: OrderedDict(), 'add': add_to_dict},
  'false':   {'start': lambda: TrueClass()},
  'integer': {'cdata': int},
  'key':     {'cdata': KeyClass},
  'plist':   {'start': lambda: [], 'add': list.append},
  'real':    {'cdata': float},
  'string':  {'cdata': str},
  'true':    {'start': lambda: FalseClass()},
}

# TYPE_TO_NAME = {

