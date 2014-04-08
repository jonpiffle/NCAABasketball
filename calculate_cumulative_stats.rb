require_relative 'models'

stats = ["fg", "fg_a", "three_fg", "three_fg_a", "ft", "ft_a", "pts", "off_reb", "def_reb", "reb", "ast", "turnovers", "steals", "blocks", "fouls"]
prefixes = ["", "o_"]
suffixes = ["", "_mean", "_min", "_max"]
years = (2010..2014).to_a
years.each do |year|
    CumulativeStat.includes(:game).where(:games => {:year => year}).destroy_all
    puts year
    Team.all.each do |team|
        puts team.name
        ty = team.team_years.find_by_year(year)

        next if ty.nil?

        plays = ty.plays.sort {|a,b| a.game.date <=> b.game.date}

        next if plays.length < 2

        #Initialize cumulative stats for game 2 to stats from game 1
        first_week_play = plays.first
        second_week_stats = plays[1].cumulative_stat || plays[1].create_cumulative_stat
        second_week_stats_update_dict = {}
        stats.each do |stat|
            prefixes.each do |prefix|
                suffixes.each do |suffix|
                    second_week_stats_update_dict["#{prefix}#{stat}#{suffix}"] = first_week_play.send("#{prefix}#{stat}")
                end
                second_week_stats_update_dict["#{prefix}#{stat}_variance"] = 0
            end
        end
        second_week_stats.update_attributes(second_week_stats_update_dict)

        #Update all remaining weeks
        plays[1..-1].each_cons(2).with_index(2).each do |p, n|
            prev = p.first
            curr = p.last

            cumulative_stats_dict = {}
            prev_stats = prev.cumulative_stat

            stats.each do |stat|
                prefixes.each do |prefix|
                    #Sum
                    cumulative_stats_dict["#{prefix}#{stat}"] = prev_stats.send("#{prefix}#{stat}") + prev.send("#{prefix}#{stat}")

                    #Mean
                    cumulative_stats_dict["#{prefix}#{stat}_mean"] = 1/n.to_f*(prev.send("#{prefix}#{stat}") + (n.to_f - 1)*prev_stats.send("#{prefix}#{stat}_mean"))

                    #Variance
                    cumulative_stats_dict["#{prefix}#{stat}_variance"] = (n.to_f - 2)/(n.to_f - 1)*prev_stats.send("#{prefix}#{stat}_variance") + 1/n.to_f*(prev.send("#{prefix}#{stat}") - prev_stats.send("#{prefix}#{stat}_mean"))**2 

                    #Min
                    cumulative_stats_dict["#{prefix}#{stat}_min"] = [prev_stats.send("#{prefix}#{stat}_min"), prev.send("#{prefix}#{stat}")].min

                    #Max
                    cumulative_stats_dict["#{prefix}#{stat}_max"] = [prev_stats.send("#{prefix}#{stat}_max"), prev.send("#{prefix}#{stat}")].max

                end
            end
            curr.create_cumulative_stat(cumulative_stats_dict)
        end
    end
end