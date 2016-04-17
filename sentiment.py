import csv 
import math 
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np

def feature(path_review_label,path_feature):
	reader_review_label = csv.reader(open(path_review_label))
	feature_count = {}
	for review in reader_review_label:
		label_index = len(review)
		for token in set(review[:label_index-1]):
			if token in feature_count:
				if int(review[label_index-1])==1:
					feature_count[token]["1"] +=1.0
				else:
					feature_count[token]['0'] +=1.0
			else:
				if int(review[label_index-1])==1:
					feature_count[token]={"1":1.0,"0":0.0}
				else:
					feature_count[token]={"1":0.0,"0":1.0}	

	reader_feature = csv.reader(open(path_feature))
	features = []
	for feature in reader_feature:
		features.append(feature[0])

	condition_DF = {}
	for word in feature_count:
		if word in features:
			condition_DF[word] = feature_count[word]
	return condition_DF

def smoothing(condition_DF,positive_doc_num,negative_doc_num):
	theta= 0.1 
	vocab_size = 4230
	naive_prob = {}
	for token in condition_DF:
		temp = {}
		temp["1"] = (condition_DF[token]["1"]+theta)/(positive_doc_num+theta*vocab_size)
		temp["0"] = (condition_DF[token]["0"]+theta)/(negative_doc_num+theta*vocab_size)
		temp["log_ratio"] = math.log(temp["1"]/temp["0"])
		naive_prob[token] = temp
	return naive_prob

def naive_bayes(naive_prob,positive_doc_num,negative_doc_num,path_review_label):
	predict_value = []
	labels = []
	prior = math.log(positive_doc_num/negative_doc_num)
	reader_review_label = csv.reader(open(path_review_label)) 
	for review in reader_review_label:
		label_index = len(review)
		label = int(review[label_index-1]) 
		condition_sum = 0
		for i in range(label_index-1):
			token = review[i]
			if token in naive_prob:
				condition_sum += math.log(naive_prob[token]["1"])-math.log(naive_prob[token]["0"])
		function_value = prior+condition_sum
		predict_value.append(function_value)
		labels.append(label)

	print 'finish label'

	predict_value,labels=zip(*sorted(zip(predict_value,labels)))

	return list(reversed(list(predict_value))),list(reversed(list(labels)))
	
def main():
	positive_doc_num = 29634
	negative_doc_num = 11110
	path_review = '/Users/Constance/Desktop/data_incubator/corpus_label.csv'
	path_feature = '/Users/Constance/Desktop/data_incubator/control_vocab.csv'

	condition_DF = feature(path_review,path_feature)
	print 'conditional df'

	naive_prob = smoothing(condition_DF,float(positive_doc_num),float(negative_doc_num))
	print 'naive prob'

	with open('/Users/Constance/Desktop/data_incubator/log_ratio.csv','w') as output:
		writer = csv.writer(output)
		for token in naive_prob:
			writer.writerow([token,naive_prob[token]['log_ratio']])

if __name__ == '__main__':
	main()	

