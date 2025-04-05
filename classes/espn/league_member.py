class LeagueMember:
    def __init__(self, data: dict = None):
        self.id = data.get("id", None).strip("{").strip("}")
        self.username = data.get("displayName", None)
        self.first_name = data.get("firstName", None)
        self.last_name = data.get("lastName", None)
        self.notification_settings = data.get("notificationSettings")
