from GroupingStrategy import GroupingStrategy
from Component import Component
from ShuffleGrouping import ShuffleGrouping
from abc import ABC, abstractmethod
from Event import Event
from typing import List

"""
This is the base class for all user-defined operators.

Properties:
name (string): The name of this component.
parallelism (int): The number of instances of this component.
grouping (GroupingStrategy): The grouping strategy of this operator.
"""
class Operator(Component):
    def __init__(self, name: str, parallelism: int, grouping: GroupingStrategy=None) -> None:
        super().__init__(name, parallelism)
        self.grouping = grouping if grouping is not None else ShuffleGrouping()
    
    """
    Set up instance.

    Parameters:
    instance (int): The instance id (an index starting from 0) of this source instance.
    """
    @abstractmethod
    def setup_instance(self, instance: int) -> int:
        pass

    """
    Apply logic to the incoming event and generate results.
    
    Parameters:
    event (Event): The incoming event.
    event_collector (list): The outgoing event collector.
    """
    @abstractmethod
    def apply(self, event: Event, event_collector: List[Event]):
        pass

    """
    Get the grouping strategy of an event.

    Returns:
    GroupingStrategy: The grouping strategy of this opertator.
    """
    def get_grouping_strategy(self):
        return self.grouping