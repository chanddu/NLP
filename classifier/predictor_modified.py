from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
import nltk
import re
import sys
import math

poswords = []
negwords = []
stop = stopwords.words('english')
wordnet_lemmatizer = WordNetLemmatizer()

def calculate_pos_cond_prob(word):
    return (poswords.count(word)+1)/(len(poswords) + len(set(poswords)))

def calculate_neg_cond_prob(word):
    return (negwords.count(word)+1)/(len(negwords) + len(set(negwords)))

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

def generate_words(filename,list):
    text = []
    
    for line in open(filename):
        line = re.sub('[~`^=!@#$,\.\)\(\:\;?\-\+0-9%&*\/_\{\}\[\]<>\"]', ' ', line)
        line = re.sub('[\']', '', line)
        for word in line.split():
            w = word.lower()
            if w not in set(stop):
                tag = nltk.pos_tag([w])[0][1]
                w = wordnet_lemmatizer.lemmatize(w,pos=penn_to_wn(tag))
                if len(w)!=1:
                    list.append(w)


def classfier(pplus,pminus):
    #wordList = re.sub("[^\w]", " ",  sys.argv[1]).split()
    testlist = []
    
    i=1;
    for line in open(sys.argv[1]):
        line = re.sub('[~`^=!@#$,\.\)\(\:\;?\-\+0-9%&*\/_\{\}\[\]<>\"]', ' ', line)
        line = re.sub('[\']', '', line)
        for word in line.split():
            w = word.lower()
            if w not in set(stop):
                tag = nltk.pos_tag([w])[0][1]
                w = wordnet_lemmatizer.lemmatize(w,pos=penn_to_wn(tag))
                if len(w)!=1:
                    testlist.append(w)
        for word in testlist:
            pplus = pplus + math.log10(calculate_pos_cond_prob(word))
            pminus = pminus + math.log10(calculate_neg_cond_prob(word))
        if pplus>=pminus:
            print(str(i) + ' +')
            i = i+1
        else:
            print(str(i) + ' -')
            i = i+1

generate_words('pos.txt',poswords)
generate_words('neg.txt',negwords)
classfier(0,0)
