class ApplicationController < ActionController::Base
  protect_from_forgery with: :exception

  def index
    puts "got it!"
  end
end
