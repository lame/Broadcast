class CreatePhoneNumbers < ActiveRecord::Migration[5.0]
  def change
    create_table :phone_numbers do |t|
      t.string :phone_number
      t.boolean :active

      t.timestamps
    end
  end
end
