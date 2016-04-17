import csv 
import math 
import numpy as np
import matplotlib.pyplot as mplot
import prettyplotlib as pplot


def Calculation_IDF(path_review,path_feature):
	reader_review = csv.reader(open(path_review))
	DF = {}
	for review in reader_review:
		for word in set(review):
			if word in DF:
				DF[word] = DF[word] + 1.0 
			else:
				DF[word] = 1.0

	reader_feature = csv.reader(open(path_feature))	
	IDF = {}
	for feature in reader_feature:
		IDF[feature[0]] = 0.0

	doc_num = 51312.0
	for token in DF:
		if token in IDF:
			IDF[token] = 1 + math.log(doc_num/float(DF[token]))

	return IDF

def TF_IDF(path_review,IDF):
	reader_review = csv.reader(open(path_review))
	TF_IDF = []
	for review in reader_review:
		TF_review = {}
		for token in review:
			if token in IDF:
				if token not in TF_review:
					TF_review[token] = 1.0
				else:
					TF_review[token] += 1.0 

		TF_IDF_review = {}
		for key in TF_review:
			TF_IDF_review[key] = (1.0 + math.log(TF_review[key]))*IDF[key]
		TF_IDF.append(TF_IDF_review)

	return TF_IDF 

def TF_IDF_product_info(path_review,IDF):
	TTF = {}
	reader_review = csv.reader(open(path_review))
	for review in reader_review:
		for token in review:
			if len(review)>200:
				if token in TTF:
					TTF[token] += 1.0
				else:
					TTF[token] = 1.0 
	TF_IDF_product = {}
	for key in TTF:
		if key in IDF:
			TF_IDF_product[key] = (1.0 + math.log(TTF[key]))*IDF[key]
	return TF_IDF_product 

def main():
	path_review = '/Users/Constance/Desktop/data_incubator/reviews_retoken.csv'
	path_feature = '/Users/Constance/Desktop/data_incubator/mutual_features.csv'
	IDF = Calculation_IDF(path_review,path_feature)
	TF_IDF_review = TF_IDF(path_review,IDF)

	path_product = '/Users/Constance/Desktop/data_incubator/product_info_retoken.csv'
	TF_IDF_product = TF_IDF_product_info(path_product,IDF)

	cosine_score = []
	for i in range(len(TF_IDF_review)):
		numerator = 0
		for token in TF_IDF_product:
			if token in TF_IDF_review[i]:
				numerator += TF_IDF_review[i][token]*TF_IDF_product[token]
		if numerator>0:
			denominator =np.sqrt(sum(np.asarray(TF_IDF_review[i].values())**2))
			score = numerator/denominator 
		else:
			score = 0.0
		cosine_score.append(score)
	
	pplot.plot(sorted(cosine_score,reverse=True))
	mplot.axvline(1000)
	mplot.xlabel("Reviews")
	mplot.ylabel("Cosine Score")
	mplot.title('Cosine Similarity Curve (without consider norm of product)')
	mplot.savefig('plot_cosine_score.png')

	with open('cosine_score.csv','w') as output:
		writer = csv.writer(output)
		for item in cosine_score:
			writer.writerow([item])

if __name__ == '__main__':
	main()