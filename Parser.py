from __future__ import absolute_import, division, print_function, unicode_literals

import xml.parsers.expat
import sys

import Types

USE_NEW_TYPES = True

class NodeHandler(object):
  def __init__(self):
    self.stack = []
    self.element_count = 0
    self.debug = False
    self.char_count = 0

  def msg(self, m):
    if m != '!':
      return
    sys.stderr.write(m)
    self.char_count += len(m)
    if self.char_count > 40:
      sys.stderr.write('\n')
      self.char_count = 0

  def StartElementHandler(self, name, attributes):
    self.msg('+')
    if self.debug:
      print('name:', name)
    self.element_count += 1
    frame = {}
    handler = Types.NAME_TO_TYPE[name]
    frame['handler'] = handler
    if 'start' in handler:
      frame['value'] = handler['start']()
    self.stack.append(frame)

  def CharacterDataHandler(self, data):
    frame = self.stack[-1]
    handler = frame['handler']
    if 'cdata' in handler:
      cdata = handler['cdata']
      self.msg('.')
      try:
        frame['value'] = cdata(data)
      except UnicodeEncodeError:
        frame['value'] = 'BAD UNICODE'
      except ValueError:
        if not (cdata is int and data == '-'):
          raise
        else:
          self.msg('!')

  def EndElementHandler(self, name):
    self.msg('-')
    if self.debug:
      print('/', name, self.stack)
    value = self.stack.pop()['value']
    if self.stack:
      frame = self.stack[-1]
      frame['handler']['append'](frame['value'], value)
    else:
      self.value = value  # We're done!

  def make_parser(self):
    parser = xml.parsers.expat.ParserCreate()
    parser.StartElementHandler = self.StartElementHandler
    parser.EndElementHandler = self.EndElementHandler
    parser.CharacterDataHandler = self.CharacterDataHandler
    self.parser = parser

  def parse_file(self, filename):
    self.make_parser()
    for x in open(filename):
      self.parser.Parse(x)
    self.parser.Parse('', True)
    return self.value

def parse(filename):
  return NodeHandler().parse_file(filename)
