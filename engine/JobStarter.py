from ComponentExecutor import ComponentExecutor
from EventDispatcher import EventDispatcher
from Connection import Connection
from api.Source import Source
from SourceExecutor import SourceExecutor
from EventQueue import EventQueue
from api.Operator import Operator
from api.Component import Component
from api.Stream import Stream
from OperatorExecutor import OperatorExecutor
from api.Job import Job
from typing import List
from WebServer import WebServer

QUEUE_SIZE = 64

"""
This class start a job by setting up executors for all the components, building connections to connect the components together, and starting all the processes.

Properties:
job (Job): The job to start.
executor_list (list): The list of executors of this job.
dispatcher_list (list): The list of stream managers of this job.
connection_list (list): The list of connections between component executors.
"""
class JobStarter:
    def __init__(self, job: Job) -> None:
        self.job = job 
        self.executor_list = List[ComponentExecutor]
        self.dispatcher_list = List[EventDispatcher]
        self.connection_list = List[Connection]

    """
    Responsible for starting the job by setting up executors for all the components, building connections between them, starting all the processes, and finally starting the web server.
    """
    def start(self):
        self.setup_component_executors()
        self.setup_connections()
        self.start_processes()
        WebServer(self.job.get_name(), self.connection_list).start()

    """
    Create all source and operator executors.
    """
    def setup_component_executors(self):
        for source in self.job.get_sources():
            executor: SourceExecutor = SourceExecutor(source)
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
    def connect_executors(self, connection: Connection):
        dispatcher: EventDispatcher = EventDispatcher(connection.to_executor)
        self.dispatcher_list.append(dispatcher)
        upstream: EventQueue = EventQueue(QUEUE_SIZE)
        connection.from_executor.set_outgoing_queue(upstream)
        dispatcher.set_incoming_queue(upstream)
        parallelism: int = connection.to_executor.get_component().get_parallelism()
        downstream: List[EventQueue] = []
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
    def traverse_component(self, component: Component, executor: ComponentExecutor):
        stream: Stream = component.get_outgoing_stream()
        for operator in stream.get_applied_operators():
            operator_executor = OperatorExecutor(operator)
            self.executor_list.append(operator_executor)
            self.connection_list.append(Connection(executor, operator_executor))
            self.traverse_component(operator, operator_executor)