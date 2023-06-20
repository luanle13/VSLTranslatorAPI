from queue import Queue


"""
The class for intermediate event queues between processes.

Properties:
size (int): The maximum size of the queue.
"""
class EventQueue(Queue):
    def __init__(self, size):
        super().__init__(size)