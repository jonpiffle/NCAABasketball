from models import *
from sklearn.cross_validation import KFold
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn import preprocessing, decomposition, linear_model
from sklearn.naive_bayes import GaussianNB
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from pybrain.datasets            import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer

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
		
	return float(sum(samples)/len(samples))

def regression_fit(classifier, data_partitions):
	samples = []
	samples_correct = []
	for data_partition in data_partitions:
		clf = classifier
		clf.fit(data_partition[0], data_partition[1])

		y_pred = clf.predict(data_partition[2])
		samples.append(sum(np.fabs(y_pred-data_partition[3]))/float(len(y_pred)))

		num_correct = 0
		for i in range(len(y_pred)):
			if (y_pred[i] < 0 and data_partition[4][i]) or (y_pred[1] >= 0 and not data_partition[4][i]):
				num_correct += 1
		samples_correct.append(float(num_correct)/float(len(y_pred)))

	return sum(samples_correct)/len(samples_correct)

correct = {
	"baseline": [],
	"naive_bayes": [],
	"decision_tree": [],
	"random_forest": [],
	"svm_rbf": [],
	"svm_linear": [],
	"regression": [],
	"neural_net": [],
}

step = 3
game_nums = range(3,31,step)
for n in game_nums:
	if n < 30:
		games = Game.games_between(n, n+step, rank_systems=("RPI", "SAG", "POM", "MOR",))
	else:
		games = Game.games_after_with_filter(n, rank_systems=("RPI", "SAG", "POM", "MOR",))
		n = 33

	print len(games)

	data = np.array([g.selected_features() for g in games], dtype=np.float)
	points_diff = np.array([g.points_diff() for g in games], dtype=np.float)
	labels = np.array([g.upset() for g in games])

	non_nan_indices = ~np.isnan(data).any(axis=1)
	data = data[non_nan_indices]
	labels = labels[non_nan_indices]
	points_diff = points_diff[non_nan_indices]

	data = preprocessing.scale(data)
	pca = decomposition.RandomizedPCA(whiten=True)
	pca.fit(data)

	kf = KFold(len(labels), n_folds=5, indices=True)
	data_partitions = []
	for train, test in kf:
		train_data = [data[i] for i in train]
		train_labels = [labels[i] for i in train]
		test_data = [data[i] for i in test]
		test_labels = [labels[i] for i in test]
		data_partitions.append((train_data, train_labels, test_data, test_labels))


	#Baseline
	pct_correct = fit(GreedyClassifier(), data_partitions)
	correct["baseline"].append((n, pct_correct))
	print "%s, %i, %f" % ("baseline", n, pct_correct)

	#Naive Bayes
	pca_data_partitions = []
	for data_partition in data_partitions:
		pca_data_partitions.append((pca.transform(data_partition[0]), data_partition[1], pca.transform(data_partition[2]), data_partition[3]))

	pct_correct = fit(GaussianNB(), pca_data_partitions)
	correct["naive_bayes"].append((n, pct_correct))
	print "%s, %i, %f" % ("naive_bayes", n, pct_correct)

	#Decision Tree Classifier
	pct_correct = fit(tree.DecisionTreeClassifier(max_depth=5, min_samples_leaf=5), data_partitions)
	correct["decision_tree"].append((n, pct_correct))
	print "%s, %i, %f" % ("decision_tree", n, pct_correct)

	#Random Forest Classifier
	pct_correct = fit(RandomForestClassifier(n_estimators=10), data_partitions)
	correct["random_forest"].append((n, pct_correct))
	print "%s, %i, %f" % ("random_forest", n, pct_correct)

	#Support Vector Machine rbf
	pct_correct = fit(svm.SVC(), data_partitions)
	correct["svm_rbf"].append((n, pct_correct))
	print "%s, %i, %f" % ("svm_rbf", n, pct_correct)

	#Support Vector Machine Linear Class
	pct_correct = fit(svm.LinearSVC(C=1.0, loss='l1'), data_partitions)
	correct["svm_linear"].append((n, pct_correct))
	print "%s, %i, %f" % ("svm_linear", n, pct_correct)

	#Linear Regression
	kf = KFold(len(labels), n_folds=5, indices=True)
	data_partitions = []
	for train, test in kf:
		train_data = [data[i] for i in train]
		train_y = [points_diff[i] for i in train]
		test_data = [data[i] for i in test]
		test_y = [points_diff[i] for i in test]
		test_labels = [labels[i] for i in test]
		data_partitions.append((train_data, train_y, test_data, test_y, test_labels))

	pct_correct = regression_fit(linear_model.LinearRegression(), data_partitions)
	correct["regression"].append((n, pct_correct))
	print "%s, %i, %f" % ("regression", n, pct_correct)

	
	#Neural Net Classifier
	alldata = ClassificationDataSet(len(data[0]))
	for j in range(len(data)):
	    alldata.addSample(data[j], labels[j])

	tstdata, trndata = alldata.splitWithProportion(0.20)
	trndata._convertToOneOfMany( )
	fnn = buildNetwork(trndata.indim, 20, trndata.outdim, outclass=SoftmaxLayer )
	trainer = BackpropTrainer( fnn, dataset=trndata, momentum=0.1, weightdecay=0.01)

	for i in range(20):
		trainer.trainEpochs( 1 )
		#trnresult = percentError( trainer.testOnClassData(), trndata['class'] )

	answerlist = []
	for row in tstdata:
		answer = np.argmax(fnn.activate(row[0]))
		answerlist.append(answer)

	pct_correct = (100 - percentError(answerlist, [x[1][0] for x in tstdata]))/100.0
	correct["neural_net"].append((n, pct_correct))
	print "%s, %i, %f" % ("neural_net", n, pct_correct)
	
print "Final accuracies: "
fig1 = plt.figure()
ax = fig1.add_subplot(1,1,1)
for label, pct_correct in correct.items():
	percentages = [x for (n,x) in pct_correct]
	print "%s, %f" % (label, sum(percentages)/float(len(pct_correct)))
	x,y = zip(*pct_correct)
	ax.plot(x, y, marker='o', label=label)

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels, loc='lower right')
plt.ylim((0,1))
plt.show()




