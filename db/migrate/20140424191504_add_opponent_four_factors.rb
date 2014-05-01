class AddOpponentFourFactors < ActiveRecord::Migration
	def change
		add_column :cumulative_stats, :o_effective_fg_pct, :float
		add_column :cumulative_stats, :o_turnover_pct, :float
		add_column :cumulative_stats, :o_offensive_reb_pct, :float
		add_column :cumulative_stats, :o_ft_rate, :float
	end
end
