from __future__ import absolute_import, division, print_function, unicode_literals

import os.path
import sys

import Unparser
from Constants import *

def itunes_filename():
  if len(sys.argv) == 1:
    itunes_file = ITUNES_FILE
  else:
    itunes_file = sys.argv[1]
  return os.path.expanduser(itunes_file)

def write_itunes(filename, value, writer=Unparser.unparse):
  with open(filename, 'w') as f:
    writer(value, f)
