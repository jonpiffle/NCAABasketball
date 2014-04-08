from models import *
import sys
from sklearn.cross_validation import KFold
import numpy as np
import random
import code
from sklearn import svm, preprocessing, linear_model

class GreedyClassifier():
	def fit(self, train, train_labels):
		pass

	def predict(self, test):
		return np.array([False for _ in range(len(test))])


def fit(classifier, data_partitions):
	samples = []
	samples_correct = []
	for data_partition in data_partitions:
		clf = classifier
		clf.fit(data_partition[0], data_partition[1])

		y_pred = clf.predict(data_partition[2])
		samples.append(sum(np.fabs(y_pred-data_partition[3]))/float(len(y_pred)))

		print y_pred
		num_correct = 0
		for i in range(len(y_pred)):
			if (y_pred[i] < 0 and data_partition[4][i]) or (y_pred[1] >= 0 and not data_partition[4][i]):
				num_correct += 1
		samples_correct.append(float(num_correct)/float(len(y_pred)))

	print sum(samples_correct)/len(samples_correct)
	print sum(samples)/len(samples)

games = Game.games_after_with_filter(5, rank_systems=("RPI", "SAG", "POM", "MOR",))

print len(games)

data = np.array([g.selected_features() for g in games], dtype=np.float)
points_diff = np.array([g.points_diff() for g in games], dtype=np.float)
labels = np.array([g.upset() for g in games])

non_nan_indices = ~np.isnan(data).any(axis=1)
data = data[non_nan_indices]
points_diff = points_diff[non_nan_indices]
labels = labels[non_nan_indices]

kf = KFold(len(labels), n_folds=5, indices=True)
data_partitions = []
for train, test in kf:
	train_data = [data[i] for i in train]
	train_y = [points_diff[i] for i in train]
	test_data = [data[i] for i in test]
	test_y = [points_diff[i] for i in test]
	test_labels = [labels[i] for i in test]
	data_partitions.append((train_data, train_y, test_data, test_y, test_labels))

print "\nLinear Regression:"
fit(linear_model.LinearRegression(), data_partitions)

print "\nBayesian Regression:"
fit(linear_model.BayesianRidge(), data_partitions)
