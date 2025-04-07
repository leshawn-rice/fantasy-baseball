from classes.espn.base import ESPNObject


class LeagueMemberNotificationSetting(ESPNObject):
    database_table = "members_notification_settings"

    def __init__(self, data: dict = None):
        self.enabled = data.get("enabled", False)
        self.id = data.get("id", None)
        self.type = data.get("type", None)
        self.member_id = data.get("member_id", None)


class LeagueMember(ESPNObject):
    database_table = "members"

    def __init__(self, data: dict = None):
        self.id = data.get("id", None)
        self.username = data.get("displayName", None)
        self.first_name = data.get("firstName", None)
        self.last_name = data.get("lastName", None)
        self.name = f"{self.first_name} {self.last_name}"
        self.notification_settings = [
            LeagueMemberNotificationSetting({**setting, "member_id": self.id}) for setting in data.get("notificationSettings", list())
        ]
