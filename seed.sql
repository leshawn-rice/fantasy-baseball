-- Drop and recreate the database
DROP DATABASE IF EXISTS baseball;
CREATE DATABASE baseball;

\c baseball;

CREATE TABLE stats (
  id INTEGER PRIMARY KEY,
  shorthand TEXT NOT NULL,
  label TEXT NOT NULL
);

CREATE TABLE positions (
  id INTEGER PRIMARY KEY,
  shorthand TEXT NOT NULL,
  label TEXT NOT NULL
);

CREATE TABLE members (
  id UUID PRIMARY KEY,
  name TEXT NOT NULL,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  username TEXT NOT NULL
);

CREATE TABLE members_notification_settings (
  id UUID PRIMARY KEY,
  member_id UUID REFERENCES members(id) ON DELETE CASCADE,
  enabled BOOLEAN DEFAULT false,
  type TEXT NOT NULL
);

CREATE TABLE divisions (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  size INTEGER DEFAULT 1
);

CREATE TABLE teams (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL
);

/*
###################
# SETTINGS TABLES #
###################
*/

CREATE TABLE settings_finance (
  id SERIAL PRIMARY KEY,
  entry_fee FLOAT DEFAULT 0.0,
  misc_fee FLOAT DEFAULT 0.0,
  per_loss FLOAT DEFAULT 0.0,
  per_trade FLOAT DEFAULT 0.0,
  player_acquisition FLOAT DEFAULT 0.0,
  player_drop FLOAT DEFAULT 0.0,
  player_move_to_active FLOAT DEFAULT 0.0,
  player_move_to_ir FLOAT DEFAULT 0.0
);

CREATE TABLE settings_trade (
  id SERIAL PRIMARY KEY,
  allow_out_of_universe BOOLEAN DEFAULT false,
  deadline_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  max_trades INTEGER DEFAULT 0,
  revision_hours INTEGER DEFAULT 24,
  veto_votes_required INTEGER DEFAULT 1
);

CREATE TABLE settings_scoring (
  id SERIAL PRIMARY KEY,
  allow_out_of_position_scoring BOOLEAN DEFAULT false,
  scoring_type TEXT NOT NULL,
  home_team_bonus INTEGER DEFAULT 0,
  matchup_tie_rule TEXT NOT NULL,
  matchup_tie_rule_by INTEGER DEFAULT 1,
  player_rank_type TEXT NOT NULL,
  playoff_home_team_bonus INTEGER DEFAULT 0,
  playoff_matchup_tie_rule TEXT NOT NULL,
  playoff_matchup_tie_rule_by INTEGER DEFAULT 1
);

CREATE TABLE settings_scoring_items (
  id SERIAL PRIMARY KEY,
  settings_scoring_id INTEGER REFERENCES settings_scoring(id) ON DELETE CASCADE,
  is_reverse_item BOOLEAN DEFAULT false,
  league_ranking FLOAT DEFAULT 0.0,
  league_total FLOAT DEFAULT 0.0,
  points FLOAT DEFAULT 0.0,
  stat_id INTEGER REFERENCES stats(id) ON DELETE CASCADE
);

CREATE TABLE settings_scoring_items_point_overrides (
  id SERIAL PRIMARY KEY,
  settings_scoring_item_id INTEGER REFERENCES settings_scoring_items(id) ON DELETE CASCADE,
  key TEXT NOT NULL,
  value FLOAT DEFAULT 0.0
);

CREATE TABLE settings_draft (
  id SERIAL PRIMARY KEY,
  auction_budget INTEGER DEFAULT 0,
  available_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  is_trading_enabled BOOLEAN DEFAULT false,
  keeper_count INTEGER DEFAULT 0,
  keeper_count_future INTEGER DEFAULT 0,
  keeper_order_type TEXT NOT NULL,
  league_sub_type TEXT NOT NULL,
  order_type TEXT NOT NULL,
  time_per_selection INTEGER DEFAULT 1,
  type TEXT NOT NULL
);

CREATE TABLE settings_draft_pick_order (
  id SERIAL PRIMARY KEY,
  settings_draft_id INTEGER REFERENCES settings_draft(id) ON DELETE CASCADE,
  -- team_id INTEGER REFERENCES teams(id) ON DELETE CASCADE,
  position INTEGER NOT NULL
);

CREATE TABLE settings_acquisition (
  id SERIAL PRIMARY KEY,
  acquisition_budget INTEGER DEFAULT 0,
  acquisition_limit INTEGER DEFAULT -1,
  acquisition_type TEXT NOT NULL,
  final_place_transaction_eligible INTEGER DEFAULT 0,
  matchup_acquisition_limit FLOAT DEFAULT 0.0,
  minimum_bid INTEGER DEFAULT 0,
  waiver_hours INTEGER DEFAULT 24,
  waiver_process_hour INTEGER DEFAULT 0,
  is_using_acquisition_budget BOOLEAN DEFAULT false,
  is_transaction_locking_enabled BOOLEAN DEFAULT false,
  is_matchup_limit_per_scoring_period BOOLEAN DEFAULT false,
  is_waiver_order_reset BOOLEAN DEFAULT false
);

CREATE TABLE settings_acquisition_waiver_process_days (
  id SERIAL PRIMARY KEY,
  settings_acquisition_id INTEGER REFERENCES settings_acquisition(id) ON DELETE CASCADE,
  day TEXT NOT NULL
);

CREATE TABLE settings_roster (
  id SERIAL PRIMARY KEY,
  lineup_locktime_type TEXT NOT NULL,
  roster_locktime_type TEXT NOT NULL,
  move_limit INTEGER DEFAULT -1,
  is_bench_unlimited BOOLEAN DEFAULT false,
  is_using_undroppable_list BOOLEAN DEFAULT false
);

CREATE TABLE settings_roster_lineup_slot_counts (
  id SERIAL PRIMARY KEY,
  settings_roster_id INTEGER REFERENCES settings_roster(id) ON DELETE CASCADE,
  position_id INTEGER REFERENCES positions(id) ON DELETE CASCADE,
  slot_count INTEGER DEFAULT 0
);

CREATE TABLE settings_roster_position_limits (
  id SERIAL PRIMARY KEY,
  settings_roster_id INTEGER REFERENCES settings_roster(id) ON DELETE CASCADE,
  position_id INTEGER REFERENCES positions(id) ON DELETE CASCADE,
  position_limit INTEGER DEFAULT 0
);

CREATE TABLE settings_roster_lineup_slot_stat_limits (
  id SERIAL PRIMARY KEY,
  settings_roster_id INTEGER REFERENCES settings_roster(id) ON DELETE CASCADE,
  position_id INTEGER REFERENCES positions(id) ON DELETE CASCADE,
  stat_id INTEGER REFERENCES stats(id) ON DELETE CASCADE,
  stat_limit FLOAT DEFAULT 0.0
);

CREATE TABLE settings_roster_universe_ids (
  id SERIAL PRIMARY KEY,
  settings_roster_id INTEGER REFERENCES settings_roster(id) ON DELETE CASCADE,
  universe_id INTEGER DEFAULT 0
);

CREATE TABLE settings_schedule (
  id SERIAL PRIMARY KEY,
  matchup_period_count INTEGER DEFAULT 1,
  matchup_period_length INTEGER DEFAULT 1,
  period_type_id INTEGER DEFAULT 0,
  playoff_matchup_period_length INTEGER DEFAULT 1,
  playoff_team_count INTEGER DEFAULT 2,
  playoff_seeding_rule TEXT NOT NULL,
  playoff_seeding_rule_by INTEGER DEFAULT 0,
  is_playoff_reseed BOOLEAN DEFAULT false,
  is_variable_playoff_matchup_period_length BOOLEAN DEFAULT false
);

CREATE TABLE settings_schedule_matchup_periods (
  id SERIAL PRIMARY KEY,
  settings_schedule_id INTEGER REFERENCES settings_schedule(id) ON DELETE CASCADE,
  matchup_id INTEGER NOT NULL,
  period_id INTEGER NOT NULL
);

CREATE TABLE settings_schedule_divisions (
  id SERIAL PRIMARY KEY,
  settings_schedule_id INTEGER REFERENCES settings_schedule(id) ON DELETE CASCADE,
  division_id INTEGER REFERENCES divisions(id) ON DELETE CASCADE
);

CREATE TABLE settings (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  size INTEGER DEFAULT 1,
  restriction_type TEXT NOT NULL,
  is_public BOOLEAN DEFAULT false,
  is_customizable BOOLEAN DEFAULT false,
  finance_id INTEGER REFERENCES settings_finance(id) ON DELETE CASCADE,
  trade_id INTEGER REFERENCES settings_trade(id) ON DELETE CASCADE,
  scoring_id INTEGER REFERENCES settings_scoring(id) ON DELETE CASCADE,
  schedule_id INTEGER REFERENCES settings_schedule(id) ON DELETE CASCADE,
  roster_id INTEGER REFERENCES settings_roster(id) ON DELETE CASCADE,
  draft_id INTEGER REFERENCES settings_draft(id) ON DELETE CASCADE,
  acquisition_id INTEGER REFERENCES settings_acquisition(id) ON DELETE CASCADE
);