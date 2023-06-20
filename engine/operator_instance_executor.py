from .instance_executor import InstanceExecutor


"""
The executor for operator components.
When the executor is started, a new thread is created to call the apply() function of the operator component repeatedly
"""
class OperatorInstanceExecutor(InstanceExecutor):
    def __init__(self, instance_id, operator):
        super().__init__()
        self.instance_id = instance_id
        self.operator = operator
        self.operator.setup_instance(instance_id)
    
    """
    Run process once.

    Returns:
    bool: True if the thread should continue; False if the thread should exit.
    """
    def run_once(self):
        try:
            event = self.incoming_queue.get()
            self.operator.apply(event, self.event_collector)
            for output in self.event_collector:
                self.outgoing_queue.put(output)
            self.event_collector.clear()
            return True
        except Exception as e:
            print(e)
            return False