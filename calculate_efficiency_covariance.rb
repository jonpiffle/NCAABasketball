require_relative 'models'

years = (2010..2014).to_a
years.each do |year|
    Game.where(:year => year).includes(:plays => :cumulative_stat).order('date asc').each_with_index do |game, i|
        puts "#{year} #{i} #{game.id}"

        cstats = game.cumulative_stats        
        cstats.each do |cstat|
            prev_play = cstat.play.prev_play
            prev_stat = cstat.prev_stat
            n = cstat.play.game_number.to_f

            next if prev_play.nil?

            if prev_stat.nil? || prev_stat.efficiency_covariance.nil?
                puts "NIL"
                cov = 0
                cstat.update_attributes(:efficiency_covariance => cov)
            else
                puts "NOTNIL"

                #See http://en.wikipedia.org/wiki/Algorithms_for_calculating_variance#Covariance for incremental update formula
                cov = (prev_stat.efficiency_covariance * (n-1).to_f + (prev_play.offensive_efficiency - prev_stat.offensive_efficiency_mean)*(prev_play.defensive_efficiency - prev_stat.defensive_efficiency_mean))/n.to_f

                cstat.update_attributes(:efficiency_covariance => cov)
            end
        end
    end
end