require 'csv'
require_relative 'models'
require_relative 'name_map'
require_relative 'kaggle_map'
require_relative 'year_map'

#season	rating_day_num	sys_name	team	orank
#CSV.foreach("data/ordinal_ranks_core_33.csv", :headers => true) do |row|
CSV.foreach("data/ordinal_ranks_season_S.csv", :headers => true) do |row|
	season = row[0]
	day = row[1]
	system = row[2]
	team = row[3]
	num = row[4]
	next unless YEAR_MAP.include?(season) && KAGGLE_MAP.include?(team)

	year = YEAR_MAP[season]
	date = Date.strptime(START_DATE_MAP[year], "%m/%d/%Y") + day.to_i.days

	t = Team.find_by_name(NAME_MAP[KAGGLE_MAP[team]])
	next if t.nil?

	ty = TeamYear.where(:year => year, :team_id => t.id).first
	next if ty.nil?

	Rank.create(:year => year, :system => system, :team_year_id => ty.id, :num => num.to_i, :date => date)
	puts "#{t.name}, #{season}"
end