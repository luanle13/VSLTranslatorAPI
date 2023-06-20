from .source_executor import SourceExecutor
from .event_dispatcher import EventDispatcher
from .event_queue import EventQueue
from .operator_executor import OperatorExecutor
from .connection import Connection


QUEUE_SIZE = 128


"""
This class start a job by setting up executors for all the components, building connections to connect the components together, and starting all the processes.

Properties:
job (Job): The job to start.
executor_list (list): The list of executors of this job.
dispatcher_list (list): The list of stream managers of this job.
connection_list (list): The list of connections between component executors.
"""
class JobStarter:
    def __init__(self, job):
        self.job = job 
        self.executor_list = []
        self.dispatcher_list = []
        self.connection_list = []

    """
    Responsible for starting the job by setting up executors for all the components, building connections between them, starting all the processes, and finally starting the web server.
    """
    def start(self):
        self.setup_component_executors()
        self.setup_connections()
        self.start_processes()
        # WebServer(self.job.get_name(), self.connection_list).start()

    """
    Create all source and operator executors.
    """
    def setup_component_executors(self):
        for source in self.job.get_sources():
            executor = SourceExecutor(source)
            self.executor_list.append(executor)
            self.traverse_component(source, executor)
    
    """
    Set up connections (intermediate queues) between all component executors.
    """
    def setup_connections(self):
        for connection in self.connection_list:
            self.connect_executors(connection)
    
    """
    Start all the processes for the job.
    """
    def start_processes(self):
        self.executor_list.reverse()
        for executor in self.executor_list:
            executor.start()
        for dispatcher in self.dispatcher_list:
            dispatcher.start()
    
    """
    Connect the component executors in the job.

    Parameters:
    connection (Connection): The connection between upstream and downstream components.
    """
    def connect_executors(self, connection):
        dispatcher = EventDispatcher(connection.to_executor)
        self.dispatcher_list.append(dispatcher)
        upstream = EventQueue(QUEUE_SIZE)
        connection.from_executor.set_outgoing_queue(upstream)
        dispatcher.set_incoming_queue(upstream)
        parallelism = connection.to_executor.get_component().get_parallelism()
        downstream = []
        for i in range(parallelism):
            downstream.append(EventQueue(QUEUE_SIZE))
        connection.to_executor.set_incoming_queue(downstream)
        dispatcher.set_outgoing_queues(downstream)

    """
    Set up executors for the downstream operators.

    Parameters:
    component (Component): The component which is being traversed.
    executor (ComponentExecutor): The executor for the current component.
    """
    def traverse_component(self, component, executor):
        stream = component.get_outgoing_stream()
        for operator in stream.get_applied_operators():
            operator_executor = OperatorExecutor(operator)
            self.executor_list.append(operator_executor)
            self.connection_list.append(Connection(executor, operator_executor))
            self.traverse_component(operator, operator_executor)