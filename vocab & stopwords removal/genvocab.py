import nltk
import re
stopwords = []
tokens = []
for sline in open("stopwords.txt"):
    for sword in sline.split():
        stopwords.append(sword)

raw = open('data.txt').read()
rawtokens = nltk.word_tokenize(raw)
for rw in rawtokens:
	rw = re.sub('[~`^=!@#$,\.\)\(\:\;?\-\+0-9%&*\/_\{\}\[\]<>\"]', ' ', rw)
	rw = re.sub('[\']', '', rw)
	rw = rw.strip()
	if rw not in set(stopwords):
		if len(rw)>1:
			tokens.append(rw)
words = [w.lower() for w in tokens]
vocab = sorted(set(words))
for word in vocab:
	print(word)