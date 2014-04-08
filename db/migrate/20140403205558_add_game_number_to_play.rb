class AddGameNumberToPlay < ActiveRecord::Migration
  def change
  	add_column :plays, :game_number, :integer
  end
end
