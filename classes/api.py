import requests
import json
from collections import defaultdict

# TODO: Put this in a config
VALID_VIEWS = [
    "mTeam",
    "mBoxscore",
    "mRoster",
    "mSettings",
    "kona_player_info",
    "player_wl",
    "mSchedule",
    "mMatchup",
    "mStandings",
    "proTeamSchedules_wl",
    "mDraftDetail",
    "kona_league_messageboard",
    "kona_playercard",
]

MAX_API_LIMIT = 3500


class FantasyBaseballAPI:
    def __init__(self, is_private: bool = True, season: str = None, league_id: str = None, espn_s2: str = None, swid: str = None):
        self.season = season
        self.league_id = league_id
        self.fantasy_url = f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/flb/seasons/{self.season}/segments/0/leagues/{self.league_id}"
        self.initialize_session(is_private=is_private,
                                espn_s2=espn_s2, swid=swid)

    def validate_set_cookies(self, is_private: bool = True, espn_s2: str = None, swid: str = None):
        if not is_private:
            return
        if not espn_s2:
            raise ValueError(
                "espn_s2 is required when is_private is set to `True`")
        if not swid:
            raise ValueError(
                "swid is required when is_private is set to `True`")
        self.session.cookies.set("espn_s2", espn_s2)
        self.session.cookies.set("SWID", swid)

    def initialize_session(self, is_private: bool = True, espn_s2: str = None, swid: str = None):
        self.session = requests.Session()
        self.validate_set_cookies(is_private=is_private,
                                  espn_s2=espn_s2, swid=swid)

    def send_request(self, endpoint: str = "", params: dict = None, headers: dict = None):
        url = f"{self.fantasy_url}/{endpoint}".strip("/")
        response = self.session.get(url, params=params, headers=headers)
        return response.json()

    def get_league(self):
        """Gets all of the leagues initial data (teams, roster, matchups, settings)"""
        params = {
            "view": ["mTeam", "mRoster", "mMatchup", "mSettings", "mStandings"]
        }
        data = self.send_request(params=params)
        return data

    def get_league_settings(self):
        params = {
            "view": "mSettings"
        }
        data = self.send_request(params=params)
        return data

    def get_pro_schedule(self):
        """Gets the current sports professional team schedules"""
        params = {
            "view": "proTeamSchedules_wl"
        }
        data = self.send_request(params=params)
        return data

    def get_pro_players(self):
        """Gets the current sports professional players"""
        params = {
            "view": ["players_wl", "kona_player_info"]
        }
        # This has no effect
        filters = {"filterActive": {"value": True}}
        headers = {"x-fantasy-filter": json.dumps(filters)}
        data = self.send_request(
            endpoint="players", params=params, headers=headers)
        return data

    def get_player_info(self):
        params = {
            "view": "kona_player_info"
        }
        filters = {"player": {"value": True}}
        headers = {"x-fantasy-filter": json.dumps(filters)}
        data = self.send_request(
            endpoint="players", params=params, headers=headers)
        return data

    def set_player_filters(self, filters: dict = defaultdict(dict), values: dict = defaultdict(dict)):
        filters["players"] = {**filters["players"], **values}

    def get_players(self, filters: dict = defaultdict(dict)):
        params = {
            "view": "kona_player_info"
        }
        limit = MAX_API_LIMIT
        offset = 0
        sort_perc_owned = {
            "sortPriority": 2, "sortAsc": False
        }
        self.set_player_filters(
            filters, {"limit": limit, "offset": offset, "sortPercOwned": sort_perc_owned})
        headers = {"x-fantasy-filter": json.dumps(filters)}
        data = self.send_request(params=params, headers=headers)
        players = list()
        while len(data.get("players", list())):
            players += data.get("players", list())
            offset = offset + limit
            self.set_player_filters(filters, {"offset": offset})
            headers = {"x-fantasy-filter": json.dumps(filters)}
            data = self.send_request(params=params, headers=headers)
        return players

    def get_free_agent_players(self):
        filters = {
            "players": {
                "filterStatus": {"value": ["FREEAGENT"]}
            }
        }
        return self.get_players(filters=filters)

    def get_players_on_team(self):
        filters = {
            "players": {
                "filterStatus": {"value": ["ONTEAM"]}
            }
        }
        return self.get_players(filters=filters)

    def get_player_info_by_id(self):
        params = {
            "view": "kona_player_info"
        }
        filters = {"player": {"value": True}}
        headers = {"x-fantasy-filter": json.dumps(filters)}
        data = self.send_request(
            endpoint="players", params=params, headers=headers)
        return data

    def get_league_draft(self):
        """Gets the leagues draft"""
        params = {
            "view": "mDraftDetail",
        }
        data = self.send_request(params=params)
        return data

    def get_player_card(self, playerIds: list[int], max_scoring_period: int, additional_filters: list = None):
        """Gets the player card"""
        params = {"view": "kona_playercard"}

        additional_value = ["00{}".format(self.year), "10{}".format(self.year)]
        if additional_filters:
            additional_value += additional_filters

        filters = {"players": {"filterIds": {"value": playerIds}, "filterStatsForTopScoringPeriodIds": {
            "value": max_scoring_period, "additionalValue": additional_value}}}
        headers = {"x-fantasy-filter": json.dumps(filters)}

        data = self.send_request(params=params, headers=headers)
        return data
