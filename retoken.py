import nltk 
import os 
import string
import re  
import sys
import numpy as np
import csv

def Normalization(token):
	punctuation = '[!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]'
	if re.match(punctuation,token) is not None:
		token = ""
	token = token.lower()
	if re.match('[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?',token) is not None or re.match('^-?[0-9]+$',token) is not None or re.match('^-?[0-9]+\,[0-9]+$',token):
		token = 'NUM'
	return token 

def StemReview(token):
	stemmer = nltk.stem.snowball.EnglishStemmer()
	word = stemmer.stem(token)
	return word

def StopWord(filename):
	stop_words = []
	stemmer = nltk.stem.snowball.EnglishStemmer()
	for line in open(filename,'r'):
		stop_words.append(stemmer.stem(Normalization(line.strip('\n'))))
	return list(set(stop_words))

def Re_Token(review_readers,stop_words):
	re_token_documents = []
	for document in review_readers:
		temp=[]
		for word in document:
			if re.match('[a-zA-Z]+\|[a-zA-Z]+|[a-zA-Z]+\||\|[a-zA-Z]+', word) is not None:
				re_token_list = word.split("|")
				for re_token in re_token_list:
					if re_token not in stop_words:
						if StemReview(re_token) == "" or StemReview(re_token) =='NUM' or StemReview(re_token) =='num':
							pass
						else:
							temp.append(StemReview(re_token).encode('utf-8'))
					else:
						pass
			else:
				if word == "" or word == "NUM" or word =='num':
					pass
				else:
					temp.append(word.encode('utf-8'))
		re_token_documents.append(temp)
	return re_token_documents

def main():	
	reload(sys)
	sys.setdefaultencoding("utf-8")
	stop_words = StopWord('/Users/Constance/Desktop/Spring2016/text_mining/MP2/stop_word.txt')
	print "StopWord"

	path = '/Users/Constance/desktop/data_incubator/product_info.csv'
	review_reader = csv.reader(open(path))
	re_token_documents = Re_Token(review_reader,stop_words)

	with open('/Users/Constance/desktop/data_incubator/product_info_retoken.csv','w') as output_review:
		writer_review = csv.writer(output_review)
		writer_review.writerows(re_token_documents)	

if __name__ == '__main__':
	main()

