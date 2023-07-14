from .component_executor import ComponentExecutor
from .source_instance_executor import SourceInstanceExecutor
import copy


"""
The executor for source components.
When the executor is started, a new thread is created to call the get_events() function of the source component repeatedly.

Parameters:
source (Source): The source which this executor executes.
"""
class SourceExecutor(ComponentExecutor):
    def __init__(self, source):
        super().__init__(source)
        self.source = source
        self.instance_executors = []
        for i in range(source.get_parallelism()):
            cloned = copy.copy(source)
            self.instance_executors.append(SourceInstanceExecutor(i, cloned))
    
    """
    Start instance executors (real processes) of this component.
    """
    def start(self):
        if self.instance_executors is not None:
            for instance in self.instance_executors:
                instance.start()
    
    """
    Set the incoming queues of this source executor.
    
    Parameters:
    queues (list): The list of incoming queues of this source executor.
    """
    def set_incoming_queue(self, queues):
        raise Exception("No incoming queue is allowed for source executor")