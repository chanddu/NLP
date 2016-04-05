import nltk
import re
import sys
import math
import pickle
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


def test_classfier(pplus,pminus,test_data):
    answer = []
    for line in test_data:
        rawtokens = nltk.word_tokenize(line)
        wordList = []
        pplus = 0
        pminus = 0
        for rw in rawtokens:
            rw = re.sub('[~`^=!@#$,\.\)\(\:\;?\-\+0-9%&*\/_\{\}\[\]<>\"]', ' ', rw)
            rw = re.sub('[\']', '', rw)
            rw = rw.strip()
            if rw not in set(stopwords):
                if len(rw)>1:
                    wordList.append(rw.lower())
        pos_dict = load_classifier('pos_data.pickle')
        neg_dict = load_classifier('neg_data.pickle')
        for word in wordList:
            pplus = pplus + pos_dict[word]
            pminus = pminus + neg_dict[word]
        if pplus>=pminus:
            answer.append('1')
        else:
            answer.append('0')
    #print(answer)
    return answer

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
        if sentiment == '1':
            generate_words(line,poswords)
        else:
            generate_words(line,negwords)

def evaluate(data):
    regex = r'(.+)\s([0,1])\n?'
    reviews = []
    labels = []
    with open(sys.argv[1]) as f:
        for line in f:
            m = re.match(regex,line)
            labels.append(m.group(2))
            reviews.append(m.group(1))

    X = np.array(reviews)
    y = np.array(labels)

    kf = KFold(1000,n_folds=10)
    train_data = []
    test_data = []
    test_labels = []

    k = 0
    acc = []
    for train_index, test_index in kf:
        train_data,train_labels = X[train_index], y[train_index]
        test_data, test_labels = X[test_index],y[test_index]
        train(train_data,train_labels)
        result = test(test_data)
        #print(test_labels)
        a =  accuracy_score(test_labels,result)
        acc.append(a)
        #f_score.append(f)
        #recall.append(r)

    print("accuracy=",np.mean(acc))
    #print("f_score=",np.mean(f_score))
    #print("recall=",np.mean(recall))

def train(train_data,train_labels):
    separate_data_by_class(train_data,train_labels)
    save_classifier(calculate_pos_probabilities(), calculate_neg_probabilities())
    #print('check')

def test(test_data):
    result = test_classfier(0,0,test_data)
    return result

evaluate('data.txt')