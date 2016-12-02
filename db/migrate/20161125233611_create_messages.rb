class CreateMessages < ActiveRecord::Migration[5.0]
  def change
    create_table :messages do |t|
      t.string :message_sid
      t.string :body
      t.integer :status
      t.string :to_number
      t.integer :to_zip
      t.string :to_country
      t.string :from_number
      t.integer :from_zip
      t.string :from_country

      t.timestamps
    end
  end
end
