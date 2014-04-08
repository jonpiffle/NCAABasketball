from models import *
import matplotlib.pyplot as plt
import numpy as np
from sklearn import preprocessing

games = Game.games_after_with_filter(20, rank_systems=("RPI", "SAG", "POM", "MOR",))
print len(games)


data = np.array([g.attributes() for g in games], dtype=np.float)
labels = np.array([g.upset() for g in games])
normed_attributes = preprocessing.normalize(data, norm='l2')


hist, bins = np.histogram(normed_attributes, bins=1000)
center = (bins[:-1] + bins[1:]) / 2
plt.bar(center, hist, align='center')
plt.show()