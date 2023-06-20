from api import *
from engine import *
from frame_reader import FrameReader
from mediapipe_detector import MediapipeDetector
from landmark_extractor import LandmarkExtractor
from text_classifier import TextClassifier
from output_emittor import OutputEmittor

if __name__ == "__main__":
    job = Job("vsl_translate")
    data_stream = job.add_source(FrameReader("frame_reader", 1, 9990))
    data_stream = data_stream.apply_operator(MediapipeDetector("mediapipe_extractor", 3))
    data_stream = data_stream.apply_operator(LandmarkExtractor("landmark_extractor", 3))
    data_stream = data_stream.apply_operator(TextClassifier("text_classifier", 3))
    data_stream.apply_operator(OutputEmittor("output_emittor", 1, 8000))
    starter = JobStarter(job)
    starter.start()