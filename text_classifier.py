from api import Operator
from keras.models import load_model
import numpy
from output_event import OutputEvent

model = load_model('./action.h5')

class TextClassifier(Operator):
    def __init__(self, name, parallelism, grouping=None):
        super().__init__(name, parallelism, grouping)
        self.instance = 0
        self.vec_set = []

    def setup_instance(self, instance):
        self.instance = instance
    
    def apply(self, event, event_collector):
        try:
            data = event.get_data()
            if data is not None:
                self.vec_set.append(data)
            if len(self.vec_set) == 30:
                # print(data.shape)
                output = model.predict(numpy.expand_dims(numpy.array(self.vec_set), axis=0))[0]
                output = numpy.argmax(output)
                self.vec_set.clear()
                event_collector.append(OutputEvent(output))
        except Exception as e:
            pass