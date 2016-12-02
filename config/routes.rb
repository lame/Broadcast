Rails.application.routes.draw do
  resources :phone_numbers
  resources :user_groups
  resources :users
  resources :messages
  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
end
