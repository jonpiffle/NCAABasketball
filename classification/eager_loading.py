from models import *
from sqlalchemy.orm import relationship, backref, contains_eager, joinedload
from collections import defaultdict

keys = [
	"games.id",
	"games.date",
	"games.location",
	"plays.id",
	"cumulative_stats.fg",
	"cumulative_stats.fg_mean",
	"cumulative_stats.fg_min",
	"cumulative_stats.fg_max",
	"cumulative_stats.fg_variance",
	"cumulative_stats.o_fg",
	"cumulative_stats.o_fg_mean",
	"cumulative_stats.o_fg_min",
	"cumulative_stats.o_fg_max",
	"cumulative_stats.o_fg_variance",
	"cumulative_stats.fg_a",
	"cumulative_stats.fg_a_mean",
	"cumulative_stats.fg_a_min",
	"cumulative_stats.fg_a_max",
	"cumulative_stats.fg_a_variance",
	"cumulative_stats.o_fg_a",
	"cumulative_stats.o_fg_a_mean",
	"cumulative_stats.o_fg_a_min",
	"cumulative_stats.o_fg_a_max",
	"cumulative_stats.o_fg_a_variance",
	"cumulative_stats.three_fg",
	"cumulative_stats.three_fg_mean",
	"cumulative_stats.three_fg_min",
	"cumulative_stats.three_fg_max",
	"cumulative_stats.three_fg_variance",
	"cumulative_stats.o_three_fg",
	"cumulative_stats.o_three_fg_mean",
	"cumulative_stats.o_three_fg_min",
	"cumulative_stats.o_three_fg_max",
	"cumulative_stats.o_three_fg_variance",
	"cumulative_stats.three_fg_a",
	"cumulative_stats.three_fg_a_mean",
	"cumulative_stats.three_fg_a_min",
	"cumulative_stats.three_fg_a_max",
	"cumulative_stats.three_fg_a_variance",
	"cumulative_stats.o_three_fg_a",
	"cumulative_stats.o_three_fg_a_mean",
	"cumulative_stats.o_three_fg_a_min",
	"cumulative_stats.o_three_fg_a_max",
	"cumulative_stats.o_three_fg_a_variance",
	"cumulative_stats.ft",
	"cumulative_stats.ft_mean",
	"cumulative_stats.ft_min",
	"cumulative_stats.ft_max",
	"cumulative_stats.ft_variance",
	"cumulative_stats.o_ft",
	"cumulative_stats.o_ft_mean",
	"cumulative_stats.o_ft_min",
	"cumulative_stats.o_ft_max",
	"cumulative_stats.o_ft_variance",
	"cumulative_stats.ft_a",
	"cumulative_stats.ft_a_mean",
	"cumulative_stats.ft_a_min",
	"cumulative_stats.ft_a_max",
	"cumulative_stats.ft_a_variance",
	"cumulative_stats.o_ft_a",
	"cumulative_stats.o_ft_a_mean",
	"cumulative_stats.o_ft_a_min",
	"cumulative_stats.o_ft_a_max",
	"cumulative_stats.o_ft_a_variance",
	"cumulative_stats.pts",
	"cumulative_stats.pts_mean",
	"cumulative_stats.pts_min",
	"cumulative_stats.pts_max",
	"cumulative_stats.pts_variance",
	"cumulative_stats.o_pts",
	"cumulative_stats.o_pts_mean",
	"cumulative_stats.o_pts_min",
	"cumulative_stats.o_pts_max",
	"cumulative_stats.o_pts_variance",
	"cumulative_stats.off_reb",
	"cumulative_stats.off_reb_mean",
	"cumulative_stats.off_reb_min",
	"cumulative_stats.off_reb_max",
	"cumulative_stats.off_reb_variance",
	"cumulative_stats.o_off_reb",
	"cumulative_stats.o_off_reb_mean",
	"cumulative_stats.o_off_reb_min",
	"cumulative_stats.o_off_reb_max",
	"cumulative_stats.o_off_reb_variance",
	"cumulative_stats.def_reb",
	"cumulative_stats.def_reb_mean",
	"cumulative_stats.def_reb_min",
	"cumulative_stats.def_reb_max",
	"cumulative_stats.def_reb_variance",
	"cumulative_stats.o_def_reb",
	"cumulative_stats.o_def_reb_mean",
	"cumulative_stats.o_def_reb_min",
	"cumulative_stats.o_def_reb_max",
	"cumulative_stats.o_def_reb_variance",
	"cumulative_stats.reb",
	"cumulative_stats.reb_mean",
	"cumulative_stats.reb_min",
	"cumulative_stats.reb_max",
	"cumulative_stats.reb_variance",
	"cumulative_stats.o_reb",
	"cumulative_stats.o_reb_mean",
	"cumulative_stats.o_reb_min",
	"cumulative_stats.o_reb_max",
	"cumulative_stats.o_reb_variance",
	"cumulative_stats.ast",
	"cumulative_stats.ast_mean",
	"cumulative_stats.ast_min",
	"cumulative_stats.ast_max",
	"cumulative_stats.ast_variance",
	"cumulative_stats.o_ast",
	"cumulative_stats.o_ast_mean",
	"cumulative_stats.o_ast_min",
	"cumulative_stats.o_ast_max",
	"cumulative_stats.o_ast_variance",
	"cumulative_stats.turnovers",
	"cumulative_stats.turnovers_mean",
	"cumulative_stats.turnovers_min",
	"cumulative_stats.turnovers_max",
	"cumulative_stats.turnovers_variance",
	"cumulative_stats.o_turnovers",
	"cumulative_stats.o_turnovers_mean",
	"cumulative_stats.o_turnovers_min",
	"cumulative_stats.o_turnovers_max",
	"cumulative_stats.o_turnovers_variance",
	"cumulative_stats.steals",
	"cumulative_stats.steals_mean",
	"cumulative_stats.steals_min",
	"cumulative_stats.steals_max",
	"cumulative_stats.steals_variance",
	"cumulative_stats.o_steals",
	"cumulative_stats.o_steals_mean",
	"cumulative_stats.o_steals_min",
	"cumulative_stats.o_steals_max",
	"cumulative_stats.o_steals_variance",
	"cumulative_stats.blocks",
	"cumulative_stats.blocks_mean",
	"cumulative_stats.blocks_min",
	"cumulative_stats.blocks_max",
	"cumulative_stats.blocks_variance",
	"cumulative_stats.o_blocks",
	"cumulative_stats.o_blocks_mean",
	"cumulative_stats.o_blocks_min",
	"cumulative_stats.o_blocks_max",
	"cumulative_stats.o_blocks_variance",
	"cumulative_stats.fouls",
	"cumulative_stats.fouls_mean",
	"cumulative_stats.fouls_min",
	"cumulative_stats.fouls_max",
	"cumulative_stats.fouls_variance",
	"cumulative_stats.o_fouls",
	"cumulative_stats.o_fouls_mean",
	"cumulative_stats.o_fouls_min",
	"cumulative_stats.o_fouls_max",
	"cumulative_stats.o_fouls_variance",
	"ranks.system",
	"ranks.num"
]

games = connection.execute(
	"SELECT " + ",".join(keys) +
	"""
	FROM games 
	INNER JOIN plays ON games.id = plays.game_id 
	INNER JOIN cumulative_stats ON plays.id = cumulative_stats.play_id
	INNER JOIN cumulative_stats_ranks ON cumulative_stats.id = cumulative_stats_ranks.cumulative_stat_id
	INNER JOIN ranks ON ranks.id = cumulative_stats_ranks.rank_id
	WHERE NOT (
		EXISTS (
			SELECT * 
			FROM plays 
			WHERE plays.game_number <= 5 AND plays.game_id = games.id
		)
	)
	AND ranks.system IN ('RPI', 'POM')
	AND games.id = 35791;
	"""
)

for game in games:
	print dict(zip(keys, game))