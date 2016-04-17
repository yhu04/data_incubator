import json 
import nltk 
import os 
import string
import re  
import sys
import numpy as np
import csv 

def JsonToDict(path): 
	reviews = []
	titles = []
	product_info = []
	labels = []
	# iterate all json files in the folder 
	for root, dirs, files in os.walk(path):
		for name in files:
			path_name = os.path.join(root,name)
			user_review = json.loads(open(path_name).read())
			user_review_content = user_review['Reviews']
			if user_review['ProductInfo']['Features'] is not None:
				product_info.append(user_review['ProductInfo']['Features'])
			for review in user_review_content:
				if review['Title'] is not None and review['Content'] is not None:
					titles.append(review['Title'])
					reviews.append(review['Content'])
					if float(review['Overall'])>=4:
						labels.append(1)
					else:
						labels.append(0)
	print 'Finish Parsing Json'
	return reviews,titles,labels,product_info
	
def StopWord(filename):
	stop_words = []
	stemmer = nltk.stem.snowball.EnglishStemmer()
	for line in open(filename,'r'):
		stop_words.append(stemmer.stem(Normalization(line.strip('\n'))))
	return list(set(stop_words))

def Normalization(token):
	punctuation = '[!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]'
	if re.match(punctuation,token) is not None:
		token = ""
	token = token.lower()
	if re.match('[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?',token) is not None or re.match('^-?[0-9]+$',token) is not None or re.match('^-?[0-9]+\,[0-9]+$',token):
		token = 'NUM'
	return token 
	
def preprocess(text_list,stop_words):
	token_text = []
	tokenizer = nltk.tokenize.treebank.TreebankWordTokenizer()  
	stemmer = nltk.stem.snowball.EnglishStemmer()
	for review in text_list:
		temp = []
		for token in tokenizer.tokenize(review):
			new_token = stemmer.stem(Normalization(token))
			if new_token in stop_words:
				pass 
			else:
				if new_token == "" or new_token == "NUM":
					pass
				else:
					temp.append(new_token.encode('utf-8'))
		token_text.append(temp)
	return token_text

def merge_text(titles_token,reviews_token):
	for i in range(len(titles_token)):
		reviews_token[i].extend(titles_token[i])
	return reviews_token

def main():
	path = '/Users/Constance/desktop/data_incubator/AmazonReviews/laptops'
	reviews,titles,labels,product_info = JsonToDict(path)
	print 'Json to List'

	with open('/Users/Constance/desktop/data_incubator/labels.csv','w') as output_label:
		writer_label = csv.writer(output_label)
		for label in labels:
			writer_label.writerow([label])
	print 'save label'

	stop_words = StopWord('/Users/Constance/Desktop/Spring2016/text_mining/MP2/stop_word.txt')
	print "StopWord"

	reviews_token = preprocess(reviews,stop_words)
	print 'Finish Reviews Token'

	titles_token = preprocess(titles,stop_words)
	print 'Finish Titles Token'

	total_token = merge_text(titles_token,reviews_token)

	with open('/Users/Constance/desktop/data_incubator/reviews.csv','w') as output_review:
		writer_review = csv.writer(output_review)
		writer_review.writerows(total_token)
	print 'Save User Info'

	product_info_token = preprocess(product_info,stop_words)
	print 'Finish Product Info Token'

	with open('/Users/Constance/desktop/data_incubator/product_info.csv','w') as output_product:
		writer_review = csv.writer(output_product)
		writer_review.writerows(product_info_token)
	print 'Save Product Info'

if __name__ == '__main__':
	main()

