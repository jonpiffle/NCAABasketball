from pybrain.datasets            import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer
from pybrain.tools.neuralnets	 import NNclassifier
from pybrain.tools.validation 	 import ModuleValidator

from pylab import ion, ioff, figure, draw, contourf, clf, show, hold, plot
from scipy import diag, arange, meshgrid, where
from numpy.random import multivariate_normal
from sklearn import preprocessing
import numpy

from models import *


games = Game.games_after_with_filter(3, rank_systems=("RPI", "SAG", "POM", "MOR",))

data = np.array([g.selected_features() for g in games], dtype=np.float)
labels = np.array([g.upset() for g in games])

non_nan_indices = ~np.isnan(data).any(axis=1)
data = data[non_nan_indices]
labels = labels[non_nan_indices]

data = preprocessing.scale(data)


alldata = ClassificationDataSet(len(data[0]))
for n in range(len(data)):
    alldata.addSample(data[n], labels[n])

tstdata, trndata = alldata.splitWithProportion(0.20)

trndata._convertToOneOfMany( )
#tstdata._convertToOneOfMany( )

fnn = buildNetwork(trndata.indim, 20, trndata.outdim, outclass=SoftmaxLayer )
trainer = BackpropTrainer( fnn, dataset=trndata, momentum=0.1, verbose=True, weightdecay=0.01)

for i in range(20):
	trainer.trainEpochs( 1 )
	trnresult = percentError( trainer.testOnClassData(), trndata['class'] )
	print "epoch: " + str(trainer.totalepochs) + "  train error: " + str(trnresult)

print ""
print "Predicting with the neural network"
answerlist = []
for row in tstdata:
	answer = numpy.argmax(fnn.activate(row[0]))
	answerlist.append(answer)
print answerlist
print [int(x[1][0]) for x in tstdata]
tstresult = percentError(answerlist, [x[1][0] for x in tstdata])
print "Test error: " + str(tstresult)