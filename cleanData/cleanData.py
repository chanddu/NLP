from cleanlib import clean_review

def cleanData(i_file,o_file):
	try:
		f  = open(i_file,'r')
	except IOError:
		print("Unable to find training file\n\n")
		raise IOError

	cleanedReviews = ''
	for review in open(i_file):
		cleanedReviews += clean_review(review,True)

	f_o = open(o_file,'w')
	f_o.write(cleanedReviews)
	f.close()
	f_o.close()

def main():
    i_file     = 'data.txt'
    o_file    = 'datac.txt'
    cleanData(i_file,o_file)

if __name__ == "__main__":
	main()