from typing import Any
from utilities.espn import get_position, get_stat, convert_epoch_to_date


class LeagueSettingsObject(object):
    """
    Base class for league settings objects.

    This class provides common functionality for reading and parsing data from a dictionary.
    Subclasses should override :meth:`parse_data` to implement custom parsing logic.
    """
    default_read_value = None

    def __init__(self, data: dict = None, parse_data: bool = True):
        """
        Initialize a new LeagueSettingsObject instance.

        :param data: Dictionary containing configuration data.
        :type data: dict, optional
        :param parse_data: If True, automatically parse the data by calling :meth:`parse_data`.
        :type parse_data: bool, optional
        """
        self.data = data
        if parse_data:
            self.parse_data()

    def read_data(self, key: str = None, default_val: Any = None):
        """
        Retrieve a value from the data dictionary using the specified key.

        If the key is not found, returns the provided default value or the class's
        :attr:`default_read_value` if no default is provided.

        :param key: The key to look up in the data dictionary.
        :type key: str, optional
        :param default_val: The default value to return if the key is not found.
        :type default_val: Any, optional
        :return: The value from the data dictionary or a default value.
        :rtype: Any
        """
        return_val = default_val if default_val is not None else self.default_read_value
        if not key:
            return return_val
        return self.data.get(key, return_val)

    def parse_data(self):
        """
        Parse the data dictionary.

        This method should be overridden by subclasses to implement custom parsing logic.
        """
        pass

    def __repr__(self):
        """
        Return a string representation of the object, excluding the 'data' attribute.

        :return: A string representation of the instance.
        :rtype: str
        """
        attrs = ", ".join(f"'{key}': {value!r}" for key,
                          value in self.__dict__.items() if f"{key}".lower() != "data")
        return f"'{self.__class__.__name__}': {{{attrs}}}"


class LeagueFinanceSettings(LeagueSettingsObject):
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


class LeagueAcquisitionSettings(LeagueSettingsObject):
    """
    Class representing league acquisition settings.

    Parses settings related to player acquisitions including budgets, limits, waiver rules,
    and transaction locking.
    """
    default_read_value = None

    def __init__(self, data: dict = None, parse_data: bool = True):
        super().__init__(data=data, parse_data=parse_data)

    def parse_data(self):
        self.acquisition_budget = self.read_data("acquisitionBudget")
        self.acquisition_limit = self.read_data("acquisitionLimit")
        self.acquisition_type = self.read_data("acquisitionType")
        self.final_place_transaction_eligible = self.read_data(
            "finalPlaceTransactionEligible")
        self.matchup_acquisition_limt = self.read_data(
            "matchupAcquisitionLimit")
        self.minimum_bid = self.read_data("minimumBid")
        self.waiver_hours = self.read_data("waiverHours")
        self.waiver_process_days = self.read_data("waiverProcessDays")
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


class LeagueDraftSettings(LeagueSettingsObject):
    """
    Class representing league draft settings.

    Parses draft configuration settings such as auction budgets, draft dates,
    keeper counts, and order types.
    """
    default_read_value = None

    def __init__(self, data: dict = None, parse_data: bool = True):
        super().__init__(data=data, parse_data=parse_data)

    def parse_data(self):
        self.auction_budget = self.read_data("auctionBudget")
        self.keeper_count = self.read_data("keeperCount")
        self.keeper_count_future = self.read_data("keeperCountFuture")
        self.keeper_order_type = self.read_data("keeperOrderType")
        self.league_sub_type = self.read_data("leagueSubType")
        self.order_type = self.read_data("orderType")
        self.pick_order = self.read_data("pickOrder")
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


class LeagueRosterSettings(LeagueSettingsObject):
    """
    Class representing league roster settings.

    Parses settings related to lineup lock times, move limits, roster limits, and associated
    position and slot configurations.
    """
    default_read_value = None

    def __init__(self, data: dict = None, parse_data: bool = True):
        super().__init__(data=data, parse_data=parse_data)

    def parse_data(self):
        self.lineup_locktime_type = self.read_data("lineupLocktimeType")
        self.move_limit = self.read_data("moveLimit")
        self.roster_locktime_type = self.read_data("rosterLocktimeType")
        self.universe_ids = self.read_data("universeIds", list())
        self.parse_boolean_data()
        self.parse_dict_data()

    def parse_dict_data(self):
        self.lineup_slot_counts = {
            get_position(k): v for k, v in self.read_data("lineupSlotCounts", dict()).items()
        }
        self.position_limits = {
            get_position(k): v for k, v in self.read_data("positionLimits", dict()).items()
        }
        self.lineup_slot_stat_limits = {
            get_position(k): {
                "stat": get_stat(v.get("statId")), "limit_value": v.get("limitValue")
            } for k, v in self.read_data("lineupSlotStatLimits", dict()).items()
        }

    def parse_boolean_data(self):
        self.is_bench_unlimited = self.read_data("isBenchUnlimited", False)
        self.is_using_undroppable_list = self.read_data(
            "isUsingUndroppableList", False)


class LeagueScheduleSettings(LeagueSettingsObject):
    """
    Class representing league schedule settings.

    Parses scheduling details including matchup periods, playoff configurations, and divisions.
    """
    default_read_value = None

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
        self.divisions = self.read_data("divisions")
        self.parse_boolean_data()
        self.parse_dict_data()

    def parse_dict_data(self):
        # dict where the keyn is the matchup ID and the value is a list of period IDs i.e. matchup 19 is weeks 19+20
        self.matchup_periods = {
            int(k): list(v) for k, v in self.read_data("matchupPeriods", dict()).items()
        }

    def parse_boolean_data(self):
        self.is_playoff_reseed = self.read_data("playoffReseed", False)
        self.is_variable_playoff_matchup_period_length = self.read_data(
            "variablePlayoffMatchupPeriodLength", False)


class LeagueScoringSettings(LeagueSettingsObject):
    """
    Class representing league scoring settings.

    Parses scoring configurations including scoring type, bonus rules, tie-breakers,
    and individual scoring items.
    """
    default_read_value = None

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
        self.scoring_items = [
            {
                "stat": get_stat(item.get("statId")),
                "points": item.get("points"),
                "is_reverse_item": item.get("isReverseItem", False),
                "league_ranking": item.get("leagueRanking", 0.0),
                "league_total": item.get("leagueTotal", 0.0),
                "points_overrides": item.get("pointsOverrides", dict())
            } for item in self.read_data("scoringItems", list())
        ]

    def parse_boolean_data(self):
        self.allow_out_of_position_scoring = self.read_data(
            "allowOutOfPositionScoring", False)


class LeagueTradeSettings(LeagueSettingsObject):
    """
    Class representing league trade settings.

    Parses trade-related settings including deadlines, maximum trades,
    revision hours, and veto vote requirements.
    """
    default_read_value = None

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


class LeagueSettings(LeagueSettingsObject):
    """
    Class representing overall league settings.

    Aggregates various league configuration settings including league information,
    acquisition, finance, draft, roster, schedule, scoring, and trade settings.
    """
    default_read_value = None

    def __init__(self, data: dict = None, parse_data: bool = True):
        super().__init__(data=data, parse_data=parse_data)

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
        self.acquisition = LeagueFinanceSettings(data=acquisition_data)

    def parse_finance_data(self):
        finance_data = self.read_data("financeSettings", dict())
        self.finance = LeagueFinanceSettings(data=finance_data)

    def parse_draft_data(self):
        draft_data = self.read_data("draftSettings", dict())
        self.draft = LeagueDraftSettings(data=draft_data)

    def parse_roster_data(self):
        roster_data = self.read_data("rosterSettings", dict())
        self.roster = LeagueRosterSettings(data=roster_data)

    def parse_schedule_data(self):
        schedule_data = self.read_data("scheduleSettings", dict())
        self.schedule = LeagueScheduleSettings(data=schedule_data)

    def parse_scoring_data(self):
        scoring_data = self.read_data("scoringSettings", dict())
        self.scoring = LeagueScoringSettings(data=scoring_data)

    def parse_trade_data(self):
        trade_data = self.read_data("tradeSettings", dict())
        self.trade = LeagueTradeSettings(data=trade_data)

    def parse_boolean_data(self):
        self.is_public = self.read_data("isPublic", False)
        self.is_customizable = self.read_data("isCustomizable", False)
