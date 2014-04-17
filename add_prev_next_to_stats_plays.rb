require_relative 'models'

years = (2010..2014).to_a

years.each do |year|
	Team.all.each do |team|
		tys = team.team_years.includes(:plays => :cumulative_stat).where(:year => year)
		tys.each do |ty|
			puts "#{year} #{team.name}"
			db_queue = []
			ty.plays.sort_by {|p| p.game_number}.each_cons(3) do |prev_play, curr_play, next_play|
				prev_play.next_play_id = curr_play.id
				curr_play.prev_play_id = prev_play.id
				curr_play.next_play_id = next_play.id
				next_play.prev_play_id = curr_play.id

				prev_play.cumulative_stat.next_stat_id = curr_play.cumulative_stat.id if prev_play.cumulative_stat
				curr_play.cumulative_stat.prev_stat_id = prev_play.cumulative_stat.id if prev_play.cumulative_stat
				curr_play.cumulative_stat.next_stat_id = next_play.cumulative_stat.id
				next_play.cumulative_stat.prev_stat_id = curr_play.cumulative_stat.id

				db_queue << prev_play
				db_queue << curr_play
				db_queue << next_play
				db_queue << prev_play.cumulative_stat if prev_play.cumulative_stat
				db_queue << curr_play.cumulative_stat
				db_queue << next_play.cumulative_stat
			end

			db_queue.uniq.each do |obj|
				obj.save
			end
		end
	end
end
