import nltk
import re
import sys
import math
import pickle
import os.path
import numpy as np
from sklearn.cross_validation import KFold
from sklearn.metrics import accuracy_score,f1_score,recall_score

poswords = []
negwords = []
stopwords = []
vocabulary = []

for sline in open("stopwords.txt"):
    for sword in sline.split():
        stopwords.append(sword)

for word in open('vocabulary.txt'):
    word = word.strip()
    vocabulary.append(word)
    #print(vocabulary)

def calculate_pos_cond_prob(word):
    return (poswords.count(word)+1)/(len(poswords) + len(set(poswords)))

def calculate_neg_cond_prob(word):
    return (negwords.count(word)+1)/(len(negwords) + len(set(negwords)))

def generate_words(line,list):
    rawtokens = nltk.word_tokenize(line)
    for rw in rawtokens:
        rw = re.sub('[~`^=!@#$,\.\)\(\:\;?\-\+0-9%&*\/_\{\}\[\]<>\"]', ' ', rw)
        rw = re.sub('[\']', '', rw)
        rw = rw.strip()
        if rw not in set(stopwords):
            if len(rw)>1:
                list.append(rw.lower())


def calculate_pos_probabilities():
    pos_probability_dictionary = {}
    for word in vocabulary:
        pos_probability_dictionary[word] = math.log10(calculate_pos_cond_prob(word))
    return pos_probability_dictionary

def calculate_neg_probabilities():
    neg_probability_dictionary = {}
    for word in vocabulary:
        neg_probability_dictionary[word] = math.log10(calculate_neg_cond_prob(word))
    return neg_probability_dictionary


def save_classifier(pos_prob_dict, neg_prob_dict):
    pos = open('pos_data.pickle', 'wb')
    neg = open('neg_data.pickle', 'wb')
    pickle.dump(pos_prob_dict, pos, pickle.HIGHEST_PROTOCOL)
    pickle.dump(neg_prob_dict, neg, pickle.HIGHEST_PROTOCOL)
    pos.close()
    neg.close()

def load_classifier(sentiment):
    f = open(sentiment, 'rb')
    classfier = pickle.load(f)
    f.close()
    return classfier

def separate_data_by_class(data,labels):
    for sample in zip(labels,data):
        sentiment,line = sample
        if sentiment == '+':
            generate_words(line,poswords)
        else:
            generate_words(line,negwords)


    #print("f_score=",np.mean(f_score))
    #print("recall=",np.mean(recall))

def train(train_data,train_labels):
    separate_data_by_class(train_data,train_labels)
    return calculate_pos_probabilities(),calculate_neg_probabilities()
    #print('check')

def predictor(pplus,pminus):
    wordList = re.sub("[^\w]", " ",  sys.argv[1]).split()
    regex = r'([+-])\s([\s\S]*)\n'
    reviews = []
    labels = []
    with open('data.txt') as f:
        for line in f:
            m = re.match(regex,line)
            labels.append(m.group(1))
            reviews.append(m.group(2))
    f.close()
    if not os.path.isfile('pos_data.pickle'):
        p_d,n_d = train(reviews,labels)
        save_classifier(p_d,n_d)

    p_di = load_classifier('pos_data.pickle')
    n_di = load_classifier('neg_data.pickle')
    separate_data_by_class(reviews,labels)
    for word in wordList:
        if word not in vocabulary:
            p = math.log10(calculate_pos_cond_prob(word))
            n = math.log10(calculate_neg_cond_prob(word))
        else:
            p = p_di[word]
            n = n_di[word]
        pplus = pplus + p
        pminus = pminus + n
    if pplus>=pminus:
        print('+')
    else:
        print('-')

def main():
    predictor(0,0)

if __name__ == "__main__":
    main()


