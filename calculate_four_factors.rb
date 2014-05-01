require_relative 'models'

db_queue = []
Play.all.each_with_index do |play, i|
	puts "#{i} #{play.id}" 

	#Calculate possessions according to kenpom
	possessions = play.fg_a - play.off_reb + play.turnovers +  0.475 * play.ft_a
	o_possessions = play.o_fg_a - play.o_off_reb + play.o_turnovers +  0.475 * play.o_ft_a

	#Avg possessions between me and my opponent (necessarily are the same)
	possessions = (possessions + o_possessions)/2.0

	#Scoring possessions according to dean oliver page 67
	scoring_possessions = play.fg + (1-(1-play.ft.to_f/play.ft_a.to_f)**2) * play.ft_a * 0.4
	o_scoring_possessions = play.o_fg + (1-(1-play.o_ft.to_f/play.o_ft_a.to_f)**2) * play.o_ft_a * 0.4

	#Field percentage according to dean oliver page 67
	field_pct = play.fg / (play.fg_a - ((play.off_reb.to_f/(play.off_reb+play.o_def_reb).to_f) * (play.fg_a-play.fg) * 1.07) + play.turnovers)
	o_field_pct = play.o_fg / (play.o_fg_a - ((play.o_off_reb.to_f/(play.o_off_reb+play.def_reb).to_f) * (play.o_fg_a-play.o_fg) * 1.07) + play.o_turnovers)

	#Plays according to dean olive page 67
	plays = play.fg_a + (play.ft_a * 0.4) + play.turnovers
	o_plays = play.o_fg_a + (play.o_ft_a * 0.4) + play.o_turnovers

	#Play pct according to dean oliver
	play_pct = scoring_possessions/plays
	o_play_pct = o_scoring_possessions/plays

	#Floor pct according to dean oliver
	floor_pct = scoring_possessions/possessions
	o_floor_pct = o_scoring_possessions/possessions

	#offensive and defensive efficiency according to dean oliver
	offensive_efficiency = (play.pts * 100.0)/possessions
	defensive_efficiency = (play.o_pts * 100.0)/possessions

	#four factors according to dean oliver
	effective_fg_pct = (play.fg + 0.5*play.three_fg)/(play.fg_a.to_f)
	turnover_pct = play.turnovers/possessions
	offensive_reb_pct = play.off_reb.to_f/(play.off_reb + play.o_def_reb)
	ft_rate = play.ft_a/play.fg_a.to_f

	o_effective_fg_pct = (play.o_fg + 0.5*play.o_three_fg)/(play.o_fg_a.to_f)
	o_turnover_pct = play.o_turnovers/possessions
	o_offensive_reb_pct = play.o_off_reb.to_f/(play.o_off_reb + play.def_reb)
	o_ft_rate = play.o_ft_a/play.o_fg_a.to_f

	#other derived stats
	fg_pct = play.fg/play.fg_a.to_f
	three_fg_pct = play.three_fg/play.three_fg_a.to_f
	ft_pct = play.ft/play.ft_a.to_f

	o_fg_pct = play.o_fg/play.o_fg_a.to_f
	o_three_fg_pct = play.o_three_fg/play.o_three_fg_a.to_f
	o_ft_pct = play.o_ft/play.o_ft_a.to_f

	four_factors = {
		'possessions' => possessions,
		'offensive_efficiency' => offensive_efficiency,
		'defensive_efficiency' => defensive_efficiency,

		'scoring_possessions' => scoring_possessions,
		'o_scoring_possessions' => o_scoring_possessions,

		'field_pct' => field_pct,
		'o_field_pct' => o_field_pct,

		'plays' => plays,
		'o_plays' => o_plays,

		'play_pct' => play_pct,
		'o_play_pct' => o_play_pct,

		'floor_pct' => floor_pct,
		'o_floor_pct' => o_floor_pct,

		'effective_fg_pct' => effective_fg_pct,
		'turnover_pct' => turnover_pct,
		'offensive_reb_pct' => offensive_reb_pct,
		'ft_rate' => ft_rate,

		"o_effective_fg_pct" => o_effective_fg_pct,
		"o_turnover_pct" => o_turnover_pct,
		"o_offensive_reb_pct" => o_offensive_reb_pct,
		"o_ft_rate" => o_ft_rate,

		'fg_pct' => fg_pct,
		'three_fg_pct' => three_fg_pct,
		'ft_pct' => ft_pct,

		'o_fg_pct' => o_fg_pct,
		'o_three_fg_pct' => o_three_fg_pct,
		'o_ft_pct' => o_ft_pct,
	}

	db_queue << Proc.new{play.update_attributes(four_factors)}
end


while !db_queue.empty?
	proc = db_queue.shift
	proc.call
end
