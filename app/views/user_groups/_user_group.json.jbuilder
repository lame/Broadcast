json.extract! user_group, :id, :active, :user_group_name, :created_at, :updated_at
json.url user_group_url(user_group, format: :json)