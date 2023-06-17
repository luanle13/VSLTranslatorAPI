from InstanceExecutor import InstanceExecutor
from api.Operator import Operator
from api.Event import Event

"""
The executor for operator components.
When the executor is started, a new thread is created to call the apply() function of the operator component repeatedly
"""
class OperatorInstanceExecutor(InstanceExecutor):
    def __init__(self, instance_id: int, operator: Operator) -> None:
        super.__init__(self)
        self.instance_id = instance_id
        self.operator = operator
        self.operator.setup_instance(instance_id)
    
    """
    Run process once.

    Returns:
    bool: True if the thread should continue; False if the thread should exit.
    """
    def run_once(self) -> bool:
        try:
            event: Event = self.incoming_queue.get()
        except KeyboardInterrupt:
            return False
        self.operator.apply(event, self.event_collector)
        try:
            for output in self.event_collector:
                self.outgoing_queue.put(output)
            self.event_collector.clear()
        except KeyboardInterrupt:
            return False
        return True