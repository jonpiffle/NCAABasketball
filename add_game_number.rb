require_relative 'models'

db_queue = []
years = (2010..2014).to_a
years.each do |year|
    puts year
    Team.all.each do |team|
        ty = team.team_years.find_by_year(year)
        next if ty.nil?
        plays = ty.plays.sort {|a,b| a.game.date <=> b.game.date}

        plays.each.with_index(1) do |play, i|
            db_queue << Proc.new{play.update_attributes(:game_number => i)}
        end
    end
end

while !db_queue.empty?
	proc = db_queue.shift
	proc.call
end