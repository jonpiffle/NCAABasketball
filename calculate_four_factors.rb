require_relative 'models'

db_queue = []
Play.all.each_with_index do |play, i|
	puts "#{i} #{play.id}" 

	#Calculate possesions according to kenpom
	possesions = play.fg_a - play.off_reb + play.turnovers +  0.475 * play.ft_a
	opponent_possesions = play.o_fg_a - play.o_off_reb + play.o_turnovers +  0.475 * play.o_ft_a

	#Avg possesions between me and my opponent (necessarily are the same)
	possesions = (possesions + opponent_possesions)/2.0

	offensive_efficiency = (play.pts * 100.0)/possesions
	defensive_efficiency = (play.o_pts * 100.0)/possesions

	effective_fg_pct = (play.fg + 0.5*play.three_fg)/(play.fg_a.to_f)
	turnover_pct = play.turnovers/possesions
	offensive_reb_pct = play.off_reb.to_f/(play.off_reb + play.o_def_reb)
	ft_rate = play.ft_a/play.fg_a.to_f

	o_effective_fg_pct = (play.o_fg + 0.5*play.o_three_fg)/(play.o_fg_a.to_f)
	o_turnover_pct = play.o_turnovers/possesions
	o_offensive_reb_pct = play.o_off_reb.to_f/(play.o_off_reb + play.def_reb)
	o_ft_rate = play.o_ft_a/play.o_fg_a.to_f

	four_factors = {
		'possesions' => possesions,
		'offensive_efficiency' => offensive_efficiency,
		'defensive_efficiency' => defensive_efficiency,
		'effective_fg_pct' => effective_fg_pct,
		'turnover_pct' => turnover_pct,
		'offensive_reb_pct' => offensive_reb_pct,
		'ft_rate' => ft_rate,
		"o_effective_fg_pct" => o_effective_fg_pct,
		"o_turnover_pct" => o_turnover_pct,
		"o_offensive_reb_pct" => o_offensive_reb_pct,
		"o_ft_rate" => o_ft_rate,
	}

	db_queue << Proc.new{play.update_attributes(four_factors)}
end


while !db_queue.empty?
	proc = db_queue.shift
	proc.call
end
