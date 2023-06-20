from abc import ABC, abstractmethod


"""
The base class for all the event classes.
Users should extend this class to implement all their own event classes.
"""
class Event(ABC):
    """
    Get data stored in the event.
    
    Returns: 
    object: The data stored in the event.
    """
    @abstractmethod
    def get_data(self):
        pass