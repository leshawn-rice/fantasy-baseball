from classes.database import DatabaseEngine
from classes.api import FantasyBaseballAPI
from settings import PRO_TEAM_MAP, POSITION_MAP, UTIL_POSITIONS


class FantasyBaseballInterface:
    def __init__(self, league_id: str = None, espn_s2: str = None, swid: str = None, season: int = None, db_connection_string: str = None):
        self.league_id = league_id
        self.espn_s2 = espn_s2
        self.swid = swid
        self.season = season
        self.db_connection_string = db_connection_string
        self.initialize_tools()

    def initialize_tools(self):
        self.api = FantasyBaseballAPI(
            season=self.season,
            league_id=self.league_id,
            espn_s2=self.espn_s2,
            swid=self.swid
        )
        self.database = DatabaseEngine(
            connection_string=self.db_connection_string
        )
        self.database.start_session()

    def setup_league(self):
        # Fetch and set up all league-wide info.
        self.league = self.api.get_league()
        # self.league_teams = self.league.get("teams", [])
        # self.league_members = self.get_league_members()
        # self.rosters = self.setup_rosters()
        # self.draft = self.setup_draft()
        # self.matchups = self.setup_matchups()
        # self.standings = self.setup_standings()
        # self.pro_schedule = self.setup_pro_schedule()
        # self.players = self.setup_players()
        # self.player_cards = self.setup_player_cards()
        # self.player_stats = self.setup_player_stats([])

    def get_league_members(self):
        members = []
        for member in self.league.get("members", []):
            first_name = member.get("firstName")
            last_name = member.get("lastName")
            name = f"{first_name} {last_name}"
            username = member.get("displayName")
            member_id = member.get("id")
            # Determine team id by matching the member id to team.primaryOwner.
            team_ids = [team.get("id") for team in self.league_teams if team.get(
                "primaryOwner") == member_id]
            if team_ids:
                team_id = team_ids[0]
                members.append({
                    "name": name,
                    "username": username,
                    "id": member_id,
                    "team_id": team_id
                })
        return members

    def setup_rosters(self):
        # Assuming each team object contains a roster under the "roster" key.
        rosters = []
        for team in self.league_teams:
            team_id = team.get("id")
            # Depending on your API response, the roster may be nested under "roster" > "entries"
            roster_entries = team.get("roster", {}).get("entries", [])
            for entry in roster_entries:
                player = entry.get("player", {})
                roster_entry = {
                    "team_id": team_id,
                    "player_id": player.get("id"),
                    "position_slot": entry.get("lineupSlot", {}).get("abbreviation"),
                    # Additional info can be added here as needed.
                }
                rosters.append(roster_entry)
        return rosters

    def setup_draft(self):
        # Retrieve draft details from the API.
        draft_data = self.api.get_league_draft()
        draft = {
            "season": draft_data.get("season"),
            "draft_date": draft_data.get("draftDate"),
            "picks": []
        }
        # Assuming draft_data contains a list of picks.
        for pick in draft_data.get("picks", []):
            draft["picks"].append({
                "round": pick.get("round"),
                "pick_number": pick.get("pickNumber"),
                "team_id": pick.get("teamId"),
                "player_id": pick.get("playerId"),
                # Include more details if needed.
            })
        return draft

    def setup_matchups(self):
        # Extract matchup data. This assumes the league API includes matchup details.
        matchups = []
        # Some APIs return a current scoring period object.
        scoring_period = self.league.get("scoringPeriod", {})
        for matchup in self.league.get("matchups", []):
            matchups.append({
                "scoring_period_id": scoring_period.get("id"),
                "team1_id": matchup.get("team1", {}).get("id"),
                "team2_id": matchup.get("team2", {}).get("id"),
                "team1_score": matchup.get("team1", {}).get("score"),
                "team2_score": matchup.get("team2", {}).get("score"),
                "game_date": matchup.get("gameDate"),
                # Additional details can be added here.
            })
        return matchups

    def setup_standings(self):
        # Gather standings from each team’s record.
        standings = []
        for team in self.league_teams:
            record = team.get("record", {})
            standings.append({
                "team_id": team.get("id"),
                "wins": record.get("wins", 0),
                "losses": record.get("losses", 0),
                "ties": record.get("ties", 0),
                "points": record.get("points", 0),
                # Add any tie-breakers or extra metrics here.
            })
        return standings

    def setup_pro_schedule(self):
        # Retrieve professional team schedules.
        pro_schedule_data = self.api.get_pro_schedule()
        schedule = []
        if not isinstance(pro_schedule_data, list):
            pro_schedule_data = [pro_schedule_data]
        for game in pro_schedule_data:
            schedule.append({
                "pro_team_id": game.get("proTeamId"),
                "game_date": game.get("gameDate"),
                "opponent_team_id": game.get("opponentTeamId"),
                "home": game.get("home"),
                "score": game.get("score"),
                "details": game.get("details")
            })
        self.pro_schedule = schedule
        return schedule

    def setup_players(self):
        # Retrieve player information from the API.
        players_data = self.api.get_pro_players()
        players = []
        for player_data in players_data:
            player = player_data.get("player", dict())
            slots = player.get("eligibleSlots")
            # Convert position IDs to position names
            eligible_positions = [
                POSITION_MAP.get(slot, "").split("/") for slot in slots if POSITION_MAP.get(slot, "") not in UTIL_POSITIONS
            ]
            # Some duplicates due to "2B/SS" & "2B" eligibility, remove them
            eligible_positions = [
                pos for positions in eligible_positions for pos in positions]
            position = "/".join(list(set(eligible_positions))).strip("/")
            players.append({
                "id": player.get("id"),
                "name": player.get("fullName"),
                "position": position,
                "team": PRO_TEAM_MAP.get(player.get("proTeamId", 0)),
                "status": player.get("status")
            })
        self.players = players
        return players

    def setup_player_stats(self, stats_data):
        """
        Expects stats_data to be a list of dicts, each containing:
            - player_id
            - season
            - game_date
            - entries: list of { stat_key, stat_value }
        """
        self.player_stats = stats_data
        return stats_data

    def setup_player_cards(self, player_ids: list, max_scoring_period: int, additional_filters: list = None):
        # Retrieve player card snapshots.
        player_card_data = self.api.get_player_card(
            player_ids, max_scoring_period, additional_filters)
        cards = []
        # Adjust the following parsing as per the actual API response structure.
        for card in player_card_data.get("playerCards", []):
            cards.append({
                "player_id": card.get("playerId"),
                "card_data": card,
                "retrieval_date": card.get("retrievalDate"),
                "scoring_period": card.get("scoringPeriod")
            })
        self.player_cards = cards
        return cards

    def write_league_teams_db(self):
        for team in self.league_teams:
            team_row = {
                "id": team.get("id"),
                "name": team.get("name"),
                "is_active": team.get("isActive"),
                "record": f"{team.get('record', {}).get('overall', {}).get('wins')}-"
                          f"{team.get('record', {}).get('overall', {}).get('losses')}"
            }
            self.database.insert("teams", team_row)

    def write_league_members_db(self):
        for member in self.league_members:
            self.database.insert("league_members", member)

    def write_rosters_db(self):
        for roster in self.rosters:
            self.database.insert("rosters", roster)

    def write_draft_db(self):
        # Insert draft header first.
        draft_header = {
            "season": self.draft.get("season"),
            "draft_date": self.draft.get("draft_date"),
            "details": None  # Modify if you have extra details.
        }
        draft_id = self.database.insert("draft", draft_header)
        # Insert each pick.
        for pick in self.draft.get("picks", []):
            pick_row = {
                "draft_id": draft_id,
                "pick_number": pick.get("pick_number"),
                "round": pick.get("round"),
                "team_id": pick.get("team_id"),
                "player_id": pick.get("player_id"),
                "details": pick.get("details")
            }
            self.database.insert("draft_picks", pick_row)

    def write_matchups_db(self):
        for matchup in self.matchups:
            self.database.insert("matchups", matchup)

    def write_standings_db(self):
        for standing in self.standings:
            self.database.insert("standings", standing)

    def write_pro_schedule_db(self):
        for game in self.pro_schedule:
            self.database.insert("pro_schedules", game)

    def write_players_db(self):
        for player in self.players:
            self.database.insert("players", player)

    def write_player_cards_db(self):
        for card in self.player_cards:
            self.database.insert("player_cards", card)

    def write_player_stats_db(self):
        """
        For each stat record in self.player_stats, insert a header into player_stats and then
        each key/value pair into player_stat_entries.
        """
        for stat in self.player_stats:
            stat_header = {
                "player_id": stat.get("player_id"),
                "season": stat.get("season"),
                "game_date": stat.get("game_date")
            }
            stat_id = self.database.insert("player_stats", stat_header)
            for entry in stat.get("entries", []):
                entry_row = {
                    "player_stats_id": stat_id,
                    "stat_key": entry.get("stat_key"),
                    "stat_value": entry.get("stat_value")
                }
                self.database.insert("player_stat_entries", entry_row)
