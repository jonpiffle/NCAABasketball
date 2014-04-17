class AddKenpomRatingsToGames < ActiveRecord::Migration
  def change
  	attributes = [
	  	"possesions",
	  	"offensive_efficiency",
	  	"defensive_efficiency",
	  	"effective_fg_pct",
	  	"turnover_pct",
	  	"offensive_reb_pct",
	  	"ft_rate",
	  	"adj_offensive_efficiency",
	  	"adj_defensive_efficiency",
	  	"pyth_expectation",
  	]

  	prefixes = ["", "o_"]
  	suffixes = ["_mean", "_max", "_min", "_variance"]

	remove_column :cumulative_stats, :adj_tempo

  	attributes.each do |attribute|
  		prefixes.each do |pre|
  			add_column :plays, "#{pre}#{attribute}", :float
  			suffixes.each do |suf|
	  			add_column :cumulative_stats, "#{pre}#{attribute}#{suf}", :float
  			end
  		end
  	end
  end
end
