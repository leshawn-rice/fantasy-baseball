DROP DATABASE IF EXISTS baseball;
CREATE DATABASE baseball;

\c baseball;

CREATE TABLE teams (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  is_active BOOLEAN DEFAULT true,
  record TEXT
);

CREATE TABLE league_members (
  id TEXT PRIMARY KEY,
  team_id INTEGER REFERENCES teams NOT NULL,
  name TEXT NOT NULL,
  username TEXT
);