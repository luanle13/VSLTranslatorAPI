from api import GroupingStrategy

NUMBER_OF_FRAMES = 30

class FrameGroupingStrategy(GroupingStrategy):
    def __init__(self) -> None:
        self.count = 0


    def get_instance(self, event, parallelism):
        if self.count >= parallelism * NUMBER_OF_FRAMES:
            self.count = 0
        self.count += 1
        return self.count - 1 % NUMBER_OF_FRAMES