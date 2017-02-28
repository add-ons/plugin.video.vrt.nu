class TitleItem:

    def __init__(self, title, url, is_playable):
        self.title = title
        self.url = url
        self.is_playable = is_playable


class Credentials:

    def __init__(self, addon):
        self.addon = addon
        self.reload()

    def are_filled_in(self):
        return not (self.username is None or self.password is None or self.username == "" or self.password == "")

    def reload(self):
        self.username = self.addon.getSetting("username")
        self.password = self.addon.getSetting("password")