require 'mechanize'
require 'nokogiri'
require 'pry'
require_relative 'models'
require_relative 'name_map'

$game_url_hash = {}
$db_queue = []

def scrape_game_page(game_link, year)
	url = game_link.uri.to_s
	$game_url_hash.include?(url) ? return : $game_url_hash[url] = url
	
	begin
		game_page = game_link.click
	rescue
		puts "ERROR opening #{game_link.uri.to_s}"
		return
	end
	doc = Nokogiri::HTML(game_page.body)
	tables = doc.css('table.mytable')

	game_info = doc.css('div.contentArea table')[2]
	team1_info, team2_info = tables[1], tables[2]
	game, team1, team2 = {}, {}, {}

	game['date'] = Date.strptime(game_info.css('tr')[0].css('td')[1].text.strip, "%m/%d/%Y")
	game['location'] = game_info.css('tr')[1].css('td')[1].text.strip

	team1['name'] = team1_info.css('tr')[0].css('td')[0].text.strip
	team1_stats = team1_info.css('tr.grey_heading')[1].css('td').to_a.map(&:text)
	team1['fg'] = team1_stats[3].to_i
	team1['fg_a'] = team1_stats[4].to_i
	team1['three_fg'] = team1_stats[5].to_i
	team1['three_fg_a'] = team1_stats[6].to_i
	team1['ft'] = team1_stats[7].to_i
	team1['ft_a'] = team1_stats[8].to_i
	team1['pts'] = team1_stats[9].to_i
	team1['off_reb'] = team1_stats[10].to_i
	team1['def_reb'] = team1_stats[11].to_i
	team1['reb'] = team1_stats[12].to_i
	team1['ast'] = team1_stats[13].to_i
	team1['turnovers'] = team1_stats[14].to_i
	team1['steals'] = team1_stats[15].to_i
	team1['blocks'] = team1_stats[16].to_i
	team1['fouls'] = team1_stats[17].to_i

	team2['name'] = team2_info.css('tr')[0].css('td')[0].text.strip
	team2_stats = team2_info.css('tr.grey_heading')[1].css('td').to_a.map(&:text)
	team2['fg'] = team2_stats[3].to_i
	team2['fg_a'] = team2_stats[4].to_i
	team2['three_fg'] = team2_stats[5].to_i
	team2['three_fg_a'] = team2_stats[6].to_i
	team2['ft'] = team2_stats[7].to_i
	team2['ft_a'] = team2_stats[8].to_i
	team2['pts'] = team2_stats[9].to_i
	team2['off_reb'] = team2_stats[10].to_i
	team2['def_reb'] = team2_stats[11].to_i
	team2['reb'] = team2_stats[12].to_i
	team2['ast'] = team2_stats[13].to_i
	team2['turnovers'] = team2_stats[14].to_i
	team2['steals'] = team2_stats[15].to_i
	team2['blocks'] = team2_stats[16].to_i
	team2['fouls'] = team2_stats[17].to_i

	team1['o_fg'] = team2['fg']
	team1['o_fg_a'] = team2['fg_a']
	team1['o_three_fg'] = team2['three_fg']
	team1['o_three_fg_a'] = team2['three_fg_a']
	team1['o_ft'] = team2['ft']
	team1['o_ft_a'] = team2['ft_a']
	team1['o_pts'] = team2['pts']
	team1['o_off_reb'] = team2['off_reb']
	team1['o_def_reb'] = team2['def_reb']
	team1['o_reb'] = team2['reb']
	team1['o_ast'] = team2['ast']
	team1['o_turnovers'] = team2['turnovers']
	team1['o_steals'] = team2['steals']
	team1['o_blocks'] = team2['blocks']
	team1['o_fouls'] = team2['fouls']

	team2['o_fg'] = team1['fg']
	team2['o_fg_a'] = team1['fg_a']
	team2['o_three_fg'] = team1['three_fg']
	team2['o_three_fg_a'] = team1['three_fg_a']
	team2['o_ft'] = team1['ft']
	team2['o_ft_a'] = team1['ft_a']
	team2['o_pts'] = team1['pts']
	team2['o_off_reb'] = team1['off_reb']
	team2['o_def_reb'] = team1['def_reb']
	team2['o_reb'] = team1['reb']
	team2['o_ast'] = team1['ast']
	team2['o_turnovers'] = team1['turnovers']
	team2['o_steals'] = team1['steals']
	team2['o_blocks'] = team1['blocks']
	team2['o_fouls'] = team1['fouls']


	return unless NAME_MAP.include? team1["name"]
	return unless NAME_MAP.include? team2["name"]

	$db_queue << Proc.new {
		t1 = Team.where(:name => NAME_MAP[team1["name"]]).first_or_create
		t2 = Team.where(:name => NAME_MAP[team2["name"]]).first_or_create

		ty1 = TeamYear.where(:team_id => t1.id, :year => year).first_or_create
		ty2 = TeamYear.where(:team_id => t2.id, :year => year).first_or_create

		g = Game.create(:year => year, :date => game["date"], :location => game["location"])

		p1 = Play.create(:game_id => g.id, :team_year_id => ty1.id)
		p2 = Play.create(:game_id => g.id, :team_year_id => ty2.id)

		team1.delete("name")
		team2.delete("name")

		p1.update_attributes(team1)
		p2.update_attributes(team2)

		if p1.pts > p2.pts
			p1.update_attributes(:won => true)
			p2.update_attributes(:won => false)
		elsif p2.pts > p1.pts
			p1.update_attributes(:won => false)
			p2.update_attributes(:won => true)
		end

		puts "#{t1.name} #{t2.name}"
	}
end

a = Mechanize.new
years = (2010..2014).to_a
years.each do |year|
	Game.where(:year => year).map(&:plays).each {|p| p.destroy_all}
	Game.where(:year => year).destroy_all

	BASE_URL = "http://stats.ncaa.org/team/inst_team_list?academic_year=#{year}&conf_id=-1&division=1&sport_code=MBB"
	a.get(BASE_URL) do |page|
		team_links = page.links.keep_if {|link| link.uri.to_s.include?("/team/index")}
		team_links.each do |team_link|
			begin
				team_page = team_link.click
			rescue
				puts "ERROR opening #{team_link.uri.to_s}"
				next
			end

			game_links = team_page.links.keep_if {|game_link| game_link.uri.to_s.include? "/game/index"}
			threads = []
			game_links.each do |game_link|
				threads << Thread.new do
					scrape_game_page(game_link, year)
				end
			end
			threads.each { |thread| thread.join }
			
			while $db_queue.size > 0
				transaction = $db_queue.pop()
				transaction.call()
			end
		end
	end
end
