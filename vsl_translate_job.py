from api import Job
from engine import JobStarter
from executor import FrameReader, MediapipeDetector, LandmarkExtractor, TextClassifier, OutputEmittor

if __name__ == "__main__":
    job = Job("vsl_translate")
    data_stream = job.add_source(FrameReader("frame_reader", 1, 9990))
    data_stream = data_stream.apply_operator(MediapipeDetector("mediapipe_extractor", 10))
    data_stream = data_stream.apply_operator(LandmarkExtractor("landmark_extractor", 10))
    data_stream = data_stream.apply_operator(TextClassifier("text_classifier", 10))
    data_stream.apply_operator(OutputEmittor("output_emittor", 1, 8000))
    starter = JobStarter(job)
    starter.start()