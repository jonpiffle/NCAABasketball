require 'rubygems'
require 'active_record'

ActiveRecord::Base.establish_connection(
  :adapter => 'postgresql',
  :pool => 500,
  :timeout => 50000,
  :encoding => 'unicode',
  :database => 'ncaa_basketball',
  :host => 'localhost',
  :username => 'piffle',
  :password => 'piffle'
)