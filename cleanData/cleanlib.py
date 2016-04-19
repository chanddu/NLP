import re
from nltk.tokenize import word_tokenize

def getstopwords(filename):
    stopwords = []
    for sline in open(filename):
        for sword in sline.split():
            stopwords.append(sword)

    return stopwords

def clean_review(review,forFileWrite = False):
    sentiment = review[0] + ' '
    review = re.sub('[^A-Za-z\s]', '', review)
    rawtokens = word_tokenize(review)
    stopwords = getstopwords('/Users/chandu/Desktop/NLP/cleanData/stopwords.txt')
    wordList = []
    cleanReview = ''
    for rw in rawtokens:
        rw = rw.strip()
        if rw not in set(stopwords):
            if len(rw)>0:
                wordList.append(rw.lower())
                cleanReview = cleanReview + rw.lower() + ' '
    if forFileWrite:
        return sentiment+cleanReview+'\n'
    else:
        return wordList

