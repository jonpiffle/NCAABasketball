require_relative 'models'

#systems = ["RTH", "SEL", "SAG", "7OT", "PPR", "SFX", "DES", "RTB", "STH", "COL", "KPK", "RTP", "MB", "PGH", "TW", "POM", "CPA", "PIG", "DCI", "ADE", "DUN", "CPR", "DOL", "WOB", "BPI", "TPR", "TRP", "RT", "UPS", "RPI", "MAS", "DOK", "AP", "USA", "EBP", "WIL", "STS", "D1A", "BOB", "REW", "STF", "MSX", "WMR", "LMC", "TMR", "MPI", "SPR", "BIH", "KBM", "DII", "BUR", "MOR", "DC", "BBT", "GRS", "RTR", "CNG", "CRO", "SPW", "SP", "WOL", "SE", "WLK", "CJB", "NOL", "BLS", "PTS", "KRA", "LOG"]
CumulativeStatsRank.delete_all

TeamYear.all.each do |team_year|
	ranks = team_year.ranks.order("date asc").pluck("ranks.date, ranks.id, ranks.system").group_by {|r| r[2]}
	stats = team_year.plays.joins(:cumulative_stat).joins(:game).pluck("games.date, cumulative_stats.id").sort {|a, b| a[0] <=> b[0]}

	transactions = []

	next if ranks.nil?

	stats.each do |stat|
		ranks.each do |system, values|
			i = 0
			while values[i][0] < stat[0] && values.count < i
				i = i+1
			end

			r_id = values[i][1]
			transactions.push("(#{r_id}, #{stat[1]})")
		end
	end
	
	puts team_year.description

	if transactions.size > 0 
		ActiveRecord::Base.connection.execute("INSERT INTO cumulative_stats_ranks (rank_id, cumulative_stat_id) VALUES #{transactions.join(',')}")
	end
end