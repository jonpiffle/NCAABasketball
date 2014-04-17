from models import *
import numpy as np
from sklearn import preprocessing, feature_selection
from sklearn.svm import SVC
from sklearn.feature_selection import RFE

features = [
	"self.get_rank('RPI')",
	"self.get_rank('SAG')",
	"self.get_rank('POM')",
	"self.get_rank('MOR')",
	"self.fg_mean",
	"self.fg_min",
	"self.fg_max",
	"self.fg_variance",
	"self.o_fg_mean",
	"self.o_fg_min",
	"self.o_fg_max",
	"self.o_fg_variance",
	"self.fg_a_mean",
	"self.fg_a_min",
	"self.fg_a_max",
	"self.fg_a_variance",
	"self.o_fg_a_mean",
	"self.o_fg_a_min",
	"self.o_fg_a_max",
	"self.o_fg_a_variance",
	"self.three_fg_mean",
	"self.three_fg_min",
	"self.three_fg_max",
	"self.three_fg_variance",
	"self.o_three_fg_mean",
	"self.o_three_fg_min",
	"self.o_three_fg_max",
	"self.o_three_fg_variance",
	"self.three_fg_a_mean",
	"self.three_fg_a_min",
	"self.three_fg_a_max",
	"self.three_fg_a_variance",
	"self.o_three_fg_a_mean",
	"self.o_three_fg_a_min",
	"self.o_three_fg_a_max",
	"self.o_three_fg_a_variance",
	"self.ft_mean",
	"self.ft_min",
	"self.ft_max",
	"self.ft_variance",
	"self.o_ft_mean",
	"self.o_ft_min",
	"self.o_ft_max",
	"self.o_ft_variance",
	"self.ft_a_mean",
	"self.ft_a_min",
	"self.ft_a_max",
	"self.ft_a_variance",
	"self.o_ft_a_mean",
	"self.o_ft_a_min",
	"self.o_ft_a_max",
	"self.o_ft_a_variance",
	"self.pts_mean",
	"self.pts_min",
	"self.pts_max",
	"self.pts_variance",
	"self.o_pts_mean",
	"self.o_pts_min",
	"self.o_pts_max",
	"self.o_pts_variance",
	"self.off_reb_mean",
	"self.off_reb_min",
	"self.off_reb_max",
	"self.off_reb_variance",
	"self.o_off_reb_mean",
	"self.o_off_reb_min",
	"self.o_off_reb_max",
	"self.o_off_reb_variance",
	"self.def_reb_mean",
	"self.def_reb_min",
	"self.def_reb_max",
	"self.def_reb_variance",
	"self.o_def_reb_mean",
	"self.o_def_reb_min",
	"self.o_def_reb_max",
	"self.o_def_reb_variance",
	"self.reb_mean",
	"self.reb_min",
	"self.reb_max",
	"self.reb_variance",
	"self.o_reb_mean",
	"self.o_reb_min",
	"self.o_reb_max",
	"self.o_reb_variance",
	"self.ast_mean",
	"self.ast_min",
	"self.ast_max",
	"self.ast_variance",
	"self.o_ast_mean",
	"self.o_ast_min",
	"self.o_ast_max",
	"self.o_ast_variance",
	"self.turnovers_mean",
	"self.turnovers_min",
	"self.turnovers_max",
	"self.turnovers_variance",
	"self.o_turnovers_mean",
	"self.o_turnovers_min",
	"self.o_turnovers_max",
	"self.o_turnovers_variance",
	"self.steals_mean",
	"self.steals_min",
	"self.steals_max",
	"self.steals_variance",
	"self.o_steals_mean",
	"self.o_steals_min",
	"self.o_steals_max",
	"self.o_steals_variance",
	"self.blocks_mean",
	"self.blocks_min",
	"self.blocks_max",
	"self.blocks_variance",
	"self.o_blocks_mean",
	"self.o_blocks_min",
	"self.o_blocks_max",
	"self.o_blocks_variance",
	"self.fouls_mean",
	"self.fouls_min",
	"self.fouls_max",
	"self.fouls_variance",
	"self.o_fouls_mean",
	"self.o_fouls_min",
	"self.o_fouls_max",
	"self.o_fouls_variance",
	"self.possesions",
	"self.offensive_efficiency",
	"self.defensive_efficiency",
	"self.effective_fg_pct",
	"self.turnover_pct",
	"self.offensive_reb_pct",
	"self.ft_rate",
	#"self.adj_offensive_efficiency",
	#"self.adj_defensive_efficiency",
	#"self.pyth_expectation",
]

#DATA SETUP
games = Game.games_after_with_filter(5, rank_systems=("RPI", "SAG", "POM", "MOR",))
print "%s games returned" % len(games)

data = np.array([g.attributes() for g in games], dtype=np.float)
labels = np.array([g.upset() for g in games])

non_nan_indices = ~np.isnan(data).any(axis=1)
data = data[non_nan_indices]
labels = labels[non_nan_indices]

print "%s usable games returned" % len(data)

#FEATURE SELECTION VIA CLASSIFICATION
f_values, p_values = feature_selection.f_classif(data, labels)

annotated = zip(features, f_values)
sorted_annotated = sorted(annotated, key=lambda x: x[1])

for (feature, f_value) in sorted_annotated:
	print "%s: %s" % (feature, f_value)

print ""

