from cleanlib import getstopwords,clean_review
from collections import Counter
from nltk import bigrams
import sys

def genvocab(filename):
	wordList = []
	for line in open(filename):
		wordList = wordList + clean_review(line)
	c = Counter(wordList)
	for w in c:
		if c[w]>=2:
			print(w)
	return wordList

'''def genbigrams(wordList):
	bigramsList = list(bigrams(wordList))
	b = Counter(bigramsList)
	for w in b:
		if b[w]>=3:
			print(w[0] + ' ' + w[1]) '''

def main():
	wordList = genvocab(sys.argv[1])
	#genbigrams(wordList)

if __name__ == "__main__":
    main()
