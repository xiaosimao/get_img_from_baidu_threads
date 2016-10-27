#!/usr/bin/env python
# coding: utf-8

str_table = {
    '_z2C$q': ':',
    '_z&e3B': '.',
    'AzdH3F': '/'
}

char_table = {
    'w': 'a',
    'k': 'b',
    'v': 'c',
    '1': 'd',
    'j': 'e',
    'u': 'f',
    '2': 'g',
    'i': 'h',
    't': 'i',
    '3': 'j',
    'h': 'k',
    's': 'l',
    '4': 'm',
    'g': 'n',
    '5': 'o',
    'r': 'p',
    'q': 'q',
    '6': 'r',
    'f': 's',
    'p': 't',
    '7': 'u',
    'e': 'v',
    'o': 'w',
    '8': '1',
    'd': '2',
    'n': '3',
    '9': '4',
    'c': '5',
    'm': '6',
    '0': '7',
    'b': '8',
    'l': '9',
    'a': '0'
}


def dec(url):
    # 先替换字符串
    for key, value in str_table.items():
        url = url.replace(key, value)
    return url


def decode(url):
    out = ''
    url = dec(url)
    for i in url:
        if i in char_table.keys():
            i = char_table[i]
            out += i
        else:
            i = i
            out += i
    return out

if __name__ == '__main__':
    url = "ippr_z2C$qAzdH3FAzdH3Ft428_z&e3Bvwvij_z&e3Bgjpjwfj_z&e3Bv54AzdH3FvwpvirtvAzdH3FBAzdH3FBEAzdH3FBEEnc98mddDm0nbnd0Emc9dEEAFEmbdm_z&e3B3r2"
    print decode(url)
