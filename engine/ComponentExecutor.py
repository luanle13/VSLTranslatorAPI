from api.Component import Component
from InstanceExecutor import InstanceExecutor
from abc import ABC, abstractmethod
from typing import List
from EventQueue import EventQueue

"""
The base class for executors of source and operator.

Parameters:
component (Component): The component which this executor executes.
"""
class ComponentExecutor(ABC):
    def __init__(self, component: Component) -> None:
        self.component = component
        parallelism: int = component.get_parallelism()
        self.instance_executors = [InstanceExecutor() for i in range(parallelism)]
    
    """
    Start instance executors (real processes) of this component.
    """
    @abstractmethod
    def start(self):
        pass

    """
    Get the instance executors of this component executor.

    Returns:
    list: List of instance executors of this component executor.
    """
    def get_instance_executors(self) -> List[InstanceExecutor]:
        return self.instance_executors

    """
    Get the component of this component executor.
    
    Returns:
    Component: The component of thsi component executor.
    """
    def get_component(self) -> Component:
        return self.component
    
    """
    Set the incoming queues of this component executor.
    
    Parameters:
    queues (list): The list of incoming queues of this component executor.
    """
    def set_incoming_queue(self, queues: List[EventQueue]):
        for i, queue in enumerate(queues):
            self.instance_executors[i].set_incoming_queue(queue)

    """
    Set the outgoing queue of this component executor.

    Parameters:
    queue (EventQueue): The outgoing queue of this component executor.
    """
    def set_outgoing_queue(self, queue: EventQueue):
        for instance in self.instance_executors:
            instance.set_outgoing_queue(queue)