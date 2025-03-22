import os
import datetime
from classes.interface import FantasyBaseballInterface
from dotenv import load_dotenv

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
    interface.write_league_teams_db()
    interface.write_league_members_db()
    interface.write_rosters_db()
    interface.write_draft_db()
    interface.write_matchups_db()
    interface.write_standings_db()
    interface.write_pro_schedule_db()
    interface.write_players_db()
    # interface.write_player_cards_db()
    # interface.write_player_stats_db()
    interface.database.end_session()
