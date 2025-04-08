from classes.espn.league.settings import Settings
from classes.espn.league.division import Division
from classes.espn.league.member import Member
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
        self.parse_league_settings()
        self.parse_league_members()

    def parse_league_settings(self):
        settings_data = self._data.get("settings", dict())
        self.settings = Settings(data=settings_data)
        self.divisions = {
            Division(div._data) for div in self.settings.schedule.divisions
        }

    def write_to_database(self, engine, table=None, ignore_children=False):
        # We have to write divisions to the DB first because settings depends on the divisions existing
        for div in self.divisions:
            div.write_to_database(engine, table)
        super().write_to_database(engine, table, ignore_children)

    def parse_league_members(self):
        members_data = self._data.get("members", dict())
        self.members = set()
        for member in members_data:
            self.members.add(Member(data=member))

    def _print_settings(self):
        print(self.settings)
