class CreateUserGroups < ActiveRecord::Migration[5.0]
  def change
    create_table :user_groups do |t|
      t.boolean :active
      t.string :user_group_name

      t.timestamps
    end
  end
end
