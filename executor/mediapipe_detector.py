from api import Operator
import cv2
import mediapipe
from event import MediapipeEvent
from grouping_strategy import FrameGroupingStrategy


model = mediapipe.solutions.holistic.Holistic(min_detection_confidence = .5, min_tracking_confidence = .5)


class MediapipeDetector(Operator):
    def __init__(self, name, parallelism, grouping=FrameGroupingStrategy):
        super().__init__(name, parallelism, grouping)
        self.instance = 0
    
    def setup_instance(self, instance):
        self.instance = instance
    
    def apply(self, event, event_collector):
        try:
            data = event.get_data()
            if data is not None:
                image = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)
                results = model.process(image)
                data = MediapipeEvent(results)
                event_collector.append(data)
        except Exception as e:
            pass