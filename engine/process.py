from threading import Thread
from abc import ABC


"""
This is the base class of all processes, including executors and stream managers.
When a process is started, a new thread is created to call the runOnce() function of the derived class.
Each process also have an incoming event queue and outgoing event queue.
"""
class Process(ABC):
    def __init__(self):
        super().__init__()
        self.thread = Thread(target=self.run)
    
    """
    Start the process
    """
    def start(self):
        self.thread.start()
    
    """
    Continuously run the process.
    """
    def run(self):
        while self.run_once():
            pass
    
    """
    Run process once.
    """
    def run_once(self):
        raise NotImplementedError