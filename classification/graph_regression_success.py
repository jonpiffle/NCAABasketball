from models import *
from sklearn.cross_validation import KFold
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm, preprocessing, linear_model, decomposition

def fit(classifier, data_partitions):
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

correct = []
step = 3
game_nums = range(15,30,step)
for n in game_nums:
	games = Game.games_between(n, n+step, rank_systems=("RPI", "SAG", "POM", "MOR",))

	print len(games)

	data = np.array([g.selected_features() for g in games], dtype=np.float)
	points_diff = np.array([g.points_diff() for g in games], dtype=np.float)
	labels = np.array([g.upset() for g in games])

	non_nan_indices = ~np.isnan(data).any(axis=1)
	data = data[non_nan_indices]
	points_diff = points_diff[non_nan_indices]
	labels = labels[non_nan_indices]

	data = preprocessing.scale(data)

	kf = KFold(len(labels), n_folds=5, indices=True)
	data_partitions = []
	for train, test in kf:
		train_data = [data[i] for i in train]
		train_y = [points_diff[i] for i in train]
		test_data = [data[i] for i in test]
		test_y = [points_diff[i] for i in test]
		test_labels = [labels[i] for i in test]
		data_partitions.append((train_data, train_y, test_data, test_y, test_labels))

	pct_correct = fit(linear_model.LinearRegression(), data_partitions)
	correct.append((n, pct_correct))
	print "%i, %f" % (n, pct_correct)

x,y = zip(*correct)
plt.plot(x, y,'bo-')
plt.ylim((0,1))
plt.show()




