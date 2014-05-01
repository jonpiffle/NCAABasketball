class AddNewDeanOliverStats < ActiveRecord::Migration
	def change
		stats = ["floor_pct", "field_pct", "play_pct", "scoring_possesions", "plays"]
		prefixes = ["", "o_"]
		suffixes = ["", "_mean", "_min", "_max", "_variance"]

		prefixes.each do |pre|
			stats.each do |stat|
				suffixes.each do |suff|
					add_column :cumulative_stats, "#{pre}#{stat}#{suff}", :float
				end
				add_column :plays, "#{pre}#{stat}", :float
			end
		end
	end
end
