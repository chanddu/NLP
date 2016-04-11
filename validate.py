import sys
import math
import numpy as np
from sklearn.cross_validation import KFold
from sklearn.metrics import accuracy_score
from NBtrainer import train
from cleanData.cleanlib import clean_review
from lib.getlib import getreviewNlabel,getVocab
from nltk import bigrams


def test_classfier(test_data,p_dict,n_dict,u_p,u_n,vocabulary):
    answer = []
    for line in test_data:
        wordList = clean_review(line)
        bigramList = list(bigrams(wordList))
        pplus = math.log10(0.5)
        pminus = math.log10(0.5)
        for word in bigramList:
            bigram = word
            word = word[0] + ' ' + word[1]
            if word in vocabulary:
                pminus = pminus + n_dict[word]
                pplus = pplus + p_dict[word]
            else:
                if bigram[0] in p_dict and bigram[1] in p_dict:
                    pplus = pplus + p_dict[bigram[0]] + p_dict[bigram[1]]
                    pminus = pminus + n_dict[bigram[0]] + n_dict[bigram[1]]
                elif bigram[0] in p_dict and bigram[1] not in p_dict:
                    pplus = pplus + p_dict[bigram[0]] + u_p
                    pminus = pminus + n_dict[bigram[0]] + u_n
                elif bigram[0] not in p_dict and bigram[1] in p_dict:
                    pplus = pplus + p_dict[bigram[1]] + u_p
                    pminus = pminus + n_dict[bigram[1]] + u_n
                else:
                    pplus = pplus + u_p + u_p
                    pminus = pminus + u_n + u_n
        if pplus>=pminus:
            answer.append('+')
        else:
            answer.append('-')
    return answer
    
def evaluate(data):
    vocabulary,vocab_len = getVocab('cleanData/vocabulary.txt')

    labels,reviews = getreviewNlabel('cleanData/data.txt')
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
        pos_dict,neg_dict,u_p,u_n = train(train_data,train_labels,vocabulary,vocab_len)
        result = test_classfier(test_data,pos_dict,neg_dict,u_p,u_n,vocabulary)
        a =  accuracy_score(test_labels,result)
        acc.append(a)

    print("accuracy=",np.mean(acc))
    print(acc)

def main():
    evaluate(sys.argv[1])

if __name__ == "__main__":
    main()

