import re

def getreviewNlabel(filename):
	regex = r'([+-])\s([\s\S]*)\n'
	reviews = []
	labels = []
	with open(filename) as f:
		for line in f:
			m = re.match(regex,line)
			labels.append(m.group(1))
			reviews.append(m.group(2))
	return labels,reviews

def getVocab(filename):
	vocab = []
	vocab_len = 0
	for word in open(filename):
		vocab.append(word.strip())
		if(len(word.split())==1):
			vocab_len = vocab_len+1
	return vocab,vocab_len