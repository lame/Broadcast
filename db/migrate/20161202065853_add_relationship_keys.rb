class AddRelationshipKeys < ActiveRecord::Migration[5.0]
  def change
    add_column :messages, :message_type, :string
    add_index :messages, [:message_type, :message_sid]
  end
end

class Message < ActiveRecord::Base
  belongs_to :messageable, polymorphic: true
end

class User < ActiveRecord::Base
  has_many :messages, as: :messagable
end

class UserGroup < ActiveRecord::Base
  has_many :messages, as: :messagable
end
