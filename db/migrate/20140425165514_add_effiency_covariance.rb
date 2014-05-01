class AddEffiencyCovariance < ActiveRecord::Migration
  def change
  	add_column :cumulative_stats, :efficiency_covariance, :float
  end
end
