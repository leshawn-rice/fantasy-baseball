from classes.database import DatabaseEngine
from classes.api import FantasyBaseballAPI


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
        self.league = self.api.get_league()
        self.league_teams = self.league.get("teams", list())
        self.get_league_members()

    def get_league_members(self):
        self.league_members = []
        for member in self.league.get("members", list()):
            first_name = member.get("firstName")
            last_name = member.get("lastName")
            name = f"{first_name} {last_name}"
            username = member.get("displayName")
            id = member.get("id")
            team_id = [
                team.get("id") for team in self.league_teams if team.get("primaryOwner") == id
            ].pop()

            self.league_members.append(
                {"name": name, "username": username, "id": id, "team_id": team_id})

    def write_league_teams_db(self):
        for team in self.league_teams:
            team_row = {
                "id": team.get("id"),
                "name": team.get("name"),
                "is_active": team.get("isActive"),
                "record": f"{team.get('record', {}).get('overall', {}).get('wins')}-{team.get('record', {}).get('overall', {}).get('losses')}"
            }
            self.database.insert("teams", team_row)

    def write_league_members_db(self):
        for member in self.league_members:
            self.database.insert("league_members", member)
