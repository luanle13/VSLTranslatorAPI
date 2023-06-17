from typing import List
from ComponentExecutor import ComponentExecutor
from EventQueue import EventQueue
from SourceInstanceExecutor import SourceInstanceExecutor
from InstanceExecutor import InstanceExecutor
from api.Source import Source
import copy

"""
The executor for source components.
When the executor is started, a new thread is created to call the get_events() function of the source component repeatedly.

Parameters:
source (Source): The source which this executor executes.
"""
class SourceExecutor(ComponentExecutor):
    def __init__(self, source: Source) -> None:
        super().__init__(source)
        self.source = source
        self.instance_executors: List[SourceInstanceExecutor] = []
        for i in range(source.get_parallelism()):
            cloned = copy.deepcopy(source)
            self.instance_executors.append(SourceInstanceExecutor(source))
    
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
    def set_incoming_queue(self, queues: List[EventQueue]):
        raise Exception("No incoming queue is allowed for source executor")