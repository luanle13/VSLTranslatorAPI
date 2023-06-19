from api import Event

class MediapipeEvent(Event):
    def __init__(self, data):
        super().__init__()
        self.data = data

    def get_data(self):
        return self.data