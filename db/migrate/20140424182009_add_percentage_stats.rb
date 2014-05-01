class AddPercentageStats < ActiveRecord::Migration
	def change
		rename_column :plays, :possesions, :possessions
		rename_column :plays, :scoring_possesions, :scoring_possessions
		rename_column :plays, :o_scoring_possesions, :o_scoring_possessions
	    rename_column :cumulative_stats, "o_scoring_possesions", "o_scoring_possessions" 
    	rename_column :cumulative_stats, "o_scoring_possesions_mean", "o_scoring_possessions_mean" 
    	rename_column :cumulative_stats, "o_scoring_possesions_min", "o_scoring_possessions_min" 
    	rename_column :cumulative_stats, "o_scoring_possesions_max", "o_scoring_possessions_max" 
    	rename_column :cumulative_stats, "o_scoring_possesions_variance", "o_scoring_possessions_variance" 
		rename_column :cumulative_stats, "scoring_possesions", "scoring_possessions"
	    rename_column :cumulative_stats, "scoring_possesions_mean", "scoring_possessions_mean"
	    rename_column :cumulative_stats, "scoring_possesions_min", "scoring_possessions_min"
	    rename_column :cumulative_stats, "scoring_possesions_max", "scoring_possessions_max"
	    rename_column :cumulative_stats, "scoring_possesions_variance", "scoring_possessions_variance"
	    rename_column :cumulative_stats, "possesions", "possessions"
	    rename_column :cumulative_stats, "possesions_mean", "possessions_mean"
	    rename_column :cumulative_stats, "possesions_max", "possessions_max"
	    rename_column :cumulative_stats, "possesions_min", "possessions_min"
	    rename_column :cumulative_stats, "possesions_variance", "possessions_variance"

	    stats = ["fg_pct", "three_fg_pct", "ft_pct"]
	    prefix = ["", "o_"]
	    suffix = ["", "_mean", "_min", "_max", "_variance"]

	    prefix.each do |pre|
	    	stats.each do |stat|
	    		suffix.each do |suff|
	    			add_column :cumulative_stats, "#{pre}#{stat}#{suff}", :float
	    		end
			    add_column :plays, "#{pre}#{stat}", :float
	    	end
	    end
	end
end
