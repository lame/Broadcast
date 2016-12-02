class CreateUsers < ActiveRecord::Migration[5.0]
  def change
    create_table :users do |t|
      t.string :fname
      t.string :lname
      t.string :phone
      t.integer :current_channels_increment
      t.boolean :active
      t.integer :role

      t.timestamps
    end
  end
end
