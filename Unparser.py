from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import xml.etree.cElementTree as ElementTree

INTRO = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
"""

def _unparse_dict(x, element):
  for key, value in x.iteritems():
    key_element = ElementTree.SubElement(element, 'key')
    key_element.text = key


def unparse(x, output=None):
  output = output or sys.stdout
  output.write(INTRO)
  root = ElementTree.Element('plist')
  root.set('version', '1.0')
  _unparse_dict(x, root)
  tree = ElementTree.ElementTree(root)
  tree.write(output)
