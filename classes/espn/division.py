from classes.espn.base import ESPNObject


class Division(ESPNObject):
    _database_table = "divisions"

    def __init__(self, data: dict):
        self._data = data
        self.id = data.get("id", None)
        self.name = data.get("name", None)
        self.size = data.get("size", None)

    def __repr__(self):
        """
        Return a string representation of the object, excluding the 'data' attribute.

        :return: A string representation of the instance.
        :rtype: str
        """
        return f"{self.__class__.__name__}_{self.id}: {self.name} [{self.size}M]"
