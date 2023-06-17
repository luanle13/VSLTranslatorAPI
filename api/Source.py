from Component import Component
from typing import List
from abc import ABC, abstractmethod
from Event import Event

"""
This class is the base class for all user-defined sources.

Properties:
name (String): The name of this source.
parallelism (int): The number of instances of this source.
"""
class Source(Component, ABC):
    def __init__(self, name: str, parallelism: int):
        super().__init__(name, parallelism)
    
    """
    Set up instance.

    Parameters:
    instance (int): The instance id (an index starting from 0) of this source instance.
    """
    @abstractmethod
    def setup_instance(self, instance: int):
        pass
    
    """
    Accept events from external into the system.

    Parameters:
    event_collector (list): The outgoing event collector.
    """
    @abstractmethod
    def get_events(self, event_collector: List[Event]):
        pass