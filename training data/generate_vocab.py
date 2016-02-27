import nltk
import re

text = []
stopwords = []
for sline in open("english"):
    for sword in sline.split():
        stopwords.append(sword)

for line in open("data.txt"):
    line = re.sub('[!@#$,\.\)\(\:\;\"?\-\+0-9\'%&*\/]', '', line)
    for word in line.split():
        if word.lower() not in set(stopwords):
            text.append(word.lower())

for data in sorted(set(text)):
    print data
