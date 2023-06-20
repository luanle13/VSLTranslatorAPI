from .grouping_strategy import GroupingStrategy


"""
With shuffle grouping, the events are routed to downstream instances relatively.
This implementation is round robin based.

Properties:
count (int): The counter of instances, which is reset to 0 if counter > parallelism
"""
class ShuffleGrouping(GroupingStrategy):
    def __init__(self):
        self.count = 0
    
    """
    Get target instance id from an event and component parallelism.

    Parameters:
    event (Event): The event object to route to the component.
    parrallelism (int): The parallelism of the component.

    Returns:
    int: The integer key of this event.
    """
    def get_instance(self, event, parallelism):
        if self.count >= parallelism:
            self.count = 0
        self.count += 1
        return self.count - 1