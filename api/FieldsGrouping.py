from GroupingStrategy import GroupingStrategy

"""
With fields grouping, the events are routed to downstream instances based on some hash method.
"""
class FieldsGrouping(GroupingStrategy):
    def __init__(self):
        pass
    
    """
    Get key from an event. Child class can override this function to calculate key in different ways.

    Parameters:
    event (Event): The event object to extract key from.

    Returns:
    object: The data to be hashed.
    """
    def get_key(self, event):
        return event.get_data()
    
    """
    Get target instance id from an event and component parallelism.

    Parameters:
    event (Event): The event object to route to the component.
    parallelism (int): The parallelism of the component.

    Returns:
    int: The integer key of this event.
    """
    def get_instance(self, event, parallelism):
        return abs(self.get_key(event).__hash__()) % parallelism