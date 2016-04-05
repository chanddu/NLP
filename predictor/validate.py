import nltk
import re
import sys
import math
import pickle
import numpy as np
from sklearn.cross_validation import KFold
from sklearn.metrics import accuracy_score,f1_score,recall_score
from classifier import train,calculate_pos_cond_prob,calculate_neg_cond_prob

stopwords = []
vocabulary = []

for sline in open("stopwords.txt"):
    for sword in sline.split():
        stopwords.append(sword)

for word in open('vocabulary.txt'):
    word = word.strip()
    vocabulary.append(word)

def test_classfier(pplus,pminus,test_data,p_dict,n_dict):
    answer = []
    for line in test_data:
        rawtokens = nltk.word_tokenize(line)
        wordList = []
        pplus = 0
        pminus = 0
        p=0
        n=0
        for rw in rawtokens:
            rw = re.sub('[~`^=!@#$,\.\)\(\:\;?\-\+0-9%&*\/_\{\}\[\]<>\"]', ' ', rw)
            rw = re.sub('[\']', '', rw)
            rw = rw.strip()
            if rw not in set(stopwords):
                if len(rw)>1:
                    wordList.append(rw.lower())
        for word in wordList:
            if word not in vocabulary:
                p = math.log10(calculate_pos_cond_prob(word))
                n = math.log10(calculate_neg_cond_prob(word))
            else:
                p = p_dict[word]
                n = n_dict[word]
            pplus = pplus + p
            pminus = pminus + n 
        if pplus>=pminus:
            answer.append('+')
        else:
            answer.append('-')
    #print(answer)
    return answer
    
def evaluate(data):
    regex = r'([+-])\s([\s\S]*)\n'
    reviews = []
    labels = []
    with open(sys.argv[1]) as f:
        for line in f:
            m = re.match(regex,line)
            labels.append(m.group(1))
            reviews.append(m.group(2))

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
        pos_dict,neg_dict = train(train_data,train_labels)
        result = test(test_data,pos_dict,neg_dict)
        #print(test_labels)
        a =  accuracy_score(test_labels,result)
        acc.append(a)

    print("accuracy=",np.mean(acc))
    print(acc)

def test(test_data,p_dict,n_dict):
    result = test_classfier(0,0,test_data,p_dict,n_dict)
    return result

evaluate(sys.argv[1])