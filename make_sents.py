# -*- coding: utf-8 -*-
import sys

sent = []
for x in sys.stdin:
    w = x.split('\n')
    if w[0]=='<s>':
    	print ' '.join(sent)
    	sent = []
    else:
        sent.append(w[0])
