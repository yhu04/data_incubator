import csv 
import numpy as np 


def main():
	path_review = '/Users/Constance/desktop/data_incubator/reviews_retoken.csv' 
	reader_review = csv.reader(open(path_review))
	reviews = []
	for review in reader_review:
		reviews.append(review)

	path_label = '/Users/Constance/desktop/data_incubator/labels.csv'
	reader_label = csv.reader(open(path_label))
	labels = []
	for label in reader_label:
		labels.append(label)

	with open('/Users/Constance/Desktop/data_incubator/corpus_label.csv','w') as output:
		writer = csv.writer(output)
		for i in range(len(labels)):
			reviews[i].extend(labels[i])
			writer.writerow(reviews[i])

if __name__ == '__main__':
	main()


