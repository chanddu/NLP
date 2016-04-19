from cleanlib import getstopwords,clean_review
from collections import Counter
from nltk import bigrams
import sys

def genvocab(filename):
	wordList = []
	for line in open(filename):
		wordList = wordList + line.split()[1:]
	c = Counter(wordList)
	for w in c:
		if c[w]>=2:
			print(w)

def main():
	wordList = genvocab(sys.argv[1])

if __name__ == "__main__":
    main()
