from __future__ import absolute_import, division, print_function, unicode_literals

import sys

from collections import OrderedDict

def _is_big(x):
  if len(x) > 3:
    return True
  for i in x:
    if isinstance(x, dict):
      i = x[i]
    if isinstance(i, dict) or isinstance(i, list):
      return True


class _Printer(object):
  def __init__(self, out=sys.stdout, indentBy=' '):
    self.write = out.write
    self.indentBy = indentBy

  def pretty_print(self, x, indent=''):
    if isinstance(x, OrderedDict):
      self._print_complex(x, indent, False)
    elif isinstance(x, list):
      self._print_complex(x, indent, True)
    else:
      self.write(repr(x))

  def _print_complex(self, item, indent, is_array):
    if _is_big(item):
      writeIf = self.write
    else:
      writeIf = lambda x: x

    self.write(is_array and '[' or '{')
    writeIf('\n')

    newIndent = indent + self.indentBy
    for i in item:
      writeIf(newIndent)

      if not is_array:
        self.write(repr(i) + ': ')
        i = item[i]

      self.pretty_print(i, newIndent)
      self.write(', ')
      writeIf('\n')

    writeIf(indent)
    self.write(is_array and ']' or '}')


def pretty_print(x):
  _Printer().pretty_print(x)
