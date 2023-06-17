from typing import List
from Process import Process
from OperatorExecutor import OperatorExecutor
from EventQueue import EventQueue
from api.Event import Event
from api.GroupingStrategy import GroupingStrategy

"""
Responsible for transporting events form the incoming queue to the outgoing queues with a grouping strategy.
"""
class EventDispatcher(Process):
    def __init__(self, downstream_executor: OperatorExecutor) -> None:
        super().__init__()
        self.downstream_executor: OperatorExecutor = downstream_executor
        self.incoming_queue: EventQueue = None
        self.outgoing_queue: List[EventQueue] = None
    
    """
    Run process once.
    """
    def run_once(self) -> bool:
        try:
            event: Event = self.incoming_queue.get()
            grouping: GroupingStrategy = self.downstream_executor.get_grouping_strategy()
            instance: int = grouping.get_instance(event, len(self.outgoing_queue))
            self.outgoing_queue[instance].put(event)
        except Exception:
            return False
        return True

    """
    Set the incoming queue of this dispatcher.

    Parameters:
    queue (EventQueue): The incoming queue of this dispatcher.
    """
    def set_incoming_queue(self, queue: EventQueue):
        self.incoming_queue = queue
    
    """
    Set the list of outgoing queues of this dispatcher.

    Parameters:
    queues (list): The list of ougoing queues of this dispatcher.
    """
    def set_outgoing_queues(self, queues: List[EventQueue]):
        self.outgoing_queue = queues