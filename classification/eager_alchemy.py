from models import *
from sqlalchemy.orm import relationship, backref, contains_eager, contains_eager
from sqlalchemy.sql.expression import func
from sqlalchemy import alias
from sqlalchemy.sql import select

"""
stats = session.query(CumulativeStat).\
		join(CumulativeStat.play).\
		options(contains_eager(CumulativeStat.play)).\
		join(CumulativeStat.ranks).\
		options(contains_eager(CumulativeStat.ranks)).\
		join(Play.game).\
		filter(Rank.system.in_(('RPI', "POM"))).limit(100)
"""



subgames1 = session.query(Game).from_statement(
	"""
	SELECT *
	FROM games
	INNER JOIN (SELECT count(games.id) AS count_1, games.id as g_id 
		FROM games INNER JOIN plays ON games.id = plays.game_id 
		WHERE plays.game_number > 5
		GROUP BY games.id
		HAVING count(games.id) = 2) gs ON games.id = gs.g_id;

	"""
)


games = (session.query(Game).\
			select_entity_from(
				select([Game.id, func.count(Game.id).label("games_count")], from_obj=[Play]).\
				where("games.id = plays.game_id AND plays.game_number > 2").\
				group_by(Game.id).\
				having(func.count() == 2)
			).limit(None).from_self()
		).join(Game.plays).\
		options(contains_eager(Game.plays)).\
		join(Play.cumulative_stat).\
		options(contains_eager(Game.plays).contains_eager(Play.cumulative_stat)).\
		join(CumulativeStat.ranks).\
		options(contains_eager(Game.plays).contains_eager(Play.cumulative_stat).contains_eager(CumulativeStat.ranks)).\
		filter(Rank.system.in_(('RPI', "POM")))
	

"""
games = subgames.\
		join(Game.plays).\
		options(contains_eager(Game.plays)).\
		join(Play.cumulative_stat).\
		options(contains_eager(Game.plays).contains_eager(Play.cumulative_stat)).\
		join(CumulativeStat.ranks).\
		options(contains_eager(Game.plays).contains_eager(Play.cumulative_stat).contains_eager(CumulativeStat.ranks)).\
		filter(Rank.system.in_(('RPI', "POM")))
"""

print games
print games.all()[0].__dict__