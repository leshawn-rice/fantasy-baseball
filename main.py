import os
import datetime
from classes.api import FantasyBaseballAPI
from dotenv import load_dotenv


def get_league_members(league, teams):
    league_members = []
    for member in league.get("members", list()):
        first_name = member.get("firstName")
        last_name = member.get("lastName")
        name = f"{first_name} {last_name}"
        username = member.get("displayName")
        id = member.get("id")
        team_id = [
            team.get("id") for team in teams if team.get("primaryOwner") == id
        ].pop()

        league_members.append(
            {"name": name, "username": username, "id": id, "team_id": team_id})

    return league_members


if __name__ == "__main__":
    load_dotenv()

    league_id = os.environ.get("league_id")
    espn_s2 = os.environ.get("espn_s2")
    swid = os.environ.get("swid")
    season = datetime.date.today().year

    api = FantasyBaseballAPI(
        season=season, league_id=league_id, espn_s2=espn_s2, swid=swid)

    league = api.get_league()
    teams = league.get("teams", list())

    league_members = get_league_members(league, teams)
    print(league_members)
