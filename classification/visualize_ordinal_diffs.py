from models import *
import matplotlib.pyplot as plt
import numpy as np
from sklearn import preprocessing

games = Game.games_after_with_filter(20, rank_systems=("RPI", "SAG", "POM", "MOR",))
print len(games)

data = np.array([g.high_seed().offensive_efficiency - g.low_seed().offensive_efficiency for g in games], dtype=np.float)

hist, bins = np.histogram(data, bins=100)
center = (bins[:-1] + bins[1:]) / 2
plt.bar(center, hist, align='center')
plt.show()