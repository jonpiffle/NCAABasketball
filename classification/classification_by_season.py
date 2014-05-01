from models import *
import sys
from sklearn.cross_validation import KFold
import numpy as np
import random
import code
from sklearn import svm
from sklearn.naive_bayes import GaussianNB
from sklearn import tree
import pydot
from StringIO import StringIO
from sklearn import preprocessing
from sklearn import decomposition
from sklearn import neighbors
from sklearn.lda import LDA
from sklearn.ensemble import RandomForestClassifier


class GreedyClassifier():
	def fit(self, train, train_labels):
		pass

	def predict(self, test):
		return np.array([False for _ in range(len(test))])


def fit(classifier, data_partitions):
	samples = []
	for data_partition in data_partitions:
		clf = classifier
		clf.fit(data_partition[0], data_partition[1])

		y_pred = clf.predict(data_partition[2])
		samples.append((float((data_partition[3] == y_pred).sum())/len(data_partition[3])))
		
	print "Correct: %f" % float(sum(samples)/len(samples))

games = Game.games_after_with_filter(19, rank_systems=("RPI", "SAG", "POM", "MOR",))

print len(games)

data = np.array([g.attributes() for g in games], dtype=np.float)
labels = np.array([g.upset() for g in games])
years = np.array([g.year for g in games], dtype=np.integer)

non_nan_indices = ~np.isnan(data).any(axis=1)
data = data[non_nan_indices]
labels = labels[non_nan_indices]
years = years[non_nan_indices]

data = preprocessing.scale(data)
#pca = decomposition.RandomizedPCA(whiten=True)
#data = pca.fit_transform(data)


"""
INSERT PARTITION LOGIC HERE
"""


print "\nAlways Pick Favorite:"
fit(GreedyClassifier(), data_partitions)

print "\nNaive Bayes: "
fit(GaussianNB(), data_partitions)

print "\nDecision Tree Classifier:"
fit(tree.DecisionTreeClassifier(max_depth=5, min_samples_leaf=5), data_partitions)

print "\nRandom Forest Classifier"
fit(RandomForestClassifier(n_estimators=10), data_partitions)

print "\nSupport Vector Machine rbf:"
fit(svm.SVC(), data_partitions)

print "\nSupport Vector Machine Linear Class:"
fit(svm.LinearSVC(C=1.0, loss='l1'), data_partitions)

