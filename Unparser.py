import sys
from xml.etree.elementTree import SubElement, ElementTree, Element

import Types

INTRO = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
"""


def _unparse_dict(element, x):
    try:
        for key, value in x.items():
            SubElement(element, 'key').text = key
            sub = SubElement(element, Types.get_name(value))
            _unparse_value(sub, value)
    except:
        # print('dict', element, value)
        raise


def _unparse_list(element, value):
    for v in value:
        _unparse_dict(SubElement(element, 'dict'), v)


def _unparse_value(element, value):
    try:
        if value.CDATA:
            if hasattr(value, 'decode'):
                value = value.decode('utf-8')
            else:
                value = str(value)

            element.text = value

        elif value.LIST:
            _unparse_list(element, value)

        elif value.DICT:
            _unparse_dict(element, value)
    except:
        # print('value', element, value)
        raise


def indent(elem, level=0, more_sibs=False):
    i = "\n"
    if level:
        i += (level - 1) * '  '
    num_kids = len(elem)
    if num_kids:
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
            if level:
                elem.text += '  '
        count = 0
        for kid in elem:
            indent(kid, level + 1, count < num_kids - 1)
            count += 1
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
            if more_sibs:
                elem.tail += '  '
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
            if more_sibs:
                elem.tail += '  '


def unparse(x, output=None):
    output = output or sys.stdout
    output.write(INTRO)
    root = Element('plist')
    root.set('version', '1.0')
    _unparse_value(root, x)
    indent(root)
    tree = ElementTree(root)
    tree.write(output, encoding='utf-8')


def unparse_file(filename, value):
    with open(filename, 'w') as f:
        unparse(value, f)
