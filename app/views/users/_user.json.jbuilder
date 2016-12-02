json.extract! user, :id, :fname, :lname, :phone, :current_channels_increment, :active, :role, :created_at, :updated_at
json.url user_url(user, format: :json)