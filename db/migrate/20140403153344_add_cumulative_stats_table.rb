class AddCumulativeStatsTable < ActiveRecord::Migration
  def up
  	create_table "cumulative_stats", force: true do |t|
  		stats = ["fg", "fg_a", "three_fg", "three_fg_a", "ft", "ft_a", "pts", "off_reb", "def_reb", "reb", "ast", "turnovers", "steals", "blocks", "fouls"]
  		prefixes = ["", "o_"]
  		suffixes = ["", "_mean", "_min", "_max", "_variance"]
  		stats.each do |stat|
  			prefixes.each do |prefix|
  				suffixes.each do |suffix|
  					t.integer "#{prefix}#{stat}#{suffix}"
  				end
  			end
  		end
  	end
  end

  def down
  end
end
