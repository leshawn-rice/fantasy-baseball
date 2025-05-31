from typing import Any
from utilities.espn import get_position, get_stat, convert_epoch_to_date
from classes.espn.base import ESPNObject, Position, Stat


class SettingsObject(ESPNObject):
    default_read_value = None

    """
    Base class for league settings objects.

    This class provides common functionality for reading and parsing data from a dictionary.
    Subclasses should override :meth:`parse_data` to implement custom parsing logic.
    """

    def __init__(self, data: dict = None, parse_data: bool = True):
        """
        Initialize a new SettingsObject instance.

        :param data: Dictionary containing configuration data.
        :type data: dict, optional
        :param parse_data: If True, automatically parse the data by calling :meth:`parse_data`.
        :type parse_data: bool, optional
        """
        self._data = data
        if parse_data:
            self.parse_data()


class SettingsObjectValue(SettingsObject):
    _parent_id_attr = "settings_id"

    def write_to_database(self, engine, table=None, ignore_children=False):
        self.set_parent_id(engine, self._parent_id_attr)
        super().write_to_database(engine, table)


class FinanceSettings(SettingsObject):
    _database_table = "settings_finance"
    """
    Class representing league finance settings.

    Parses financial settings such as entry fees, trade fees, and player-related fees.
    """
    default_read_value = 0.0

    def __init__(self, data: dict = None, parse_data: bool = True):
        super().__init__(data=data, parse_data=parse_data)

    def parse_data(self):
        self.entry_fee = self.read_data("entryFee")
        self.misc_fee = self.read_data("miscFee")
        self.per_loss = self.read_data("perLoss")
        self.per_trade = self.read_data("perTrade")
        self.player_acquisition = self.read_data("playerAcquisition")
        self.player_drop = self.read_data("playerDrop")
        self.player_move_to_active = self.read_data("playerMoveToActive")
        self.player_move_to_ir = self.read_data("playerMoveToIR")


class AcquisitionSettingsWaiverProcessDays(SettingsObjectValue):
    _database_table = "settings_acquisition_waiver_process_days"
    _parent_id_attr = "settings_acquisition_id"

    def __init__(self, day: str = None, acquisition_settings: Any = None):
        self.day = day
        self._parent = acquisition_settings


class AcquisitionSettings(SettingsObject):
    _database_table = "settings_acquisition"
    """
    Class representing league acquisition settings.

    Parses settings related to player acquisitions including budgets, limits, waiver rules,
    and transaction locking.
    """

    def __init__(self, data: dict = None, parse_data: bool = True):
        super().__init__(data=data, parse_data=parse_data)

    def parse_data(self):
        self.acquisition_budget = self.read_data("acquisitionBudget")
        self.acquisition_limit = self.read_data("acquisitionLimit")
        self.acquisition_type = self.read_data("acquisitionType")
        self.final_place_transaction_eligible = self.read_data(
            "finalPlaceTransactionEligible")
        self.matchup_acquisition_limit = self.read_data(
            "matchupAcquisitionLimit")
        self.minimum_bid = self.read_data("minimumBid")
        self.waiver_hours = self.read_data("waiverHours")
        self.waiver_process_days = [
            AcquisitionSettingsWaiverProcessDays(day, acquisition_settings=self) for day in self.read_data("waiverProcessDays", list())
        ]
        self.waiver_process_hour = self.read_data("waiverProcessHour")
        self.parse_boolean_data()

    def parse_boolean_data(self):
        self.is_transaction_locking_enabled = self.read_data(
            "transactionLockingEnabled", False)
        self.is_matchup_limit_per_scoring_period = self.read_data(
            "matchupLimitPerScoringPeriod", False)
        self.is_using_acquisition_budget = self.read_data(
            "isUsingAcuisitionBudget", False)
        self.is_waiver_order_reset = self.read_data("waiverOrderReset", False)


class DraftSettingsPickOrder(SettingsObjectValue):
    _database_table = "settings_draft_pick_order"
    _parent_id_attr = "settings_draft_id"

    def __init__(self, team_id: int = None, position: int = None, draft_settings: Any = None):
        self.position = position
        # self.team_id = team_id
        self._parent = draft_settings


class DraftSettings(SettingsObject):
    _database_table = "settings_draft"

    """
    Class representing league draft settings.

    Parses draft configuration settings such as auction budgets, draft dates,
    keeper counts, and order types.
    """

    def __init__(self, data: dict = None, parse_data: bool = True):
        super().__init__(data=data, parse_data=parse_data)

    def parse_data(self):
        self.auction_budget = self.read_data("auctionBudget")
        self.keeper_count = self.read_data("keeperCount")
        self.keeper_count_future = self.read_data("keeperCountFuture")
        self.keeper_order_type = self.read_data("keeperOrderType")
        self.league_sub_type = self.read_data("leagueSubType")
        self.order_type = self.read_data("orderType")
        self.pick_order = [
            DraftSettingsPickOrder(id, pos, draft_settings=self) for pos, id in enumerate(self.read_data("pickOrder", list()))
        ]
        self.time_per_selection = self.read_data("timePerSelection")
        self.type = self.read_data("type")
        self.parse_boolean_data()
        self.parse_date_data()

    def parse_boolean_data(self):
        self.is_trading_enabled = self.read_data("isTradingEnabled", False)

    def parse_date_data(self):
        self.available_date = convert_epoch_to_date(
            self.read_data("availableDate"))
        self.date = convert_epoch_to_date(self.read_data("date"))


class RosterSettingsLineupSlotCounts(SettingsObjectValue):
    _database_table = "settings_roster_lineup_slot_counts"
    _parent_id_attr = "settings_roster_id"

    def __init__(self, position: Position = None, slot_count: int = 0, roster_settings: Any = None):
        self.position_id = position.id
        self.slot_count = slot_count
        self._parent = roster_settings


class RosterSettingsPositionLimits(SettingsObjectValue):
    _database_table = "settings_roster_position_limits"
    _parent_id_attr = "settings_roster_id"

    def __init__(self, position: Position = None, position_limit: int = 0, roster_settings: Any = None):
        self.position_id = position.id
        self.position_limit = position_limit
        self._parent = roster_settings


class RosterSettingsLineupSlotStatLimits(SettingsObjectValue):
    _database_table = "settings_roster_lineup_slot_stat_limits"
    _parent_id_attr = "settings_roster_id"

    def __init__(self, position: Position = None, stat: Stat = None, stat_limit: int = 0, roster_settings: Any = None):
        self.position_id = position.id
        self.stat_id = stat.id
        self.stat_limit = stat_limit
        self._parent = roster_settings


class RosterSettingsUniverseIds(SettingsObjectValue):
    _database_table = "settings_roster_universe_ids"
    _parent_id_attr = "settings_roster_id"

    def __init__(self, universe_id: int = 0, roster_settings: Any = None):
        self.universe_id = universe_id
        self._parent = roster_settings


class RosterSettings(SettingsObject):
    _database_table = "settings_roster"

    """
    Class representing league roster settings.

    Parses settings related to lineup lock times, move limits, roster limits, and associated
    position and slot configurations.
    """

    def __init__(self, data: dict = None, parse_data: bool = True):
        super().__init__(data=data, parse_data=parse_data)

    def parse_data(self):
        self.lineup_locktime_type = self.read_data("lineupLocktimeType")
        self.move_limit = self.read_data("moveLimit")
        self.roster_locktime_type = self.read_data("rosterLocktimeType")
        self.universe_ids = [
            RosterSettingsUniverseIds(
                universe_id=id,
                roster_settings=self
            ) for id in self.read_data("universeIds", list())
        ]
        self.parse_boolean_data()
        self.parse_dict_data()

    def parse_dict_data(self):
        self.lineup_slot_counts = set()

        self.lineup_slot_counts = {
            RosterSettingsLineupSlotCounts(
                position=get_position(k),
                slot_count=v,
                roster_settings=self
            ) for k, v in self.read_data("lineupSlotCounts", dict()).items()
        }

        self.position_limits = {
            RosterSettingsPositionLimits(
                position=get_position(k),
                position_limit=v,
                roster_settings=self
            ) for k, v in self.read_data("positionLimits", dict()).items()
        }

        self.lineup_slot_stat_limits = {
            RosterSettingsLineupSlotStatLimits(
                position=get_position(k),
                stat=get_stat(v.get("statId")),
                stat_limit=v.get("limitValue"),
                roster_settings=self
            ) for k, v in self.read_data("lineupSlotStatLimits", dict()).items()
        }

    def parse_boolean_data(self):
        self.is_bench_unlimited = self.read_data("isBenchUnlimited", False)
        self.is_using_undroppable_list = self.read_data(
            "isUsingUndroppableList", False)


class ScheduleSettingsMatchupPeriods(SettingsObjectValue):
    _database_table = "settings_schedule_matchup_periods"
    _parent_id_attr = "settings_schedule_id"

    def __init__(self, matchup_id: int = 0, period_id: int = 0, schedule_settings: Any = None):
        self.matchup_id = matchup_id
        self.period_id = period_id
        self._parent = schedule_settings


class ScheduleSettingsDivisions(SettingsObjectValue):
    _database_table = "settings_schedule_divisions"
    _parent_id_attr = "settings_schedule_id"

    def __init__(self, data: dict = None, schedule_settings: Any = None):
        self._data = data
        self.division_id = data.get("id", None)
        self._parent = schedule_settings


class ScheduleSettings(SettingsObject):
    _database_table = "settings_schedule"

    """
    Class representing league schedule settings.

    Parses scheduling details including matchup periods, playoff configurations, and divisions.
    """

    def __init__(self, data: dict = None, parse_data: bool = True):
        super().__init__(data=data, parse_data=parse_data)

    def parse_data(self):
        self.matchup_period_count = self.read_data("matchupPeriodCount")
        # length in weeks of matchups
        self.matchup_period_length = self.read_data("matchupPeriodLength")
        self.period_type_id = self.read_data("periodTypeId")
        self.playoff_matchup_period_length = self.read_data(
            "playoffMatchupPeriodLength")
        self.playoff_seeding_rule = self.read_data("playoffSeedingRule")
        self.playoff_seeding_rule_by = self.read_data("playoffSeedingRuleBy")
        self.playoff_team_count = self.read_data("playoffTeamCount")
        self.divisions = {
            ScheduleSettingsDivisions(
                data=div,
                schedule_settings=self
            ) for div in self.read_data("divisions", list())
        }
        self.parse_boolean_data()
        self.parse_dict_data()

    def parse_dict_data(self):
        # dict where the keyn is the matchup ID and the value is a list of period IDs i.e. matchup 19 is weeks 19+20
        self.matchup_periods = {
            ScheduleSettingsMatchupPeriods(
                matchup_id=int(k),
                period_id=int(p),
                schedule_settings=self
            ) for k, v in self.read_data("matchupPeriods", dict()).items() for p in list(v)
        }

    def parse_boolean_data(self):
        self.is_playoff_reseed = self.read_data("playoffReseed", False)
        self.is_variable_playoff_matchup_period_length = self.read_data(
            "variablePlayoffMatchupPeriodLength", False)


class ScoringSettingsItemsPointOverrides(SettingsObjectValue):
    _database_table = "settings_scoring_items_point_overrides"
    _parent_id_attr = "settings_scoring_item_id"

    def __init__(self, key: str = None, value: float = None, scoring_settings_item: Any = None):
        self.key = key
        self.value = value
        self._parent = scoring_settings_item


class ScoringSettingsItems(SettingsObjectValue):
    _database_table = "settings_scoring_items"
    _parent_id_attr = "settings_scoring_id"

    def __init__(self, is_reverse_item: bool = False, league_ranking: float = 0.0, league_total: float = 0.0, points: float = 0.0,
                 stat:  Stat = None, point_overrides: dict = None, scoring_settings: Any = None):
        self.is_reverse_item = is_reverse_item
        self.league_ranking = league_ranking
        self.league_total = league_total
        self.points = points
        self.stat_id = stat.id
        self.point_overrides = {
            ScoringSettingsItemsPointOverrides(
                key=k,
                value=v,
                scoring_settings_item=self
            ) for k, v in point_overrides.items()
        }
        self._parent = scoring_settings


class ScoringSettings(SettingsObject):
    _database_table = "settings_scoring"

    """
    Class representing league scoring settings.

    Parses scoring configurations including scoring type, bonus rules, tie-breakers,
    and individual scoring items.
    """

    def __init__(self, data: dict = None, parse_data: bool = True):
        super().__init__(data=data, parse_data=parse_data)

    def parse_data(self):
        self.scoring_type = self.read_data("scoringType")
        self.home_team_bonus = self.read_data("homeTeamBonus")
        self.matchup_tie_rule = self.read_data("matchupTieRule")
        self.matchup_tie_rule_by = self.read_data("matchupTieRuleBy")
        self.player_rank_type = self.read_data("playerRankType")
        self.playoff_home_team_bonus = self.read_data("playoffHomeTeamBonus")
        self.playoff_matchup_tie_rule = self.read_data("playoffMatchupTieRule")
        self.playoff_matchup_tie_rule_by = self.read_data(
            "playoffMatchupTieRuleBy")

        self.parse_boolean_data()
        self.parse_dict_data()

    def parse_dict_data(self):
        self.scoring_items = {
            ScoringSettingsItems(
                is_reverse_item=item.get("isReverseItem", False),
                stat=get_stat(item.get("statId")),
                points=item.get("points"),
                league_ranking=item.get("leagueRanking", 0.0),
                league_total=item.get("leagueTotal", 0.0),
                point_overrides=item.get("pointsOverrides", dict()),
                scoring_settings=self
            ) for item in self.read_data("scoringItems", list())
        }

    def parse_boolean_data(self):
        self.allow_out_of_position_scoring = self.read_data(
            "allowOutOfPositionScoring", False)


class TradeSettings(SettingsObject):
    _database_table = "settings_trade"

    """
    Class representing league trade settings.

    Parses trade-related settings including deadlines, maximum trades,
    revision hours, and veto vote requirements.
    """

    def __init__(self, data: dict = None, parse_data: bool = True):
        super().__init__(data=data, parse_data=parse_data)

    def parse_data(self):
        self.max_trades = self.read_data("max")
        self.revision_hours = self.read_data("revisionHours")
        self.veto_votes_required = self.read_data("vetoVotesRequired")
        self.parse_date_data()
        self.parse_boolean_data()

    def parse_boolean_data(self):
        self.allow_out_of_universe = self.read_data(
            "allowOutOfUniverse", False)

    def parse_date_data(self):
        self.deadline_date = convert_epoch_to_date(
            self.read_data("deadlineDate", False))


class Settings(SettingsObject):
    _database_table = "settings"

    """
    Class representing overall league settings.

    Aggregates various league configuration settings including league information,
    acquisition, finance, draft, roster, schedule, scoring, and trade settings.
    """

    def __init__(self, data: dict = None, parse_data: bool = True):
        super().__init__(data=data, parse_data=parse_data)

    def write_to_database(self, engine, table=None, ignore_children=False):
        # Not the cleanest way to do this but we can fix it later (famous last words)
        super().write_to_database(engine, table)

        attribute_map: dict = {
            "finance_id": self.finance,
            "trade_id": self.trade,
            "scoring_id": self.scoring,
            "schedule_id": self.schedule,
            "roster_id": self.roster,
            "draft_id": self.draft,
            "acquisition_id": self.acquisition,
        }

        for id_attr_name, attr_value in attribute_map.items():
            if not hasattr(self, id_attr_name):
                self.set_child_id(engine, id_attr_name, attr_value)

        super().write_to_database(engine, table, ignore_children=True)

    def parse_data(self):
        """
        Parse the overall league settings data and assign values to instance attributes.

        Calls methods to parse acquisition, finance, draft, roster, schedule,
        scoring, and trade settings.
        """
        self.name = self.read_data("name")
        self.size = self.read_data("size")
        self.restriction_type = self.read_data("restrictionType")
        self.parse_boolean_data()
        self.parse_acquisition_data()
        self.parse_finance_data()
        self.parse_draft_data()
        self.parse_roster_data()
        self.parse_schedule_data()
        self.parse_scoring_data()
        self.parse_trade_data()

    def parse_acquisition_data(self):
        acquisition_data = self.read_data("acquisitionSettings", dict())
        self.acquisition = AcquisitionSettings(data=acquisition_data)

    def parse_finance_data(self):
        finance_data = self.read_data("financeSettings", dict())
        self.finance = FinanceSettings(data=finance_data)

    def parse_draft_data(self):
        draft_data = self.read_data("draftSettings", dict())
        self.draft = DraftSettings(data=draft_data)

    def parse_roster_data(self):
        roster_data = self.read_data("rosterSettings", dict())
        self.roster = RosterSettings(data=roster_data)

    def parse_schedule_data(self):
        schedule_data = self.read_data("scheduleSettings", dict())
        self.schedule = ScheduleSettings(data=schedule_data)

    def parse_scoring_data(self):
        scoring_data = self.read_data("scoringSettings", dict())
        self.scoring = ScoringSettings(data=scoring_data)

    def parse_trade_data(self):
        trade_data = self.read_data("tradeSettings", dict())
        self.trade = TradeSettings(data=trade_data)

    def parse_boolean_data(self):
        self.is_public = self.read_data("isPublic", False)
        self.is_customizable = self.read_data("isCustomizable", False)
