class AddFourFactors < ActiveRecord::Migration
  def change
  	add_column :cumulative_stats, :possesions, :float
  	add_column :cumulative_stats, :offensive_efficiency, :float
  	add_column :cumulative_stats, :defensive_efficiency, :float
  	add_column :cumulative_stats, :effective_fg_pct, :float
  	add_column :cumulative_stats, :turnover_pct, :float
  	add_column :cumulative_stats, :offensive_reb_pct, :float
  	add_column :cumulative_stats, :ft_rate, :float
  	add_column :cumulative_stats, :adj_offensive_efficiency, :float
  	add_column :cumulative_stats, :adj_defensive_efficiency, :float
  	add_column :cumulative_stats, :adj_tempo, :float
  	add_column :cumulative_stats, :pyth_expectation, :float
  end
end
