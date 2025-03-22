-- Drop and recreate the database
DROP DATABASE IF EXISTS baseball;
CREATE DATABASE baseball;

\c baseball;

-- Table: scoring_periods
-- Defines scoring periods (e.g. weeks) for tracking matchups and stats.
CREATE TABLE scoring_periods (
  id SERIAL PRIMARY KEY,
  season TEXT,
  period INTEGER,
  start_date DATE,
  end_date DATE
);

-- Table: teams
-- Fantasy teams for the single league.
CREATE TABLE teams (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  is_active BOOLEAN DEFAULT true,
  record TEXT
);

-- Table: league_members
-- Associates managers/owners with their fantasy teams.
CREATE TABLE league_members (
  id TEXT PRIMARY KEY,
  team_id INTEGER REFERENCES teams(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  username TEXT
);

-- Table: players
-- Stores player info from ESPN (or similar sources), including status and position.
CREATE TABLE players (
  id INTEGER PRIMARY KEY,  -- External player ID from API
  name TEXT NOT NULL,
  position TEXT,
  team TEXT,               -- MLB team abbreviation, for example
  status TEXT              -- e.g. Active, Injured
);

-- Table: rosters
-- Maps fantasy teams to the players on their roster.
CREATE TABLE rosters (
  id SERIAL PRIMARY KEY,
  team_id INTEGER REFERENCES teams(id) ON DELETE CASCADE,
  player_id INTEGER REFERENCES players(id) ON DELETE CASCADE,
  position_slot TEXT,      -- e.g. C, 1B, P, etc.
  added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: professional_teams
-- Stores real-life (e.g. MLB) team information.
CREATE TABLE professional_teams (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  abbreviation TEXT UNIQUE,
  city TEXT,
  conference TEXT,
  division TEXT
);

-- Table: pro_schedules
-- Stores professional team schedules (games, opponents, scores, etc.)
CREATE TABLE pro_schedules (
  id SERIAL PRIMARY KEY,
  pro_team_id INTEGER REFERENCES professional_teams(id) ON DELETE CASCADE,
  game_date DATE,
  opponent_team_id INTEGER REFERENCES professional_teams(id),
  home BOOLEAN,
  score JSONB,    -- Can include scores for pro team and opponent
  details JSONB   -- Any additional game details
);

-- Table: draft
-- Stores draft events for the season.
CREATE TABLE draft (
  id SERIAL PRIMARY KEY,
  season TEXT,
  draft_date DATE,
  details JSONB   -- Additional draft settings or notes
);

-- Table: draft_picks
-- Records individual draft picks, mapping teams to players.
CREATE TABLE draft_picks (
  id SERIAL PRIMARY KEY,
  draft_id INTEGER REFERENCES draft(id) ON DELETE CASCADE,
  pick_number INTEGER,
  round INTEGER,
  team_id INTEGER REFERENCES teams(id) ON DELETE CASCADE,
  player_id INTEGER REFERENCES players(id),
  details JSONB   -- Extra pick details if needed
);

-- Table: matchups
-- Records head-to-head matchups between teams for a given scoring period.
CREATE TABLE matchups (
  id SERIAL PRIMARY KEY,
  scoring_period_id INTEGER REFERENCES scoring_periods(id),
  team1_id INTEGER REFERENCES teams(id),
  team2_id INTEGER REFERENCES teams(id),
  team1_score NUMERIC,
  team2_score NUMERIC,
  game_date DATE,
  details JSONB   -- Could include additional metrics or notes
);

-- Table: standings
-- Stores current standings for each team in the league.
CREATE TABLE standings (
  id SERIAL PRIMARY KEY,
  team_id INTEGER REFERENCES teams(id),
  wins INTEGER DEFAULT 0,
  losses INTEGER DEFAULT 0,
  ties INTEGER DEFAULT 0,
  points NUMERIC DEFAULT 0,
  details JSONB   -- Additional ranking criteria or tie-breaker info
);

-- Table: player_stats
-- Records game-by-game header info for players.
CREATE TABLE player_stats (
  id SERIAL PRIMARY KEY,
  player_id INTEGER REFERENCES players(id) ON DELETE CASCADE,
  season TEXT,
  game_date DATE
);

-- Table: player_stat_entries
-- Stores individual stat key/value pairs for each game.
CREATE TABLE player_stat_entries (
  id SERIAL PRIMARY KEY,
  player_stats_id INTEGER REFERENCES player_stats(id) ON DELETE CASCADE,
  stat_key TEXT NOT NULL,
  stat_value NUMERIC
);

-- Table: player_cards
-- Stores snapshots of player card data (advanced stats, projections, etc.)
CREATE TABLE player_cards (
  id SERIAL PRIMARY KEY,
  player_id INTEGER REFERENCES players(id) ON DELETE CASCADE,
  card_data JSONB,        -- Raw JSON snapshot from API
  retrieval_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  scoring_period INTEGER   -- Which scoring period this snapshot is for
);

-- Table: transactions
-- Logs roster moves like acquisitions, drops, and trades.
CREATE TABLE transactions (
  id SERIAL PRIMARY KEY,
  team_id INTEGER REFERENCES teams(id) ON DELETE CASCADE,
  player_id INTEGER REFERENCES players(id),
  transaction_type TEXT,   -- e.g. 'acquisition', 'drop', 'trade', 'waiver'
  transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  details JSONB            -- Additional info about the transaction
);
