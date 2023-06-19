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


"""
The base class for all components, including Source and Operator

Properties:
name (string): The name of this component.
parallelism (int): The number of instances of this component.
outgoing_stream (Stream): The outgoing event stream of this component. The stream is used to connect the downstream components
"""
class Component:
    def __init__(self, name, parallelism):
        self.name = name
        self.parallelism = parallelism
        self.outgoing_stream = Stream()

    """
    Get the name of this component.

    Returns
    string: The name of this component.
    """
    def get_name(self):
        return self.name

    """
    Get the parallelism (number of instances) of this component.

    Returns:
    int: The parallelism (number of instances) of this component.
    """
    def get_parallelism(self):
        return self.parallelism

    """
    Get the outgoing event stream of this component. The stream is used to connect the downstream components.

    Returns:
    Stream: The outgoing event stream of this component. The stream is used to connect the downstream components
    """
    def get_outgoing_stream(self):
        return self.outgoing_stream


"""
This class is the base class for all user-defined sources.

Properties:
name (String): The name of this source.
parallelism (int): The number of instances of this source.
"""
class Source(Component, ABC):
    def __init__(self, name, parallelism):
        super().__init__(name, parallelism)
    
    """
    Set up instance.

    Parameters:
    instance (int): The instance id (an index starting from 0) of this source instance.
    """
    @abstractmethod
    def setup_instance(self, instance):
        pass
    
    """
    Accept events from external into the system.

    Parameters:
    event_collector (list): The outgoing event collector.
    """
    @abstractmethod
    def get_events(self, event_collector):
        pass


"""
This is the base class for all user-defined operators.

Properties:
name (string): The name of this component.
parallelism (int): The number of instances of this component.
grouping (GroupingStrategy): The grouping strategy of this operator.
"""
class Operator(Component):
    def __init__(self, name, parallelism, grouping=None):
        super().__init__(name, parallelism)
        self.grouping = grouping if grouping is not None else ShuffleGrouping()
    
    """
    Set up instance.

    Parameters:
    instance (int): The instance id (an index starting from 0) of this source instance.
    """
    @abstractmethod
    def setup_instance(self, instance):
        pass

    """
    Apply logic to the incoming event and generate results.
    
    Parameters:
    event (Event): The incoming event.
    event_collector (list): The outgoing event collector.
    """
    @abstractmethod
    def apply(self, event, event_collector):
        pass

    """
    Get the grouping strategy of an event.

    Returns:
    GroupingStrategy: The grouping strategy of this opertator.
    """
    def get_grouping_strategy(self):
        return self.grouping
    

"""
The Stream class represents a data stream coming out of a component.
Operators with the correct type can be applied to this stream.

Properties:
operator_set (set): List of all operators to be applied to this stream.
"""
class Stream:
    def __init__(self):
        self.operator_set = set()
    
    """
    Apply an operator to this stream.

    Parameters:
    operator (Operator): The operator to be connected to the current stream.

    Returns:
    Stream: The outgoing stream of the operator.
    """
    def apply_operator(self, operator):
        if operator in self.operator_set:
            raise Exception(f"Operator {operator.getName()} is added to job twice")
        self.operator_set.add(operator)
        return operator.get_outgoing_stream()
    
    """
    Get the collection of operators applied to this stream.

    Returns:
    list: The collection of operators applied to this stream.
    """
    def get_applied_operators(self):
        return self.operator_set
    

"""
The class is used by users to set up their jobs and run.

Properties:
name (str): The name of this job.
source_set (set): The list of sources in this job.
"""
class Job:
    def __init__(self, job_name):
        self.name = job_name
        self.source_set = set()
    
    """
    Add a source into the job.
    A stream is returned which will be used to connect to other operators.

    Parameters:
    source (Source): The source object to be added into the job.

    Returns:
    stream (Stream): A stream that can be used to connect to other operators.
    """
    def add_source(self, source):
        if source in self.source_set:
            raise Exception(f"Source {source.get_name()} is added to job twice")
        self.source_set.add(source)
        return source.get_outgoing_stream()

    """
    Get the name of this job.

    Returns:
    str: The name of this job.
    """
    def get_name(self):
        return self.name
    
    """
    Get the list of sources in this job.
    This function is used by JobRunner to traverse the graph.

    Returns:
    The list of sources in this job.
    """
    def get_sources(self):
        return self.source_set