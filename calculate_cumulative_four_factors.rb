require_relative 'models'

stats = ["possessions", "offensive_efficiency", "defensive_efficiency", "scoring_possessions", "o_scoring_possessions", "field_pct", "o_field_pct", "plays", "o_plays", "play_pct", "o_play_pct", "floor_pct", "o_floor_pct", "effective_fg_pct", "o_effective_fg_pct", "turnover_pct", "o_turnover_pct", "offensive_reb_pct", "o_offensive_reb_pct", "ft_rate", "o_ft_rate", "fg_pct", "o_fg_pct", "three_fg_pct", "o_three_fg_pct", "ft_pct", "o_ft_pct"]
years = (2014..2014).to_a
years.each do |year|
    Game.where(:year => year).includes(:plays => :cumulative_stat).order('date asc').each_with_index do |game, i|
        puts "#{year} #{i} #{game.id}"

        cstats = game.cumulative_stats        
        cstats.each do |cstat|
            prev_play = cstat.play.prev_play
            prev_stat = cstat.prev_stat
            n = cstat.play.game_number.to_f

            next if prev_play.nil?
            cumulative_stats_dict = {}

            if prev_stat.nil? || stats.map {|s| prev_play.send("#{s}")}.include?(nil) || stats.map {|s| prev_stat.send("#{s}_mean")}.include?(nil) || stats.map {|s| prev_stat.send("#{s}_min")}.include?(nil) || stats.map {|s| prev_stat.send("#{s}_max")}.include?(nil) || stats.map {|s| prev_stat.send("#{s}_variance")}.include?(nil)
                puts "NIL"

                stats.each do |stat|
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

                stats.each do |stat|
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