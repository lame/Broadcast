# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# Note that this schema.rb definition is the authoritative source for your
# database schema. If you need to create the application database on another
# system, you should be using db:schema:load, not running all the migrations
# from scratch. The latter is a flawed and unsustainable approach (the more migrations
# you'll amass, the slower it'll run and the greater likelihood for issues).
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 20161202073104) do

  create_table "messages", force: :cascade do |t|
    t.string   "message_sid"
    t.string   "body"
    t.integer  "status"
    t.string   "to_number"
    t.integer  "to_zip"
    t.string   "to_country"
    t.string   "from_number"
    t.integer  "from_zip"
    t.string   "from_country"
    t.datetime "created_at",   null: false
    t.datetime "updated_at",   null: false
    t.string   "message_type"
    t.index ["message_type", "message_sid"], name: "index_messages_on_message_type_and_message_sid"
  end

  create_table "phone_numbers", force: :cascade do |t|
    t.string   "phone_number"
    t.boolean  "active"
    t.datetime "created_at",   null: false
    t.datetime "updated_at",   null: false
  end

  create_table "user_groups", force: :cascade do |t|
    t.string   "user_group_name"
    t.datetime "created_at",      null: false
    t.datetime "updated_at",      null: false
  end

  create_table "users", force: :cascade do |t|
    t.string   "fname"
    t.string   "lname"
    t.string   "phone"
    t.integer  "current_channels_increment"
    t.boolean  "active"
    t.integer  "role"
    t.datetime "created_at",                 null: false
    t.datetime "updated_at",                 null: false
  end

end
