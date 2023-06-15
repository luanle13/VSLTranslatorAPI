from abc import ABC, abstractmethod

"""
This class is the base class for all grouping strategies.
"""
class GroupingStrategy(ABC):
    """
    Get target instance id from an event and component parallelism.
    Note that in this implementation, only one instance is selected.
    This can be easily extended if needed.

    Parameters:
    event (Event): The event object to route to the component.
    parallelism (int): The parallelism of the component.

    Returns:
    int: The integer key of this event.
    """
    @abstractmethod
    def get_instance(self, event, parallelism):
        pass