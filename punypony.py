import re
import string
import sys
from pprint import pprint

import whois
from unidecode import unidecode

from punypony.lib import mapping_read, mapping_write

PATH = 'test_mapping.json'
START = int('0x1D5A0', 0)
END = sys.maxunicode


def main():
    test_string = "{a}dmin"
    result = find_and_replace_chars(test_string)

    for domain in result:
        whois_query = whois.query(domain)
        print("'%s' %s" % (domain, 'free' if not whois_query else 'registered by %s' % whois_query.registrar))


def find_and_replace_chars(text):
    combinations = []
    mapping = mapping_read(PATH)
    regex = r'\{([A-Za-z0-9_]{1})\}'

    r = re.search(regex, text)
    if not r:
        return [text]
    _c = r.groups()[0]

    assert _c and _c in mapping.keys(), 'Not in mapping'

    possible_replacement = mapping[_c] + [_c]
    if not possible_replacement:
        return

    start, end = r.span()
    for c in possible_replacement:
        _txt = text.replace(text[start:end], c, 1)
        combinations = combinations + find_and_replace_chars(_txt)

    return combinations


def create_mapping():
    print("Type 'save' to save and quit")
    char_map = mapping_read(PATH)
    for i in range(START, END):
        _char = chr(i)
        _str = unidecode(chr(i))
        if _str == "":
            continue

        typed_char = input('(%s) %s: ' % (hex(i), _char)).strip()

        if typed_char == "save":
            break

        if typed_char == "\n" or typed_char == "" or typed_char is None:
            continue

        if typed_char not in string.ascii_letters and typed_char not in string.digits:
            continue

        if char_map.get(typed_char) and isinstance(char_map[typed_char], list):
            if _char not in char_map[typed_char]:
                char_map[typed_char].append(_char)
        else:
            char_map[typed_char] = [_char]

    mapping_write(PATH, char_map)
    print("Created Mapping")
    pprint(char_map)


if __name__ == '__main__':
    main()
