from enum import Enum
from classes.database import DatabaseEngine


class ESPNObject:
    database_table: str = None

    def serialize_for_db(self):
        db_serialized_object = {}
        for key, val in self.serialize().items():
            if isinstance(val, ESPNObject):
                continue
            elif isinstance(val, (list, set)):
                val = [
                    item for item in val if not isinstance(item, ESPNObject)]
            elif isinstance(val, dict):
                val = {
                    k: v for k, v in val.items() if not isinstance(v, ESPNObject)
                }
            if isinstance(val, (list, set, dict)) and not len(val):
                continue
            db_serialized_object[key] = val
        return db_serialized_object

    def serialize(self):
        serialized_object = {}
        for key, val in self.__dict__.items():
            if key.startswith("_"):
                continue
            serialized_object[key] = val
        return serialized_object

    def read_database_id(self, engine: DatabaseEngine, table: str = None, data: dict = None):
        if engine is None:
            return None

        if data.get("id", None) is not None:
            return data.get("id")
        try:
            item = engine.get_by_column_value_multiple(
                table_name=table, filter_dict=data
            )
            return item.id
        except Exception as exc:
            print(exc)

    def write_to_database(self, engine: DatabaseEngine, table: str = None):
        if engine is None:
            return None

        data = self.serialize()

        items_to_write_to_db = []

        # Process nested ESPNObject instances
        for key, val in list(data.items()):
            if isinstance(val, ESPNObject):
                items_to_write_to_db.append(val)
                del data[key]
            elif isinstance(val, (list, set)):
                for item in list(val):
                    if isinstance(item, ESPNObject):
                        items_to_write_to_db.append(item)
                        data[key].remove(item)
                if not data[key]:
                    del data[key]
            elif isinstance(val, dict):
                for subkey, subval in list(val.items()):
                    if isinstance(subval, ESPNObject):
                        items_to_write_to_db.append(subval)
                        del data[key][subkey]
                if not data[key]:
                    del data[key]

        # Insert this object's data into the database using the provided engine.
        # Here, we're assuming that 'engine' has an 'insert' method that takes
        # a table name and a dictionary of column data.
        table = self.database_table if table is None else table
        if hasattr(engine, "insert") and table is not None:
            try:
                engine.insert(table, data)
            except Exception as exc:
                print(
                    f"{self.__class__.__name__} failed to insert into {table} with values {data}\n{exc}\n\n")
        else:
            if table is None:
                print(f"Invalid Table {table}")
            else:
                print("Engine does not support an 'insert' operation")

        if not hasattr(self, "id"):
            self.id = self.read_database_id(engine, table, data)

        for item in items_to_write_to_db:
            item.write_to_database(engine)


class ESPNEnum(ESPNObject, Enum):
    """
    Base enumeration class for ESPN-related constants.

    This class extends Python's built-in Enum to include additional attributes for each member:

    - **id**: A unique integer identifier.
    - **shorthand**: A short string representation.
    - **label**: A descriptive label.

    It also provides a custom implementation for handling missing values via the
    :meth:`_missing_` method.
    """
    def __new__(cls, id, shorthand, label):
        """
        Create a new enum member with the specified id, shorthand, and label.

        :param id: The unique integer identifier for the enum member.
        :type id: int
        :param shorthand: The short string representation of the enum member.
        :type shorthand: str
        :param label: A descriptive label for the enum member.
        :type label: str
        :return: A new instance of the enum member.
        :rtype: ESPNEnum
        """
        obj = object.__new__(cls)
        obj._value_ = id
        obj.id = id
        obj.shorthand = shorthand
        obj.label = label
        return obj

    @classmethod
    def _missing_(cls, value):
        """
        Handle lookups for missing enum values.

        This method is invoked when a lookup for an enum member using a given value fails.
        It logs a warning message and returns the default member (``DEFAULT``) of the enumeration.

        :param value: The value that was not found in the enumeration.
        :type value: Any
        :return: The default enum member.
        :rtype: ESPNEnum
        """
        print(f"Warning: {value} is not a valid {cls.__name__}.")
        return cls.DEFAULT

    @classmethod
    def write_all_to_database(cls, engine):
        table = None

        if cls is Stat:
            table = "stats"
        if cls is Position:
            table = "positions"
        for member in cls:
            member.write_to_database(engine, table)


class Position(ESPNEnum):
    """
    Enumeration representing baseball positions.

    Each member represents a specific baseball position with an associated id,
    shorthand code, and descriptive label.
    """
    DEFAULT = (-1, "_", "DEFAULT")

    CATCHER = (0, "C", "Catcher")
    FIRST_BASE = (1, "1B", "First Baseman")
    SECOND_BASE = (2, "2B", "Second Baseman")
    THIRD_BASE = (3, "3B", "Third Baseman")
    SHORTSTOP = (4, "SS", "Shortstop")
    OUTFIELD = (5, "OF", "Outfielder")
    SECOND_BASE_SHORTSTOP = (6, "2B/SS", "Second Baseman/Shortstop")
    FIRST_BASE_THIRD_BASE = (7, "1B/3B", "First Baseman/Third Baseman")
    LEFT_FIELD = (8, "LF", "Left Fielder")
    CENTER_FIELD = (9, "CF", "Center Fielder")
    RIGHT_FIELD = (10, "RF", "Right Fielder")
    DESIGNATED_HITTER = (11, "DH", "Designated Hitter")
    UTILITY = (12, "UTIL", "Utility")
    PITCHER = (13, "P", "Pitcher")
    STARTING_PITCHER = (14, "SP", "Starting Pitcher")
    RELIEF_PITCHER = (15, "RP", "Relief Pitcher")
    BENCH = (16, "BE", "Bench")
    INJURED_LIST = (17, "IL", "Injured List")
    UNKNOWN = (18, "_", "Unknown")
    INFIELDER = (19, "IF", "Infielder")  # 1B/2B/SS/3B noted
    UNKNOWN_ALT = (21, "-", "Unknown Alt")
    DESIGNATED_HITTER_STARTING_PITCHER = (
        22, "DH/SP", "Designated Hitter/Starting Pitcher")


class Stat(ESPNEnum):
    # database_table = "stats"
    """
    Enumeration representing baseball statistics.

    Each member represents a specific baseball statistic with an associated id,
    shorthand code, and descriptive label.
    """
    DEFAULT = (-1, "DEF", "DEFAULT")

    AT_BATS = (0, "AB", "At Bats")
    HITS = (1, "H", "Hits")
    BATTING_AVG = (2, "AVG", "Batting Average")
    DOUBLES = (3, "2B", "Doubles")
    TRIPLES = (4, "3B", "Triples")
    HOME_RUNS = (5, "HR", "Home Runs")
    EXTRA_BASE_HITS = (6, "XBH", "Extra Base Hits")
    SINGLES = (7, "1B", "Singles")
    TOTAL_BASES = (8, "TB", "Total Bases")
    SLUGGING_PERCENT = (9, "SLG", "Slugging Percentage")
    WALKS = (10, "B_BB", "Base on Balls (Walks)")
    INTENTIONAL_WALKS = (11, "B_IBB", "Intentional Walks")
    HIT_BY_PITCH = (12, "HBP", "Hit By Pitch")
    SACRIFICE_FLY = (13, "SF", "Sacrifice Fly")
    SACRIFICE_HIT = (14, "SH", "Sacrifice Hit (Bunt)")
    SACRIFICES = (15, "SAC", "Total Sacrifices")
    PLATE_APPEARANCES = (16, "PA", "Plate Appearances")
    ON_BASE_PERCENTAGE = (17, "OBP", "On Base Percentage")
    ON_BASE_PLUS_SLUGGING = (18, "OPS", "On-base Plus Slugging")
    RUNS_CREATED = (19, "RC", "Runs Created")
    RUNS = (20, "R", "Runs")
    RUNS_BATTED_IN = (21, "RBI", "Runs Batted In")
    STOLEN_BASES = (23, "SB", "Stolen Bases")
    CAUGHT_STEALING = (24, "CS", "Caught Stealing")
    NET_STEALS = (25, "SB-CS", "Net Steals (Steals minus Caught Stealing)")
    GROUNDED_DOUBLE_PLAY = (26, "GDP", "Grounded Into Double Play")
    BATTER_STRIKE_OUTS = (27, "B_SO", "Strikeouts (Batter)")
    PITCHES_SEEN = (28, "PS", "Pitches Seen")
    PITCHES_PER_APPEARANCE = (29, "PPA", "Pitches Per Appearance")
    CYCLE = (31, "CYC", "Cycle")
    GAMES_PITCHED = (32, "GP", "Games Pitched")
    GAMES_STARTED = (33, "GS", "Games Started")
    OUTS = (34, "OUTS", "Outs Recorded")
    TOTAL_BATTERS_FACED = (35, "TBF", "Total Batters Faced")
    PITCHES = (36, "P", "Pitches")
    HITS_ALLOWED = (37, "P_H", "Hits Allowed")
    OPPONENT_BATTING_AVG = (38, "OBA", "Opponent Batting Average")
    WALKS_ALLOWED = (39, "P_BB", "Walks Allowed")
    INTENTIONAL_WALKS_ALLOWED = (40, "P_IBB", "Intentional Walks Allowed")
    WHIP = (41, "WHIP", "Walks plus Hits per Inning Pitched")
    PITCHER_HIT_BY_PITCH = (42, "HBP", "Hit By Pitch (Pitcher)")
    OPPONENT_ON_BASE_PERCENTAGE = (43, "OOBP", "Opponent On-base Percentage")
    RUNS_ALLOWED = (44, "P_R", "Runs Allowed")
    EARNED_RUNS = (45, "ER", "Earned Runs")
    HOME_RUNS_ALLOWED = (46, "P_HR", "Home Runs Allowed")
    EARNED_RUN_AVERAGE = (47, "ERA", "Earned Run Average")
    STRIKE_OUTS = (48, "K", "Strikeouts")
    STEIKE_OUTS_PER_9_INNINGS = (49, "K/9", "Strikeouts per 9 Innings")
    WILD_PITCHES = (50, "WP", "Wild Pitches")
    BLOCKED_PITCHES = (51, "BLK", "Blocked Pitches")
    PICKOFFS = (52, "PK", "Pickoffs")
    WINS = (53, "W", "Wins")
    LOSSES = (54, "L", "Losses")
    WIN_PERCENTAGE = (55, "WPCT", "Win Percentage")
    SAVE_OPPORTUNITIES = (56, "SVO", "Save Opportunities")
    SAVES = (57, "SV", "Saves")
    BLOWN_SAVES = (58, "BLSV", "Blown Saves")
    SAVE_PERCENTAGE = (59, "SV%", "Save Percentage")
    HOLDS = (60, "HLD", "Holds")
    COMPLETE_GAMES = (62, "CG", "Complete Games")
    QUALITY_STARTS = (63, "QS", "Quality Starts")
    NO_HITTER = (65, "NH", "No-hitter")
    PERFECT_GAME = (66, "PG", "Perfect Game")
    TOTAL_CHANCES = (67, "TC", "Total Chances")
    PUTOUTS = (68, "PO", "Putouts")
    ASSISTS = (69, "A", "Assists")
    OUTFIELD_ASSISTS = (70, "OFA", "Outfield Assists")
    FIELDING_PERCENTAGE = (71, "FPCT", "Fielding Percentage")
    ERRORS = (72, "E", "Errors")
    DOUBLE_PLAYS_TURNED = (73, "DP", "Double Plays Turned")
    BATTER_GAMES_WON = (74, "B_G_W", "Batter Games Won")
    BATTER_GAMES_LOST = (75, "B_G_L", "Batter Games Lost")
    PITCHER_GAMES_WON = (76, "P_G_W", "Pitcher Games Won")
    PITCHER_GAMES_LOST = (77, "P_G_L", "Pitcher Games Lost")
    GAMES_PLAYED = (81, "G", "Games Played")
    STRIKEOUTS_PER_WALK = (82, "K/BB", "Strikeout-to-Walk Ratio")
    SAVES_AND_HOLDS = (83, "SVHD", "Saves + Holds")
    STARTER = (99, "STARTER", "Starter")
