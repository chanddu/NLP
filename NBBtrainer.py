import math
from nltk import bigrams
from collections import Counter

def train(train_data,train_labels,vocabulary,vocab_len):
    poswords,negwords,posbigrams,negbigrams = separate_data_by_class(train_data,train_labels,vocabulary)
    pos_len = len(poswords)
    neg_len = len(negwords)
    unseen_pos_prob = math.log10(1/(pos_len+vocab_len))
    unseen_neg_prob = math.log10(1/(neg_len+vocab_len))
    #poswords,negwords = changeUnigramCounts(Counter(poswords),Counter(negwords),Counter(posbigrams),Counter(negbigrams),vocabulary)
    pos_probabilities,neg_probabilities = calculate_probabilities(Counter(poswords),Counter(negwords),posbigrams,negbigrams,vocab_len,vocabulary
        ,pos_len,neg_len)
    return pos_probabilities,neg_probabilities,unseen_pos_prob,unseen_neg_prob

def calculate_pos_cond_prob(word,poswords,pos_len,vocab_len):
    return (poswords[word]+1)/(pos_len + vocab_len)

def calculate_neg_cond_prob(word,negwords,neg_len,vocab_len):
    return (negwords[word]+1)/(neg_len + vocab_len)

def cal_pos_bigram_cond_prob(word,posbigrams,poswords,vocab_len):
    return (posbigrams.count(word)+1)/(poswords[word.split()[0]] - posbigrams.count(word) + vocab_len)

def cal_neg_bigram_cond_prob(word,negbigrams,negwords,vocab_len):
    return (negbigrams.count(word)+1)/(negwords[word.split()[0]] - negbigrams.count(word) + vocab_len)

def calculate_probabilities(poswords,negwords,posbigrams,negbigrams,vocab_len,vocabulary,pos_len,neg_len):
    pos_probability_dictionary = {}
    neg_probability_dictionary = {}
    for word in vocabulary:
        if len(word.split())==1:
            #print(calculate_pos_cond_prob(word,poswords,pos_len,vocab_len))
            pos_probability_dictionary[word] = math.log10(calculate_pos_cond_prob(word,poswords,pos_len,vocab_len))
            neg_probability_dictionary[word] = math.log10(calculate_neg_cond_prob(word,negwords,neg_len,vocab_len))
        else:
            pos_probability_dictionary[word] = math.log10(cal_pos_bigram_cond_prob(word,posbigrams,poswords,vocab_len))
            neg_probability_dictionary[word] = math.log10(cal_neg_bigram_cond_prob(word,negbigrams,negwords,vocab_len))
    return pos_probability_dictionary,neg_probability_dictionary


def genbigramList(b):
    blist = []
    for bigram in b:
        blist.append(bigram[0] + ' ' + bigram[1])
    return blist

'''def genbigramNuniGramList(bigramsList,words,vocabulary,sentiment):
    poswords = []
    negwords = []
    posbigrams = []
    negbigrams = []
    bigram_size = 0
    for b in bigramsList:
        bigram_size+=1
    if(bigram_size>=1):
        for i in range(0,bigram_size-1):
            bigram1 = bigramsList[i]
            word1 = bigram1[0] + ' ' + bigram1[1]
            bigram2 = bigramsList[i+1]
            word2 = bigram2[0] + ' ' + bigram2[1]
            if word1 not in vocabulary and word2 not in vocabulary:
                if sentiment == '+':
                    poswords.append(bigram1[1])
                else:
                    negwords.append(bigram1[1])
            if sentiment == '+':
                posbigrams.append(word1)
            else:
                negbigrams.append(word1)

        if sentiment == '+':
            posbigrams.append(bigramsList[bigram_size-1][0] + ' ' + bigramsList[bigram_size-1][1])
        else:
            negbigrams.append(bigramsList[bigram_size-1][0] + ' ' + bigramsList[bigram_size-1][1])
    return poswords,negwords,posbigrams,negbigrams'''

'''def separate_data_by_class(train_data,labels,vocabulary):
    poswords = []
    negwords = []
    posbigrams = []
    negbigrams = []
    for sample in zip(labels,train_data):
        words = []
        sentiment,review = sample
        words.append('*')
        words += review.split()
        bigramsList = list(bigrams(words))
        p_words,n_words,p_bigrams,n_bigrams = genbigramNuniGramList(bigramsList,words,vocabulary,sentiment)
        if sentiment == '+':
            poswords = poswords + p_words
            posbigrams = posbigrams + p_bigrams
        else:
            negwords = negwords + n_words
            negbigrams = negbigrams + n_bigrams

    return poswords,negwords,posbigrams,negbigrams'''

def separate_data_by_class(train_data,labels,vocabulary):
    poswords = []
    negwords = []
    posbigrams = []
    negbigrams = []
    for sample in zip(labels,train_data):
        #words = []
        sentiment,review = sample
        #words.append('*')
        words = review.split()
        bigramsList = list(bigrams(words))
        bgrams = genbigramList(bigramsList)
        if sentiment == '+':
            poswords = poswords + words
            posbigrams = posbigrams + bgrams
        else:
            negwords = negwords + words
            negbigrams = negbigrams + bgrams

    return poswords,negwords,posbigrams,negbigrams
