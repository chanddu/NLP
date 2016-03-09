from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
import nltk
import re

text = []
wordnet_lemmatizer = WordNetLemmatizer()
stop = stopwords.words('english')
def is_noun(tag):
	return tag in ['NN', 'NNS', 'NNP', 'NNPS']

def is_verb(tag):
	return tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']

def is_adverb(tag):
	return tag in ['RB', 'RBR', 'RBS']

def is_adjective(tag):
	return tag in ['JJ', 'JJR', 'JJS']

def penn_to_wn(tag):
	if is_noun(tag):
		return wn.NOUN
	elif is_verb(tag):
		return wn.VERB
	elif is_adverb(tag):
		return wn.ADV
	elif is_adjective(tag):
		return wn.ADJ
	return wn.NOUN

for line in open("data.txt"):
    line = re.sub('[~`^=!@#$,\.\)\(\:\;?\-\+0-9%&*\/_\{\}\[\]<>\"]', ' ', line)
    line = re.sub('[\']', '', line)
    for word in line.split():
    	w = word.lower()
    	if w not in set(stop):
    		tag = nltk.pos_tag([w])[0][1]
    		w = wordnet_lemmatizer.lemmatize(w,pos=penn_to_wn(tag))
    		if len(w)!=1:
    			text.append(w)

for data in sorted(set(text)):
    print(data)
