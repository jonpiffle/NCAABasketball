from pybrain.datasets            import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer

from pylab import ion, ioff, figure, draw, contourf, clf, show, hold, plot
from scipy import diag, arange, meshgrid, where
from numpy.random import multivariate_normal
from sklearn import preprocessing

from models import *


games = Game.games_after_with_filter(30, rank_systems=("RPI", "SAG", "POM", "MOR",))

print len(games)

data = np.array([g.selected_features() for g in games], dtype=np.float)
labels = np.array([g.upset() for g in games])

non_nan_indices = ~np.isnan(data).any(axis=1)
data = data[non_nan_indices]
labels = labels[non_nan_indices]

data = preprocessing.scale(data)


alldata = ClassificationDataSet(len(data[0]))
for n in range(len(data)):
    alldata.addSample(data[n], labels[n])

tstdata, trndata = alldata.splitWithProportion( 0.25 )

trndata._convertToOneOfMany( )
tstdata._convertToOneOfMany( )

fnn = buildNetwork( trndata.indim, 5, trndata.outdim, outclass=SoftmaxLayer )
trainer = BackpropTrainer( fnn, dataset=trndata, momentum=0.1, verbose=True, weightdecay=0.01)

for i in range(20):
	trainer.trainEpochs( 5 )

	trnresult = percentError( trainer.testOnClassData(), trndata['class'] )
	tstresult = percentError( trainer.testOnClassData( dataset=tstdata ), tstdata['class'] )
	print "epoch: %4d" % trainer.totalepochs, \
          "  train error: %5.2f%%" % trnresult, \
          "  test error: %5.2f%%" % tstresult

	print trainer.testOnClassData( dataset=tstdata )