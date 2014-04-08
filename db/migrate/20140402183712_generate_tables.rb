class GenerateTables < ActiveRecord::Migration

  def up
  	create_table "games", force: true do |t|
  		t.integer "year"
	    t.date  "date"
	   	t.string "location"
  	end

  	create_table "teams", force: true do |t|
  		t.string "name"
  	end

  	create_table "team_years", force: true do |t|
  		t.integer "year"
  		t.integer "team_id"
  	end

	create_table "plays", force: true do |t|
		t.integer "game_id"
		t.integer "team_year_id"
		t.boolean "won"

		t.integer "fg"
		t.integer "fg_a"
		t.integer "three_fg"
		t.integer "three_fg_a"
		t.integer "ft"
		t.integer "ft_a"
		t.integer "pts"
		t.integer "off_reb"
		t.integer "def_reb"
		t.integer "reb"
		t.integer "ast"
		t.integer "turnovers"
		t.integer "steals"
		t.integer "blocks"
		t.integer "fouls"

		t.integer "o_fg"
		t.integer "o_fg_a"
		t.integer "o_three_fg"
		t.integer "o_three_fg_a"
		t.integer "o_ft"
		t.integer "o_ft_a"
		t.integer "o_pts"
		t.integer "o_off_reb"
		t.integer "o_def_reb"
		t.integer "o_reb"
		t.integer "o_ast"
		t.integer "o_turnovers"
		t.integer "o_steals"
		t.integer "o_blocks"
		t.integer "o_fouls"
	end
  end

  def down
  end
end
