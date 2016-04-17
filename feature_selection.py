import csv 
import math 

def IDF_calculation(path):
	DF_vocab = {}
	reader_doc = csv.reader(open(path))
	for review in reader_doc:
		for token in set(review):
			if token in DF_vocab:
				DF_vocab[token] += 1.0
			else:
				DF_vocab[token] = 1.0

	IDF = {}
	doc_num = float(40744)
	for word in DF_vocab:
		#if DF_vocab[word]>50:
		IDF[word]=1 + math.log(doc_num/float(DF_vocab[word]))

	DF = {}
	for word in DF_vocab:
		if DF_vocab[word]>50:
			DF[word] = DF_vocab
	print "DF Calculation"
	return IDF,DF

def matrix(path,label,DF):
	# basic
	total_doc = len(label)
	positive_doc = sum(label)
	negative_doc = total_doc - positive_doc

	con_matrix = {}
	reader_review = csv.reader(open(path))
	for review in reader_review:
		label = int(review[len(review)-1])
		for token in set(review[:len(review)-1]):
			if token in DF:
				if token in con_matrix:
					if label == 0:
						con_matrix[token]["negative"] = con_matrix[token]["negative"] + 1.0
					else:
						con_matrix[token]['positive'] = con_matrix[token]['positive'] + 1.0
				else:
					if label == 0:
						con_matrix[token] = {"positive":0.0,"negative":1.0}
					else:
						con_matrix[token] = {"positive":1.0,"negative":0.0}

	return con_matrix,total_doc,negative_doc,positive_doc

def InfoGain(con_matrix,total_doc,positive_doc,negative_doc):
	info_gain = {}
	entropy_Y = (positive_doc/total_doc)*math.log(positive_doc/total_doc)+(negative_doc/total_doc)*math.log(negative_doc/total_doc)
	i = 0 
	for word in con_matrix:
		p_positive_t = con_matrix[word]['positive']/(con_matrix[word]['positive']+con_matrix[word]['negative'])
		p_negative_t = con_matrix[word]['negative']/(con_matrix[word]['positive']+con_matrix[word]['negative'])
		entropy_t = p_positive_t*math.log(p_positive_t)+p_negative_t*math.log(p_negative_t)

		p_positive_not_t = (positive_doc-con_matrix[word]['positive'])/((positive_doc-con_matrix[word]['positive'])+(negative_doc-con_matrix[word]['negative']))
		p_negative_not_t = (negative_doc-con_matrix[word]['negative'])/((positive_doc-con_matrix[word]['positive'])+(negative_doc-con_matrix[word]['negative']))
		entropy_not_t = p_positive_not_t*math.log(p_positive_not_t) + p_negative_not_t*math.log(p_negative_not_t)

		p_t = (con_matrix[word]['positive']+con_matrix[word]['negative'])/total_doc
		p_not_t = ((positive_doc-con_matrix[word]['positive'])+(negative_doc-con_matrix[word]['negative']))/total_doc

		infogain = -entropy_Y + p_t*entropy_t + p_not_t*entropy_not_t
		info_gain[word] = infogain

	InfoGainFeature = sorted(info_gain.keys(), key=info_gain.__getitem__)
	print InfoGainFeature[-50:]
	return InfoGainFeature

def ChiSquare(con_matrix,positive_doc,negative_doc):
	chisquare = {}
	for word in con_matrix:
		A = con_matrix[word]['positive']
		B = float(positive_doc) - A
		C = con_matrix[word]['negative']
		D = float(negative_doc) - C
		temp = (A+B+C+D)*((A*D-B*C)**2)/((A+C)*(B+D)*(A+B)*(C+D))
		threshod = 3.841
		if temp > threshod:
			chisquare[word] = temp

	ChiqSquareFeature = sorted(chisquare.keys(), key=chisquare.__getitem__)
	print ChiqSquareFeature[-50:]
	return ChiqSquareFeature

def similar_feature(path_review_features,IDF):
	mutual_feature = {}
	review_reader = csv.reader(open(path_review_features))
	for feature in review_reader:
		if feature[0] in IDF:
			mutual_feature[feature[0]]=IDF[feature[0]]
	return mutual_feature


def main():
	# find initial vocab 
	path_product = '/Users/Constance/desktop/data_incubator/product_info_retoken.csv'
	IDF,DF = IDF_calculation(path_product)

	# import label
	path_label = '/Users/Constance/desktop/data_incubator/labels.csv'
	label_reader = csv.reader(open(path_label))
	labels = []
	for label in label_reader:
		labels.append(int(label[0]))

	# read labels
	path_reviews_label = '/Users/Constance/Desktop/data_incubator/corpus_label.csv'
	con_matrix,total_doc,negative_doc,positive_doc = matrix(path_reviews_label,labels,DF)

	# ChiSquare 
	ChiqSquareFeature = ChiSquare(con_matrix,positive_doc,negative_doc)

	# Information Gain
	InfoGainFeature = InfoGain(con_matrix,float(total_doc),float(positive_doc),float(negative_doc))

	# combine 
	control_vocab = list(set(ChiqSquareFeature+InfoGainFeature))
	print len(control_vocab)

	with open('/Users/Constance/Desktop/data_incubator/control_vocab.csv','w') as output:
		writer = csv.writer(output)
		for feature in control_vocab:
			writer.writerow([feature])

	path_product = '/Users/Constance/desktop/data_incubator/product_info_retoken.csv'
	IDF = IDF_calculation(path_product)
	features = IDF.keys()
	idf_value = IDF.values()
	idf_value,features=zip(*sorted(zip(idf_value,features)))
	with open('/Users/Constance/Desktop/data_incubator/product_features.csv','w') as output:
		writer = csv.writer(output)
		for i in range(len(idf_value)):
			writer.writerow([features[i],idf_value[i]])

	path_review_features = '/Users/Constance/Desktop/data_incubator/control_vocab.csv'
	mutual_features = similar_feature(path_review_features,IDF)
	with open('/Users/Constance/Desktop/data_incubator/mutal_features.csv','w') as output_mutual:
		writer = csv.writer(output_mutual)
		for key in mutual_features:
			print key, mutual_features[key]
			writer.writerow([key,mutual_features[key]])	

if __name__ == '__main__':
	main()
