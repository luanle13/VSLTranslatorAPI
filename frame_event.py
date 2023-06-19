from api import Event

class FrameEvent(Event):
    def __init__(self, frame):
        super().__init__()
        self.frame = frame

    def get_data(self):
        return self.frame