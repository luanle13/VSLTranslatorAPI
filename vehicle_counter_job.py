from api import *
from engine import *
from frame_reader import FrameReader
from mediapipe_detector import MediapipeDetector
from landmark_extractor import LandmarkExtractor


if __name__ == "__main__":
    job = Job("vsl_translator")
    data_stream = job.add_source(FrameReader("frame_reader", 1, 9990))
    data_stream = data_stream.apply_operator(MediapipeDetector("mediapipe_extractor", 1))
    data_stream = data_stream.apply_operator(LandmarkExtractor("landmark_extractor", 1))
    starter = JobStarter(job)
    starter.start()