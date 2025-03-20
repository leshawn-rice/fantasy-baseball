import os
import datetime
from classes.api import FantasyBaseballAPI
from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv()

    league_id = os.environ.get("league_id")
    espn_s2 = os.environ.get("espn_s2")
    swid = os.environ.get("swid")
    season = datetime.date.today().year

    api = FantasyBaseballAPI(
        season=season, league_id=league_id, espn_s2=espn_s2, swid=swid)

    league = api.get_league()

    league_members = [
        {
            "name": f"{m.get('firstName')} {m.get('lastName')}",
            "username": m.get("displayName"),
            "id": m.get("id"),
            "team_id": [x.get("id") for x in league.get("teams", list()) if x.get("primaryOwner") == m.get("id")].pop()
        } for m in league.get("members", list())
    ]

    print(league_members)
