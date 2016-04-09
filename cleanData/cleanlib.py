import nltk
import re

def getstopwords(filename):
    stopwords = []
    for sline in open(filename):
        for sword in sline.split():
            stopwords.append(sword)

    return stopwords

def clean_review(review):
    rawtokens = nltk.word_tokenize(review)
    stopwords = getstopwords('/Users/chandu/Desktop/NLP/cleanData/stopwords.txt')
    wordList = []
    for rw in rawtokens:
        rw = re.sub('[~`^=!@#$,\.\)\(\:\;?\-\+0-9%&*\/_\{\}\[\]<>\"]', ' ', rw)
        rw = re.sub('[\']', '', rw)
        rw = rw.strip()
        if rw not in set(stopwords):
            if len(rw)>1:
                wordList.append(rw.lower())
    return wordList

