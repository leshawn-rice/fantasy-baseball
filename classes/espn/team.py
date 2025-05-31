from classes.espn.base import ESPNObject


class TeamObject(ESPNObject):
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


class TeamOwner(TeamObject):
    _database_table = "teams_owners"

    def __init__(self, team_id, owner_id):
        self.team_id = team_id
        self.owner_id = owner_id


class Team(TeamObject):
    _database_table = "teams"

    def __init__(self, data: dict = None, parse_data: bool = True):
        super().__init__(data=data, parse_data=parse_data)

    def parse_data(self):
        self.id = self.read_data("id")
        self.name = self.read_data("name")
        self.abbreviation = self.read_data("abbrev")
        self.division_id = self.read_data("divisionId")
        self.primary_owner_id = self.read_data("primaryOwner")
        self.logo = self.read_data("logo")
        self.logo_type = self.read_data("logoType")
        self.playoff_seed = self.read_data("playoffSeed", 0)
        self.playoff_clinch_type = self.read_data("playoffClinchType")
        self.points = self.read_data("points", 0.0)
        self.points_adjusted = self.read_data("pointsAdjusted", 0.0)
        self.points_delta = self.read_data("pointsDelta", 0.0)
        self.current_projected_rank = self.read_data("currentProjectedRank", 0)
        self.draft_day_projected_rank = self.read_data(
            "draftDayProjectedRank", 0)
        self.rank_calculated_final = self.read_data("rankCalculatedFinal", 0)
        self.rank_final = self.read_data("rankFinal", 0)
        self.waiver_rank = self.read_data("waiverRank", 0)
        self.parse_boolean_data()
        self.parse_complex_data()

    def parse_boolean_data(self):
        self.is_active = self.read_data("isActive", False)

    def parse_complex_data(self):
        self.team_owners = [
            TeamOwner(team_id=self.id, owner_id=owner) for owner in self.read_data("owners")
        ]
