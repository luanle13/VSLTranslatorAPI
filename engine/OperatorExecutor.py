from ComponentExecutor import ComponentExecutor
from InstanceExecutor import InstanceExecutor
from api.Operator import Operator
from api.GroupingStrategy import GroupingStrategy
from OperatorInstanceExecutor import OperatorInstanceExecutor
from typing import List
import copy

"""
The executor for operator components.
When the executor is started, a new thread is created to call the apply() function of the operator component repeatedly.
"""
class OperatorExecutor(ComponentExecutor):
    def __init__(self, operator: Operator) -> None:
        super().__init__(operator)
        self.operator = operator
        self.instance_executors: List[OperatorInstanceExecutor] = []
        for i in range(operator.get_parallelism()):
            cloned = copy.deepcopy(operator)
            self.instance_executors.append(OperatorInstanceExecutor(cloned))

    """
    Start instance executors (real processes) of this operator.
    """
    def start(self):
        if self.instance_executors is not None:
            for executor in self.instance_executors:
                executor.start()

    """
    Get the grouping strategy of this operator executor.

    Returns:
    GroupingStrategy: The grouping strategy of this operator executor.
    """
    def get_grouping_strategy(self) -> GroupingStrategy:
        return self.operator.get_grouping_strategy()