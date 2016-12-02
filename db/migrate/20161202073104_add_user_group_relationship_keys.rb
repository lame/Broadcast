class AddUserGroupRelationshipKeys < ActiveRecord::Migration[5.0]
  def change
  end
end

class UserGroup < ActiveRecord::Base
  has_one :phone_number
  has_many :users
end

class User < ActiveRecord::Base
  has_many :user_groups
end
