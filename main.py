import os
import datetime
from classes.interface import FantasyBaseballInterface
from dotenv import load_dotenv
from classes.espn.league import League

if __name__ == "__main__":
    load_dotenv()

    db_connection_string = os.environ.get("db_connection_string")
    league_id = os.environ.get("league_id")
    espn_s2 = os.environ.get("espn_s2")
    swid = os.environ.get("swid")
    season = datetime.date.today().year

    interface = FantasyBaseballInterface(
        league_id=league_id,
        espn_s2=espn_s2,
        swid=swid,
        season=season,
        db_connection_string=db_connection_string
    )

    interface.setup_league()
    l = interface.league

    league = League(data=l)
    league.parse_league_data()

    # print(league.settings.finance.entry_fee)
    # print(league.settings.league_name)
    # print(league.settings.draft.type)
    print(league.settings.scoring.scoring_items)

    interface.database.end_session()
