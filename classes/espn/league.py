from classes.espn.league_settings import LeagueSettings


class League(object):
    def __init__(self, data: dict = None):
        self.data = data

    def parse_league_data(self):
        self.id = self.data.get("id", None)
        self.season_id = self.data.get("seasonId", None)
        self.segment_id = self.data.get("segmentId", None)
        self.scoring_period_id = self.data.get("scoringPeriodId", None)
        self.game_id = self.data.get("gameId", None)
        settings_data = self.data.get("settings", dict())
        self.settings = LeagueSettings(data=settings_data)

    def _print_settings(self):
        print(self.settings)
