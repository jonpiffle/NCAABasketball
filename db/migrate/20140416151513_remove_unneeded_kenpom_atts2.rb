class RemoveUnneededKenpomAtts2 < ActiveRecord::Migration
	 def change
		attributes = ["o_possesions"]
		suffixes = ["_mean", "_max", "_min", "_variance"]
		attributes.each do |attribute|
			remove_column :plays, "#{attribute}"
			suffixes.each do |suf|
				remove_column :cumulative_stats, "#{attribute}#{suf}"
			end
		end
	end
end
