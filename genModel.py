import sys
import pickle

from NBtrainer import train
from cleanData.cleanlib import clean_review
from lib.getlib import getreviewNlabel,getVocab

def genModel():
	vocabulary,vocab_len = getVocab('cleanData/vocabulary.txt')
	labels,reviews = getreviewNlabel('cleanData/datac.txt')
	pos_dict,neg_dict,u_p,u_n = train(reviews,labels,vocabulary)
	t_m = pos_dict,neg_dict,u_p,u_n,vocabulary
	saveModel(t_m)

def saveModel(t_m):
	pickle.dump( t_m, open( "model/model.p", "wb" ) )

def main():
    genModel()

if __name__ == "__main__":
    main()