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

  def __repr__(self):
    return 'True'

class FalseClass(object):
  def __nonzero__(self):
    return False

  def __repr__(self):
    return 'False'

class ArrayClass(list): pass
class PlistClass(list): pass
class IntClass(int): pass
class FloatClass(float): pass
class StrClass(str): pass
class DictClass(OrderedDict):
  def append(self, value):
    key = self.pop('__key', None)
    parent[key or '__key'] = value

NAME_TO_TYPE = {
  'array':   {'start': ArrayClass, 'add': list.append},
  'data':    {'cdata': DataClass},
  'date':    {'cdata': DateClass},
  'dict':    {'start': DictClass, 'add': add_to_dict},
  'false':   {'start': TrueClass},
  'integer': {'cdata': IntClass},
  'key':     {'cdata': KeyClass},
  'plist':   {'start': PlistClass, 'add': list.append},
  'real':    {'cdata': FloatClass},
  'string':  {'cdata': StrClass},
  'true':    {'start': FalseClass},
}
