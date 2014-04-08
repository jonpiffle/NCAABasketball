class AddPlayIdToCumulativeStat < ActiveRecord::Migration
  def change
  	add_column :cumulative_stats, :play_id, :integer
  end
end
