from api import *
import cv2
import numpy
from mediapipe_event import MediapipeEvent
from numpy_array_event import NumpyArrayEvent


# model = mediapipe.solutions.holistic.Holistic(min_detection_confidence = .5, min_tracking_confidence = .5)


class LandmarkExtractor(Operator):
    def __init__(self, name, parallelism, grouping=None):
        super().__init__(name, parallelism, grouping)
        self.instance = 0
    
    def setup_instance(self, instance):
        self.instance = instance
    
    def apply(self, event, event_collector):
        try:
            data = event.get_data()
            if data is not None:
                pose = self.extract_pose(data)
                face = self.extract_face(data)
                left_hand, right_hand = self.extract_hands(data)
                event_collector.append(NumpyArrayEvent(numpy.concatenate([pose, face, left_hand, right_hand])))
        except Exception as e:
            pass
    
    def extract_pose(self, data):
        pose_lm = []
        for res in data.pose_landmarks.landmark:
            arr = numpy.array([res.x, res.y, res.z, res.visibility])
            pose_lm.append(arr)
        pose_lm = numpy.array(pose_lm).flatten()
        return pose_lm

    def extract_hands(self, data):
        lh_lm = []
        if data.left_hand_landmarks is None:
            lh_lm = numpy.zeros(63,)
        else:
            for res in data.left_hand_landmarks.landmark:
                lh_lm.append(numpy.array([res.x, res.y, res.z]))
            lh_lm = numpy.append(lh_lm).flatten()
        rh_lm = []
        if data.right_hand_landmarks is None:
            rh_lm = numpy.zeros(63,)
        else:
            for res in data.right_hand_landmarks.landmark:
                rh_lm.append(numpy.array([res.x, res.y, res.z]))
            rh_lm = numpy.array(rh_lm).flatten()
        return lh_lm, rh_lm
    
    def extract_face(self, data):
        face_lm = numpy.array([[res.x, res.y, res.z] for res in data.face_landmarks.landmark]).flatten() if data.face_landmarks else numpy.zeros(468*3,)
        return face_lm