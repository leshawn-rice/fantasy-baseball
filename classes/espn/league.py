from classes.espn.settings import Settings
from classes.espn.division import Division
from classes.espn.member import Member
from classes.espn.team import Team
from classes.espn.base import ESPNObject


class League(ESPNObject):
    def __init__(self, data: dict = None):
        self._data = data

    def parse_league_data(self):
        self.id = self._data.get("id", None)
        self.season_id = self._data.get("seasonId", None)
        self.segment_id = self._data.get("segmentId", None)
        self.scoring_period_id = self._data.get("scoringPeriodId", None)
        self.game_id = self._data.get("gameId", None)
        self.parse_league_teams()
        self.parse_league_settings()
        self.parse_league_members()

    def write_to_database(self, engine, table=None, ignore_children=False):
        # We have to write divisions to the DB first because (settings, teams) depends on the divisions existing
        # we have to write members before teams
        # we have to write teams before i.e. settings
        for div in self.divisions:
            div.write_to_database(engine, table)
        for member in self.members:
            member.write_to_database(engine, table)
        for team in self.teams:
            team.write_to_database(engine, table)
        super().write_to_database(engine, table, ignore_children)

    def parse_league_settings(self):
        settings_data = self.read_data("settings", dict())
        self.settings = Settings(data=settings_data)
        self.divisions = {
            Division(div._data) for div in self.settings.schedule.divisions
        }

    def parse_league_teams(self):
        teams_data = self.read_data("teams", list())
        self.teams = {
            Team(data=team_data) for team_data in teams_data
        }

    def parse_league_members(self):
        members_data = self.read_data("members", dict())
        self.members = {
            Member(member) for member in members_data
        }

    def _print_settings(self):
        print(self.settings)

    def _print_teams(self):
        print(self.teams)
