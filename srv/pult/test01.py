#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def prepare_list2str(list_=[]):
    # преобразуем список в строку
    try:
        buf = ''
        delimiter = ''
        for i in list_:
            ii = "'" + str(i) + "'" if isinstance(i, str) else str(i)
            buf += delimiter + ii
            delimiter = ', '
    except:
        buf = ''
    return buf

print(prepare_list2str(['1', '2', '3', 4, 5, '6', '7', 8]))

'''
a = ['Geeks', 'for', 'Geeks']

# Convert list to string using a loop
res = ''
for s in a:
    res += s + ' '

# Remove trailing space
res = res.strip()
print(res)
'''
