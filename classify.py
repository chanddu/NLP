import pickle
import sys

from validate import test_classfier
from genModel import genModel

def classify(test_data):
	pos_dict,neg_dict,u_p,u_n,vocabulary = pickle.load(open('model/model.p','rb'))
	print(test_classfier(test_data,pos_dict,neg_dict,u_p,u_n,vocabulary))

def error_check():
	try:
		f = open('model/model.p','rb')
	except IOError:
		print('No model found and a new one will be generated')
		genModel()

def main():
    test_data = []
    error_check()
    review = input('Enter a review:')
    test_data.append(review)
    classify(test_data)

if __name__ == "__main__":
    main()


