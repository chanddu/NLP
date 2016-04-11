import math
from cleanData.cleanlib import clean_review
from nltk import bigrams
from collections import Counter

def train(train_data,train_labels,vocabulary,vocab_len):
    poswords,negwords,posbigrams,negbigrams = separate_data_by_class(train_data,train_labels)
    pos_len = len(poswords)
    neg_len = len(negwords)
    unseen_pos_prob = math.log10(1/(pos_len+vocab_len))
    unseen_neg_prob = math.log10(1/(neg_len+vocab_len))
    poswords,negwords = changeUnigramCounts(Counter(poswords),Counter(negwords),Counter(posbigrams),Counter(negbigrams),vocabulary)
    pos_probabilities,neg_probabilities = calculate_probabilities(poswords,negwords,Counter(posbigrams),Counter(posbigrams),vocab_len,vocabulary
        ,pos_len,neg_len)
    return pos_probabilities,neg_probabilities,unseen_pos_prob,unseen_neg_prob

def calculate_pos_cond_prob(word,poswords,pos_len,vocab_len):
    return (poswords[word]+1)/(pos_len + vocab_len)

def calculate_neg_cond_prob(word,negwords,neg_len,vocab_len):
    return (negwords[word]+1)/(neg_len + vocab_len)

def cal_pos_bigram_cond_prob(word,posbigrams,pos_len,vocab_len):
    return (posbigrams[word]+1)/(pos_len + vocab_len)

def cal_neg_bigram_cond_prob(word,negbigrams,neg_len,vocab_len):
    return (negbigrams[word]+1)/(neg_len + vocab_len)

def calculate_probabilities(poswords,negwords,posbigrams,negbigrams,vocab_len,vocabulary,pos_len,neg_len):
    pos_probability_dictionary = {}
    neg_probability_dictionary = {}
    for word in vocabulary:
        if len(word.split())==1:
            pos_probability_dictionary[word] = math.log10(calculate_pos_cond_prob(word,poswords,pos_len,vocab_len))
            neg_probability_dictionary[word] = math.log10(calculate_neg_cond_prob(word,negwords,neg_len,vocab_len))
        else:
            pos_probability_dictionary[word] = math.log10(cal_pos_bigram_cond_prob(word,posbigrams,pos_len,vocab_len))
            neg_probability_dictionary[word] = math.log10(cal_neg_bigram_cond_prob(word,negbigrams,neg_len,vocab_len))
    return pos_probability_dictionary,neg_probability_dictionary

def genbigramList(b):
    blist = []
    for bigram in b:
        if b[bigram]>=3:
            blist.append(bigram[0] + ' ' + bigram[1])
    return blist
def changeUnigramCounts(poswords,negwords,posbigrams,negbigrams,vocabulary):
    for word in vocabulary:
        w = word.split()
        if len(w)!=1:
            poswords[w[0]] -= posbigrams[word]
            poswords[w[1]] -= posbigrams[word]
            negwords[w[0]] -= negwords[word]
            negwords[w[1]] -= negwords[word]
    return poswords,negwords

def separate_data_by_class(train_data,labels):
    poswords = []
    negwords = []
    posbigrams = []
    negbigrams = []
    for sample in zip(labels,train_data):
        sentiment,review = sample
        words = clean_review(review)
        bigramsList = list(bigrams(words))
        b = Counter(bigramsList)
        bgrams = genbigramList(b)
        if sentiment == '+':
            poswords = poswords + words
            posbigrams = posbigrams + bgrams
        else:
            negwords = negwords + words
            negbigrams = negbigrams + bgrams

    return poswords,negwords,posbigrams,negbigrams


