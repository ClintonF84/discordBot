from datetime import datetime

class Game:
    def __init__(self, name, howToLink, createdDate=None, playedDate="", votedCount=0):
        self.name = name
        self.how_to_link = howToLink
        self.created_date = createdDate if createdDate else datetime.today().date().isoformat()
        self.played_date = playedDate
        self.voted_count = votedCount

    def vote(self):
        self.voted_count += 1

    def play(self):
        self.played_date = datetime.today().date().isoformat()

    def to_dict(self):
        return {
            "name": self.name,
            "createdDate": self.created_date,
            "playedDate": self.played_date,
            "howToLink": self.how_to_link,
            "votedCount": self.voted_count
        }
