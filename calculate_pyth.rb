require_relative 'models'

db_queue = []
START_INDEX = 39126
CumulativeStat.all.each_with_index do |stat,i|
	next if i < START_INDEX || stat.adj_offensive_efficiency.nil? || stat.adj_defensive_efficiency.nil?
	puts i
	pyth = (stat.adj_offensive_efficiency**10.25)/(stat.adj_offensive_efficiency**10.25+stat.adj_defensive_efficiency**10.25)
	db_queue << Proc.new{stat.update_attributes(:pyth_expectation_mean => pyth)}

	if db_queue.size > 1000
		while db_queue.size > 0
			db_queue.shift.call
		end
	end
end