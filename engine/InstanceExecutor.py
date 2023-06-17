from abc import ABC
from EventQueue import EventQueue
from Process import Process

"""
The executor for source components. 
When the executor is started, a new thread is created to call the get_events() function of the source component repeatedly.

Properties
event_collector (list): This list is used for accepting events from user logic.
incoming_queue (EventQueue): Data queue for the upstream process
outgoing_queue (EventQueue): Data queue for the downstream process
"""
class InstanceExecutor(Process):
    def __init__(self) -> None:
        super().__init__()
        self.event_collector = []
        self.incoming_queue = None
        self.outgoing_queue = None

    """
    Set the data queue for the upstream process.

    Parameters:
    queue (EventQueue): Data queue for the upstream process.
    """
    def set_incoming_queue(self, queue: EventQueue):
        self.incoming_queue = queue
    
    """
    Set the data queue for the downstream process.

    Parameters:
    queue (EventQueue): Data queue for the downstream process.
    """
    def set_outgoing_queue(self, queue: EventQueue):
        self.outgoing_queue = queue