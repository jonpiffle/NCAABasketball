class AddIdToJoinTable < ActiveRecord::Migration
  def change
  	drop_table :cumulative_stats_ranks
  	
  	create_table :cumulative_stats_ranks do |t|
      t.integer :cumulative_stat_id
      t.integer :rank_id
    end
  end
end
