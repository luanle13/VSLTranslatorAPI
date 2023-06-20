from .process import Process
from api import GroupingStrategy


"""
Responsible for transporting events form the incoming queue to the outgoing queues with a grouping strategy.
"""
class EventDispatcher(Process):
    def __init__(self, downstream_executor):
        super().__init__()
        self.downstream_executor = downstream_executor
        self.incoming_queue = None
        self.outgoing_queue = None
    
    """
    Run process once.
    """
    def run_once(self):
        try:
            event = self.incoming_queue.get()
            grouping: GroupingStrategy = self.downstream_executor.get_grouping_strategy()
            instance = grouping.get_instance(event, len(self.outgoing_queue))
            self.outgoing_queue[instance].put(event)
        except Exception:
            return False
        return True

    """
    Set the incoming queue of this dispatcher.

    Parameters:
    queue (EventQueue): The incoming queue of this dispatcher.
    """
    def set_incoming_queue(self, queue):
        self.incoming_queue = queue
    
    """
    Set the list of outgoing queues of this dispatcher.

    Parameters:
    queues (list): The list of ougoing queues of this dispatcher.
    """
    def set_outgoing_queues(self, queues):
        self.outgoing_queue = queues