import re

regex = r'(.+)\s([0,1])\n?'
s = ""
fpos = open('pos.txt', 'a')
fneg = open('neg.txt', 'a')
with open('data.txt') as f:
    for line in f:
        m = re.match(regex,line)
        if m:
            if m.group(2) == '1':
                s = s + m.group(1).strip()
                fpos.write(s+'\n') 
            elif m.group(2) == '0':
                s = s + m.group(1).strip()
                fneg.write(s+'\n')
            s = ""
        else:
            s = s + line.strip()

