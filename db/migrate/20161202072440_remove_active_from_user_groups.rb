class RemoveActiveFromUserGroups < ActiveRecord::Migration[5.0]
  def change
    remove_column :user_groups, :active, :boolean
  end
end
