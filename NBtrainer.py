import math
from cleanData.cleanlib import clean_review

def train(train_data,train_labels,vocabulary):
    poswords,negwords = separate_data_by_class(train_data,train_labels)
    vocab_len = len(vocabulary)
    unseen_pos_prob = 1/(len(poswords)+vocab_len)
    unseen_neg_prob = 1/(len(negwords)+vocab_len)
    pos_probabilities,neg_probabilities = calculate_probabilities(poswords,negwords,vocab_len,vocabulary)
    return pos_probabilities,neg_probabilities,unseen_pos_prob,unseen_neg_prob

def calculate_pos_cond_prob(word,poswords,vocab_len):
    return (poswords.count(word)+1)/(len(poswords) + vocab_len)

def calculate_neg_cond_prob(word,negwords,vocab_len):
    return (negwords.count(word)+1)/(len(negwords) + vocab_len)


def calculate_probabilities(poswords,negwords,vocab_len,vocabulary):
    pos_probability_dictionary = {}
    neg_probability_dictionary = {}
    for word in vocabulary:
        pos_probability_dictionary[word] = math.log10(calculate_pos_cond_prob(word,poswords,vocab_len))
        neg_probability_dictionary[word] = math.log10(calculate_neg_cond_prob(word,negwords,vocab_len))
    return pos_probability_dictionary,neg_probability_dictionary


def separate_data_by_class(train_data,labels):
    poswords = []
    negwords = []
    for sample in zip(labels,train_data):
        sentiment,review = sample
        if sentiment == '+':
            poswords = poswords + clean_review(review)
        else:
            negwords = negwords + clean_review(review)

    return poswords,negwords


