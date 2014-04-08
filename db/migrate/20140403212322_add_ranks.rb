class AddRanks < ActiveRecord::Migration
  def change
  	create_table "ranks", force: true do |t|
  		t.integer :team_year_id
  		t.integer :year
  		t.date :date
  		t.integer :num
  		t.string :system
  	end

  	create_table :cumulative_stats_ranks, id: false do |t|
      t.integer :cumulative_stat_id
      t.integer :rank_id
    end
  end
end
