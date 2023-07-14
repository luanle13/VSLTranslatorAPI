from api import Job
from engine import JobStarter
from executor import FrameReader, MediapipeDetector, LandmarkExtractor, TextClassifier, OutputEmittor
from server import Receiver, Sender


if __name__ == "__main__":
    receiver = Receiver(9990)
    receiver.run()
    sender = Sender(8000)
    sender.run()
    job = Job("vsl_translate")
    data_stream = job.add_source(FrameReader("frame_reader", 1, receiver.get_frame_data))
    data_stream = data_stream.apply_operator(MediapipeDetector("mediapipe_extractor", 10))
    data_stream = data_stream.apply_operator(LandmarkExtractor("landmark_extractor", 10))
    data_stream = data_stream.apply_operator(TextClassifier("text_classifier", 10))
    data_stream.apply_operator(OutputEmittor("output_emittor", 1, sender.set_out_data))
    starter = JobStarter(job)
    starter.start()
