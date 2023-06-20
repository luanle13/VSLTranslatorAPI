from .instance_executor import InstanceExecutor


"""
The executor for source components. 
When the executor is started, a new thread is created to call the get_events() function of the source component repeatedly.

Properties:
instance_id (int): The ID of this instance.
source (Source): The source of this instance.
"""
class SourceInstanceExecutor(InstanceExecutor):
    def __init__(self, instance_id, source):
        super().__init__()
        self.instance_id = instance_id
        self.source = source
        self.source.setup_instance(instance_id)
    
    """
    Run the process once.

    Returns:
    bool: True if the thread should continue; False if the thread should exit.
    """
    def run_once(self):
        try:
            self.source.get_events(self.event_collector)
            for event in self.event_collector:
                self.outgoing_queue.put(event)
            self.event_collector.clear()
            return True
        except Exception as e:
            print(e)
            return False