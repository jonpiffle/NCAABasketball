class AddPrevNextToCumulativeStatsAndPlays < ActiveRecord::Migration
  def change
  	add_column :cumulative_stats, :next_stat_id, :integer
  	add_column :cumulative_stats, :prev_stat_id, :integer
  	add_column :plays, :next_play_id, :integer
  	add_column :plays, :prev_play_id, :integer
  end
end
