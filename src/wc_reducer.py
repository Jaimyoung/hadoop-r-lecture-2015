#!/usr/bin/env python
""" Reducer for word counter Hadoop Streaming Job
"""

import sys

word_dict = dict()

for line in sys.stdin:
    line = line.strip()
    word, count = line.split('\t', 1)
    count = int(count)

    if word in word_dict:
        word_dict[word] += 1
    else:
        word_dict[word] = 1

for word, count in word_dict.iteritems():
    print '%s\t%s' % (word, count)
