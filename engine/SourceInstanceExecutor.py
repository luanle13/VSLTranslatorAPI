from InstanceExecutor import InstanceExecutor
from api.Source import Source
from typing import List
from api.Event import Event

"""
The executor for source components. 
When the executor is started, a new thread is created to call the get_events() function of the source component repeatedly.

Properties:
instance_id (int): The ID of this instance.
source (Source): The source of this instance.
"""
class SourceInstanceExecutor(InstanceExecutor):
    def __init__(self, instance_id: int, source: Source) -> None:
        super().__init__()
        self.instance_id = instance_id
        self.source = source
        self.source.setup_instance(instance_id)
    
    """
    Run the process once.

    Returns:
    bool: True if the thread should continue; False if the thread should exit.
    """
    def run_once(self) -> bool:
        event_collector: List[Event] = []
        try:
            self.source.get_events(event_collector)
        except Exception:
            return False
        try:
            for event in event_collector:
                self.outgoing_queue.put(event)
            event_collector.clear()
        except KeyboardInterrupt:
            return False