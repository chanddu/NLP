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

def calculate_pos_cond_prob(word):
    return (poswords.count(word)+1)/(len(poswords) + len(set(poswords)))

def calculate_neg_cond_prob(word):
    return (negwords.count(word)+1)/(len(negwords) + len(set(negwords)))

def generate_words(filename,list):
    text = []
    
    for line in open(filename):
        line = re.sub('[~`^=!@#$,\.\)\(\:\;?\-\+0-9%&*\/_\{\}\[\]<>\"]', ' ', line)
        line = re.sub('[\']', '', line)
        for word in line.split():
            w = word.lower()
            if w not in set(stop):
                if len(w)!=1:
                    list.append(w)


def classfier(pplus,pminus):
    wordList = re.sub("[^\w]", " ",  sys.argv[1]).split()
    for word in wordList:
        pplus = pplus + math.log10(calculate_pos_cond_prob(word))
        pminus = pminus + math.log10(calculate_neg_cond_prob(word))
    if pplus>=pminus:
        print('+')
    else:
        print('-')
            

generate_words('pos.txt',poswords)
generate_words('neg.txt',negwords)
classfier(0,0)
