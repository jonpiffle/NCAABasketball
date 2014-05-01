require_relative 'models'

class Array
	def avg
		copy = self.compact
		return copy.inject(:+)/copy.length
	end
end


CumulativeStat.joins(:play => :game).where("games.year = 2013").update_all(
	"adj_offensive_efficiency" => nil,
	"adj_offensive_efficiency_mean" => nil,
	"adj_offensive_efficiency_max" => nil,
	"adj_offensive_efficiency_min" => nil,
	"adj_offensive_efficiency_variance" => nil,
	"adj_defensive_efficiency" => nil,
	"adj_defensive_efficiency_mean" => nil,
	"adj_defensive_efficiency_max" => nil,
	"adj_defensive_efficiency_min" => nil,
	"adj_defensive_efficiency_variance" => nil
)

Play.joins(:game).where("games.year = 2013").update_all(
	"adj_offensive_efficiency" => nil,
	"adj_defensive_efficiency" => nil
)


START_YEAR = 2010
START_INDEX = 0

years = (2010..2014)
years.each do |year|

	next if year < START_YEAR

	avg_offensive_efficiency = Play.includes(:game).where(:games => {:year => year}).pluck(:offensive_efficiency).avg
	avg_defensive_efficiency = Play.includes(:game).where(:games => {:year => year}).pluck(:defensive_efficiency).avg

	Game.where(:year => year).includes(:plays => :cumulative_stat).order('date asc').each_with_index do |game, i|
		puts "#{year} #{i} #{game.id}"
		next if (i < START_INDEX && year == START_YEAR) || year < START_YEAR

		stats = game.cumulative_stats		
		stats.each do |cstat|
			other_c = stats.keep_if {|c| c != cstat}.first
			prev_play = cstat.play.prev_play
			prev_stat = cstat.prev_stat
			n = cstat.play.game_number.to_f

			next if prev_play.nil?

			if other_c.nil? || other_c.adj_offensive_efficiency_mean.nil? || other_c.adj_defensive_efficiency_mean.nil?
				prev_play.adj_offensive_efficiency = prev_play.offensive_efficiency 
				prev_play.adj_defensive_efficiency = prev_play.defensive_efficiency

			else
				prev_play.adj_offensive_efficiency = prev_play.offensive_efficiency * avg_offensive_efficiency / (other_c.adj_defensive_efficiency_mean)
				prev_play.adj_defensive_efficiency = prev_play.defensive_efficiency * avg_defensive_efficiency / (other_c.adj_offensive_efficiency_mean)
			end

			prev_play.save
			
			cumulative_stats_dict = {}

			if prev_stat.nil? || prev_stat.adj_offensive_efficiency_mean.nil? || prev_stat.adj_defensive_efficiency_mean.nil?
				puts "NIL"
			

				["adj_offensive_efficiency", "adj_defensive_efficiency"].each do |stat|
					#Sum
                    cumulative_stats_dict["#{stat}"] = prev_play.send("#{stat}")

                    #Mean
                    cumulative_stats_dict["#{stat}_mean"] = prev_play.send("#{stat}")

                    #Variance
                    cumulative_stats_dict["#{stat}_variance"] = 0

                    #Min
                    cumulative_stats_dict["#{stat}_min"] = prev_play.send("#{stat}")

                    #Max
                    cumulative_stats_dict["#{stat}_max"] = prev_play.send("#{stat}")
                end

                cstat.update_attributes(cumulative_stats_dict)
			else

				puts "NOTNIL"


				["adj_offensive_efficiency", "adj_defensive_efficiency"].each do |stat|
					#Sum
                    cumulative_stats_dict["#{stat}"] = prev_stat.send("#{stat}") + prev_play.send("#{stat}")

                    #Mean
                    cumulative_stats_dict["#{stat}_mean"] = 1/n.to_f*(prev_play.send("#{stat}") + (n.to_f - 1)*prev_stat.send("#{stat}_mean"))

                    #Variance
                    cumulative_stats_dict["#{stat}_variance"] = (n.to_f - 2)/(n.to_f - 1)*prev_stat.send("#{stat}_variance") + 1/n.to_f*(prev_play.send("#{stat}") - prev_stat.send("#{stat}_mean"))**2 

                    #Min
                    cumulative_stats_dict["#{stat}_min"] = [prev_stat.send("#{stat}_min"), prev_play.send("#{stat}")].min

                    #Max
                    cumulative_stats_dict["#{stat}_max"] = [prev_stat.send("#{stat}_max"), prev_play.send("#{stat}")].max
                end

                cstat.update_attributes(cumulative_stats_dict)
			end
		end
	end
end
