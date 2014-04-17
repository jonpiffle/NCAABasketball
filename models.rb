require_relative 'database_configuration'

class Game < ActiveRecord::Base
    has_many :plays, :dependent => :destroy
    has_many :cumulative_stats, :through => :plays
    has_many :team_years, :through => :plays
    has_many :teams, :through => :team_years

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
    has_one :cumulative_stat, :dependent => :destroy
    belongs_to :prev_play, :class_name => "Play"
    belongs_to :next_play, :class_name => "Play"

    def date
        game.date
    end

    def previous_plays
        p_plays = []
        p_play = prev_play
        while p_play != nil
            p_plays << p_play
            p_play = p_play.prev_play
        end
        return p_plays
    end
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

    def last_play
        plays.where("next_play_id is null").first
    end

    def first_play
        plays.where("prev_play_id is null").first
    end

    def last_stat
        cumulative_stats.where("next_stat_id is null").first
    end

    def first_stat
        cumulative_stats.where("prev_stat_id is null").first
    end

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

    def opponents
        plays.map(&:game).map {|g| g.team_years.where("team_years.id != ?", self.id).first}
    end
end

class CumulativeStat < ActiveRecord::Base
    belongs_to :play
    has_one :game, :through => :play
    has_one :team_year, :through => :play
    has_one :team, :through => :play
    has_and_belongs_to_many :ranks
    belongs_to :prev_stat, :class_name => "CumulativeStat"
    belongs_to :next_stat, :class_name => "CumulativeStat"

    def sagarin_rank
        ranks.find_by(:system => "SAG")
    end

    def opponent_stat
        game.cumulative_stats.keep_if {|stat| stat != self}.first
    end

    def date
        game.date
    end

    def opponents
       team_year.games.where("date < ?", play.game.date).keep_if {|g| g.cumulative_stats.count > 0}.map {|g| g.teams.where("teams.id != ?", self.team.id).first }
    end

    def previous_stats
        p_stats = []
        p_stat = prev_stat
        while p_stat != nil
            p_stats << p_stat
            p_stat = p_stat.prev_stat
        end
        return p_stats
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