from classes.espn.league_settings import LeagueSettings
from classes.espn.league_division import LeagueDivision
from classes.espn.league_member import LeagueMember
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
        self.settings = LeagueSettings(data=settings_data)
        self.divisions = {
            LeagueDivision(div) for div in self.settings.schedule.divisions
        }

    def parse_league_members(self):
        members_data = self._data.get("members", dict())
        self.members = set()
        for member in members_data:
            self.members.add(LeagueMember(data=member))

    def _print_settings(self):
        print(self.settings)
