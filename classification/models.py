from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float, Date, exists, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import func
from sqlalchemy.sql import select
from sqlalchemy.orm import relationship, backref, contains_eager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import numpy as np
import math

Base = declarative_base()

def list_get (l, idx, default=None):
	try:
		return l[idx]
	except IndexError:
		return default

class CumulativeStat(Base):
	__tablename__ = 'cumulative_stats'

	id = Column(Integer, primary_key=True)
	play_id = Column(Integer, ForeignKey("plays.id"))

	fg = Column(Float)
	fg_mean = Column(Float)
	fg_min = Column(Float)
	fg_max = Column(Float)
	fg_variance = Column(Float)
	o_fg = Column(Float)
	o_fg_mean = Column(Float)
	o_fg_min = Column(Float)
	o_fg_max = Column(Float)
	o_fg_variance = Column(Float)
	fg_a = Column(Float)
	fg_a_mean = Column(Float)
	fg_a_min = Column(Float)
	fg_a_max = Column(Float)
	fg_a_variance = Column(Float)
	o_fg_a = Column(Float)
	o_fg_a_mean = Column(Float)
	o_fg_a_min = Column(Float)
	o_fg_a_max = Column(Float)
	o_fg_a_variance = Column(Float)
	three_fg = Column(Float)
	three_fg_mean = Column(Float)
	three_fg_min = Column(Float)
	three_fg_max = Column(Float)
	three_fg_variance = Column(Float)
	o_three_fg = Column(Float)
	o_three_fg_mean = Column(Float)
	o_three_fg_min = Column(Float)
	o_three_fg_max = Column(Float)
	o_three_fg_variance = Column(Float)
	three_fg_a = Column(Float)
	three_fg_a_mean = Column(Float)
	three_fg_a_min = Column(Float)
	three_fg_a_max = Column(Float)
	three_fg_a_variance = Column(Float)
	o_three_fg_a = Column(Float)
	o_three_fg_a_mean = Column(Float)
	o_three_fg_a_min = Column(Float)
	o_three_fg_a_max = Column(Float)
	o_three_fg_a_variance = Column(Float)
	ft = Column(Float)
	ft_mean = Column(Float)
	ft_min = Column(Float)
	ft_max = Column(Float)
	ft_variance = Column(Float)
	o_ft = Column(Float)
	o_ft_mean = Column(Float)
	o_ft_min = Column(Float)
	o_ft_max = Column(Float)
	o_ft_variance = Column(Float)
	ft_a = Column(Float)
	ft_a_mean = Column(Float)
	ft_a_min = Column(Float)
	ft_a_max = Column(Float)
	ft_a_variance = Column(Float)
	o_ft_a = Column(Float)
	o_ft_a_mean = Column(Float)
	o_ft_a_min = Column(Float)
	o_ft_a_max = Column(Float)
	o_ft_a_variance = Column(Float)
	pts = Column(Float)
	pts_mean = Column(Float)
	pts_min = Column(Float)
	pts_max = Column(Float)
	pts_variance = Column(Float)
	o_pts = Column(Float)
	o_pts_mean = Column(Float)
	o_pts_min = Column(Float)
	o_pts_max = Column(Float)
	o_pts_variance = Column(Float)
	off_reb = Column(Float)
	off_reb_mean = Column(Float)
	off_reb_min = Column(Float)
	off_reb_max = Column(Float)
	off_reb_variance = Column(Float)
	o_off_reb = Column(Float)
	o_off_reb_mean = Column(Float)
	o_off_reb_min = Column(Float)
	o_off_reb_max = Column(Float)
	o_off_reb_variance = Column(Float)
	def_reb = Column(Float)
	def_reb_mean = Column(Float)
	def_reb_min = Column(Float)
	def_reb_max = Column(Float)
	def_reb_variance = Column(Float)
	o_def_reb = Column(Float)
	o_def_reb_mean = Column(Float)
	o_def_reb_min = Column(Float)
	o_def_reb_max = Column(Float)
	o_def_reb_variance = Column(Float)
	reb = Column(Float)
	reb_mean = Column(Float)
	reb_min = Column(Float)
	reb_max = Column(Float)
	reb_variance = Column(Float)
	o_reb = Column(Float)
	o_reb_mean = Column(Float)
	o_reb_min = Column(Float)
	o_reb_max = Column(Float)
	o_reb_variance = Column(Float)
	ast = Column(Float)
	ast_mean = Column(Float)
	ast_min = Column(Float)
	ast_max = Column(Float)
	ast_variance = Column(Float)
	o_ast = Column(Float)
	o_ast_mean = Column(Float)
	o_ast_min = Column(Float)
	o_ast_max = Column(Float)
	o_ast_variance = Column(Float)
	turnovers = Column(Float)
	turnovers_mean = Column(Float)
	turnovers_min = Column(Float)
	turnovers_max = Column(Float)
	turnovers_variance = Column(Float)
	o_turnovers = Column(Float)
	o_turnovers_mean = Column(Float)
	o_turnovers_min = Column(Float)
	o_turnovers_max = Column(Float)
	o_turnovers_variance = Column(Float)
	steals = Column(Float)
	steals_mean = Column(Float)
	steals_min = Column(Float)
	steals_max = Column(Float)
	steals_variance = Column(Float)
	o_steals = Column(Float)
	o_steals_mean = Column(Float)
	o_steals_min = Column(Float)
	o_steals_max = Column(Float)
	o_steals_variance = Column(Float)
	blocks = Column(Float)
	blocks_mean = Column(Float)
	blocks_min = Column(Float)
	blocks_max = Column(Float)
	blocks_variance = Column(Float)
	o_blocks = Column(Float)
	o_blocks_mean = Column(Float)
	o_blocks_min = Column(Float)
	o_blocks_max = Column(Float)
	o_blocks_variance = Column(Float)
	fouls = Column(Float)
	fouls_mean = Column(Float)
	fouls_min = Column(Float)
	fouls_max = Column(Float)
	fouls_variance = Column(Float)
	o_fouls = Column(Float)
	o_fouls_mean = Column(Float)
	o_fouls_min = Column(Float)
	o_fouls_max = Column(Float)
	o_fouls_variance = Column(Float)

	l_ranks = relationship("Rank", secondary="cumulative_stats_ranks", lazy='dynamic', backref=backref("l_cumulative_stats", lazy='dynamic'))
	ranks = relationship("Rank", secondary="cumulative_stats_ranks", backref=backref("cumulative_stats"))
	play = relationship("Play", foreign_keys="CumulativeStat.play_id", backref=backref('cumulative_stat', uselist=False))

	def attributes(self):
		return np.array([
			self.get_rank("RPI"),
			self.get_rank("SAG"),
			self.get_rank("POM"),
			self.get_rank("MOR"),
			self.fg_mean,
			self.fg_min,
			self.fg_max,
			self.fg_variance,
			self.o_fg_mean,
			self.o_fg_min,
			self.o_fg_max,
			self.o_fg_variance,
			self.fg_a_mean,
			self.fg_a_min,
			self.fg_a_max,
			self.fg_a_variance,
			self.o_fg_a_mean,
			self.o_fg_a_min,
			self.o_fg_a_max,
			self.o_fg_a_variance,
			self.three_fg_mean,
			self.three_fg_min,
			self.three_fg_max,
			self.three_fg_variance,
			self.o_three_fg_mean,
			self.o_three_fg_min,
			self.o_three_fg_max,
			self.o_three_fg_variance,
			self.three_fg_a_mean,
			self.three_fg_a_min,
			self.three_fg_a_max,
			self.three_fg_a_variance,
			self.o_three_fg_a_mean,
			self.o_three_fg_a_min,
			self.o_three_fg_a_max,
			self.o_three_fg_a_variance,
			self.ft_mean,
			self.ft_min,
			self.ft_max,
			self.ft_variance,
			self.o_ft_mean,
			self.o_ft_min,
			self.o_ft_max,
			self.o_ft_variance,
			self.ft_a_mean,
			self.ft_a_min,
			self.ft_a_max,
			self.ft_a_variance,
			self.o_ft_a_mean,
			self.o_ft_a_min,
			self.o_ft_a_max,
			self.o_ft_a_variance,
			self.pts_mean,
			self.pts_min,
			self.pts_max,
			self.pts_variance,
			self.o_pts_mean,
			self.o_pts_min,
			self.o_pts_max,
			self.o_pts_variance,
			self.off_reb_mean,
			self.off_reb_min,
			self.off_reb_max,
			self.off_reb_variance,
			self.o_off_reb_mean,
			self.o_off_reb_min,
			self.o_off_reb_max,
			self.o_off_reb_variance,
			self.def_reb_mean,
			self.def_reb_min,
			self.def_reb_max,
			self.def_reb_variance,
			self.o_def_reb_mean,
			self.o_def_reb_min,
			self.o_def_reb_max,
			self.o_def_reb_variance,
			self.reb_mean,
			self.reb_min,
			self.reb_max,
			self.reb_variance,
			self.o_reb_mean,
			self.o_reb_min,
			self.o_reb_max,
			self.o_reb_variance,
			self.ast_mean,
			self.ast_min,
			self.ast_max,
			self.ast_variance,
			self.o_ast_mean,
			self.o_ast_min,
			self.o_ast_max,
			self.o_ast_variance,
			self.turnovers_mean,
			self.turnovers_min,
			self.turnovers_max,
			self.turnovers_variance,
			self.o_turnovers_mean,
			self.o_turnovers_min,
			self.o_turnovers_max,
			self.o_turnovers_variance,
			self.steals_mean,
			self.steals_min,
			self.steals_max,
			self.steals_variance,
			self.o_steals_mean,
			self.o_steals_min,
			self.o_steals_max,
			self.o_steals_variance,
			self.blocks_mean,
			self.blocks_min,
			self.blocks_max,
			self.blocks_variance,
			self.o_blocks_mean,
			self.o_blocks_min,
			self.o_blocks_max,
			self.o_blocks_variance,
			self.fouls_mean,
			self.fouls_min,
			self.fouls_max,
			self.fouls_variance,
			self.o_fouls_mean,
			self.o_fouls_min,
			self.o_fouls_max,
			self.o_fouls_variance
		], dtype="float")
	
	def selected_features(self):
		return np.array([
			self.get_rank("RPI"),
			self.get_rank("SAG"),
			self.get_rank("POM"),
			self.get_rank("MOR"),
			self.fg_mean,
			self.o_fg_mean,
			self.pts_mean,
			self.pts_min,
			self.o_pts_mean,
			self.o_pts_min,
			self.o_def_reb_mean,
			self.o_reb_mean,
			self.ast_mean,
			self.o_ast_mean,
			self.ast_max,
			self.turnovers_mean,
		], dtype="float")


	def get_scaled_rank(self, system):
		r = self.get_rank(system)
		return (100 - 4*math.log(r+1) - r/22)

	def get_rank(self, system):
		ranks = [r for r in self.ranks if r.system == system]
		if len(ranks) > 0:
			return ranks[0].num
		else:
			return None

class CumulativeStatsRank(Base):
	__tablename__ = 'cumulative_stats_ranks'

	id = Column(Integer, primary_key=True)
	cumulative_stat_id = Column(Integer, ForeignKey("cumulative_stats.id"))
	rank_id = Column(Integer, ForeignKey("ranks.id"))
	cumulative_stat = relationship("CumulativeStat", foreign_keys="CumulativeStatsRank.cumulative_stat_id", backref=backref('cumulative_stats_ranks', lazy='dynamic'))
	l_rank = relationship("Rank", foreign_keys="CumulativeStatsRank.rank_id", backref=backref('l_cumulative_stats_ranks', lazy='dynamic'))
	rank = relationship("Rank", foreign_keys="CumulativeStatsRank.rank_id", backref=backref('cumulative_stats_ranks'))


class Game(Base):
	__tablename__ = 'games'
	id = Column(Integer, primary_key=True)
	year = Column(Integer)
	date = Column(Date)
	location = Column(String)

	def points_diff(self):
		return self.high_seed().play.pts - self.low_seed().play.pts

	def attributes(self):
		return self.high_seed().attributes() - self.low_seed().attributes()

	def selected_features(self):
		return self.high_seed().selected_features() - self.low_seed().selected_features()

	def winner(self):
		try:
			return [p.cumulative_stat for p in self.plays if p.won][0]
		except IndexError:
			print self.__dict__

	def loser(self):
		return [p.cumulative_stat for p in self.plays if not p.won][0]

	def high_seed(self):
		return min(self.plays, key=lambda x: x.cumulative_stat.get_rank("RPI")).cumulative_stat

	def low_seed(self):
		return max(self.plays, key=lambda x: x.cumulative_stat.get_rank("RPI")).cumulative_stat

	def upset(self):
		return self.winner() == self.low_seed()

	def rpi_diff(self):
		return self.high_seed().get_scaled_rank("RPI") - self.low_seed().get_scaled_rank("RPI")

	def projected_winner(self, upset):
		if upset:
			return self.low_seed().play.team_year
		else:
			return self.high_seed().play.team_year

	@classmethod
	def games_after(self, after_threshold, rank_systems=("RPI",)):
		games = (session.query(Game).\
			select_entity_from(
				select([Game.id, func.count(Game.id).label("games_count")], from_obj=[Play]).\
				where(("games.id = plays.game_id AND plays.game_number > %s AND plays.won IS NOT NULL" % after_threshold)).\
				group_by(Game.id).\
				having(func.count() == 2)
			)#.limit(limit).from_self()
		).join(Game.plays).\
		options(contains_eager(Game.plays)).\
		join(Play.cumulative_stat).\
		options(contains_eager(Game.plays).contains_eager(Play.cumulative_stat)).\
		join(CumulativeStat.ranks).\
		options(contains_eager(Game.plays).contains_eager(Play.cumulative_stat).contains_eager(CumulativeStat.ranks)).\
		filter(Rank.system.in_(rank_systems))

		print games
		return games.all()

	@classmethod	
	def games_after_with_filter(self, after_threshold, rank_systems=("RPI",)):
		games = (session.query(Game).\
			join(Game.plays).\
			filter(Play.game_number > after_threshold).\
			filter("plays.won IS NOT NULL").\
			options(contains_eager(Game.plays)).\
			join(Play.cumulative_stat).\
			options(contains_eager(Game.plays).contains_eager(Play.cumulative_stat)).\
			join(CumulativeStat.ranks).\
			options(contains_eager(Game.plays).contains_eager(Play.cumulative_stat).contains_eager(CumulativeStat.ranks)).\
			filter(Rank.system.in_(rank_systems)))

		#print games

		games = games.all()
		games = [g for g in games if len(g.plays) == 2]
		return games



class Play(Base):
	__tablename__ = "plays"
	id = Column(Integer, primary_key=True)
	team_year_id = Column(Integer, ForeignKey("team_years.id"))
	game_id = Column(Integer, ForeignKey("games.id"))

	won = Column(Integer)
	fg = Column(Integer)
	fg_a = Column(Integer)
	three_fg = Column(Integer)
	three_fg_a = Column(Integer)
	ft = Column(Integer)
	ft_a = Column(Integer)
	pts = Column(Integer)
	off_reb = Column(Integer)
	def_reb = Column(Integer)
	reb = Column(Integer)
	ast = Column(Integer)
	turnovers = Column(Integer)
	steals = Column(Integer)
	blocks = Column(Integer)
	fouls = Column(Integer)
	o_fg = Column(Integer)
	o_fg_a = Column(Integer)
	o_three_fg = Column(Integer)
	o_three_fg_a = Column(Integer)
	o_ft = Column(Integer)
	o_ft_a = Column(Integer)
	o_pts = Column(Integer)
	o_off_reb = Column(Integer)
	o_def_reb = Column(Integer)
	o_reb = Column(Integer)
	o_ast = Column(Integer)
	o_turnovers = Column(Integer)
	o_steals = Column(Integer)
	o_blocks = Column(Integer)
	o_fouls = Column(Integer)
	game_number = Column(Integer)

	def attributes(self):
		return self.cumulative_stat.attributes()

	team_year = relationship("TeamYear", foreign_keys="Play.team_year_id", backref=backref('plays', lazy='dynamic'))
	#l_game = relationship("Game", foreign_keys="Play.game_id", backref=backref('l_plays', lazy='dynamic'))
	game = relationship("Game", foreign_keys="Play.game_id", backref=backref('plays'))

	def __repr__(self):
		return "<Play: %s %s>" % (self.game.date, self.team_year.team.name)


class Rank(Base):
	__tablename__ = 'ranks'
	id = Column(Integer, primary_key=True)
	team_year_id = Column(Integer, ForeignKey("team_years.id"))
	year = Column(Integer)
	date = Column(Date)
	num = Column(Integer)
	system = Column(String)
	team_year = relationship("TeamYear", foreign_keys="Rank.team_year_id", backref=backref('ranks', lazy='dynamic'))

	def __repr__(self):
		return "<Rank: %s %s %s %s>" % (self.date, self.team_year.team.name, self.system, self.num)


class Team(Base):
	__tablename__ = 'teams'
	id = Column(Integer, primary_key=True)
	name = Column(String)

	def __repr__(self):
		return "<Team: %s>" % (self.name)


class TeamYear(Base):
	__tablename__ = 'team_years'

	id = Column(Integer, primary_key=True)
	team_id = Column(Integer, ForeignKey("teams.id"))
	year = Column(Integer)
	team = relationship("Team", foreign_keys="TeamYear.team_id", backref=backref('team_years', lazy='dynamic'))

	def __repr__(self):
		return "<TeamYear: %s %s>" % (self.team.name, self.year)


engine = create_engine('postgresql://localhost/ncaa_basketball')
connection = engine.connect()
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()