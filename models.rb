require_relative 'database_configuration'

class Game < ActiveRecord::Base
    has_many :plays
    has_many :cumulative_stats, :through => :plays
    has_many :team_years, :through => :plays

    def loser
        plays.where(:won => false).map(&:team_year).first
    end

    def winner
        plays.where(:won => true).map(&:team_year).first
    end

    def w_score
        plays.where(:won => true).first.pts
    end

    def l_score
        plays.where(:won => false).first.pts
    end

    def description
        return "#{winner.team.name}\n#{loser.team.name}"
    end

    def safe_description
        return team_years.map(&:team).map(&:name).inject(&:+)
    end
end

class Play < ActiveRecord::Base
    belongs_to :team_year
    belongs_to :game
    has_one :team, :through => :team_year
    has_one :cumulative_stat
end

class Team < ActiveRecord::Base
    has_many :team_years, :dependent => :destroy
end

class TeamYear < ActiveRecord::Base
    belongs_to :team
    has_many :plays
    has_many :games, :through => :plays
    has_many :cumulative_stats, :through => :plays
    has_many :ranks

    def ordered_games
        games.sort {|a,b| a.date <=> b.date}
    end

    def ordered_stats
        cumulative_stats.sort {|a,b| a.game.date <=> b.game.date}
    end

    def ordered_plays
        plays.sort {|a,b| a.game.date <=> b.game.date}
    end

    def description
        team.nil? ? "" : "#{team.name} #{year}"
    end
end

class CumulativeStat < ActiveRecord::Base
    belongs_to :play
    has_one :game, :through => :play
    has_one :team_year, :through => :play
    has_one :team, :through => :play
    has_and_belongs_to_many :ranks

    def sagarin_rank
        ranks.find_by(:system => "SAG")
    end
end

class Rank < ActiveRecord::Base
    belongs_to :team_year
    has_and_belongs_to_many :cumulative_stats
end

class CumulativeStatsRank < ActiveRecord::Base
    belongs_to :cumulative_stat
    belongs_to :rank
end