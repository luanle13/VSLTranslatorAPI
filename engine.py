from threading import Thread
from abc import ABC
from queue import Queue
from api import *
import copy


QUEUE_SIZE = 64


"""
The class for intermediate event queues between processes.

Properties:
size (int): The maximum size of the queue.
"""
class EventQueue(Queue):
    def __init__(self, size):
        super().__init__(size)


"""
This is the base class of all processes, including executors and stream managers.
When a process is started, a new thread is created to call the runOnce() function of the derived class.
Each process also have an incoming event queue and outgoing event queue.
"""
class Process(ABC):
    def __init__(self):
        super().__init__()
        self.thread = Thread(target=self.run)
    
    """
    Start the process
    """
    def start(self):
        self.thread.start()
    
    """
    Continuously run the process.
    """
    def run(self):
        while self.run_once():
            pass
    
    """
    Run process once.
    """
    def run_once(self):
        raise NotImplementedError


"""
The executor for source components. 
When the executor is started, a new thread is created to call the get_events() function of the source component repeatedly.

Properties
event_collector (list): This list is used for accepting events from user logic.
incoming_queue (EventQueue): Data queue for the upstream process
outgoing_queue (EventQueue): Data queue for the downstream process
"""
class InstanceExecutor(Process):
    def __init__(self):
        super().__init__()
        self.event_collector = []
        self.incoming_queue = None
        self.outgoing_queue = None

    """
    Set the data queue for the upstream process.

    Parameters:
    queue (EventQueue): Data queue for the upstream process.
    """
    def set_incoming_queue(self, queue):
        self.incoming_queue = queue
    
    """
    Set the data queue for the downstream process.

    Parameters:
    queue (EventQueue): Data queue for the downstream process.
    """
    def set_outgoing_queue(self, queue):
        self.outgoing_queue = queue


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
        

"""
The base class for executors of source and operator.

Parameters:
component (Component): The component which this executor executes.
"""
class ComponentExecutor(ABC):
    def __init__(self, component):
        self.component = component
        parallelism = component.get_parallelism()
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
    def get_instance_executors(self):
        return self.instance_executors

    """
    Get the component of this component executor.
    
    Returns:
    Component: The component of thsi component executor.
    """
    def get_component(self):
        return self.component
    
    """
    Set the incoming queues of this component executor.
    
    Parameters:
    queues (list): The list of incoming queues of this component executor.
    """
    def set_incoming_queue(self, queues):
        for i, queue in enumerate(queues):
            self.instance_executors[i].set_incoming_queue(queue)

    """
    Set the outgoing queue of this component executor.

    Parameters:
    queue (EventQueue): The outgoing queue of this component executor.
    """
    def set_outgoing_queue(self, queue):
        for instance in self.instance_executors:
            instance.set_outgoing_queue(queue)


"""
The executor for operator components.
When the executor is started, a new thread is created to call the apply() function of the operator component repeatedly.
"""
class OperatorExecutor(ComponentExecutor):
    def __init__(self, operator):
        super().__init__(operator)
        self.operator = operator
        self.instance_executors = []
        for i in range(operator.get_parallelism()):
            cloned = copy.deepcopy(operator)
            self.instance_executors.append(OperatorInstanceExecutor(i, cloned))

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
    def get_grouping_strategy(self):
        return self.operator.get_grouping_strategy()


"""
The executor for source components.
When the executor is started, a new thread is created to call the get_events() function of the source component repeatedly.

Parameters:
source (Source): The source which this executor executes.
"""
class SourceExecutor(ComponentExecutor):
    def __init__(self, source):
        super().__init__(source)
        self.source = source
        self.instance_executors = []
        for i in range(source.get_parallelism()):
            cloned = copy.deepcopy(source)
            self.instance_executors.append(SourceInstanceExecutor(i, cloned))
    
    """
    Start instance executors (real processes) of this component.
    """
    def start(self):
        if self.instance_executors is not None:
            for instance in self.instance_executors:
                instance.start()
    
    """
    Set the incoming queues of this source executor.
    
    Parameters:
    queues (list): The list of incoming queues of this source executor.
    """
    def set_incoming_queue(self, queues):
        raise Exception("No incoming queue is allowed for source executor")


"""
Responsible for transporting events form the incoming queue to the outgoing queues with a grouping strategy.
"""
class EventDispatcher(Process):
    def __init__(self, downstream_executor):
        super().__init__()
        self.downstream_executor = downstream_executor
        self.incoming_queue = None
        self.outgoing_queue = None
    
    """
    Run process once.
    """
    def run_once(self):
        try:
            event = self.incoming_queue.get()
            grouping: GroupingStrategy = self.downstream_executor.get_grouping_strategy()
            instance = grouping.get_instance(event, len(self.outgoing_queue))
            self.outgoing_queue[instance].put(event)
        except Exception:
            return False
        return True

    """
    Set the incoming queue of this dispatcher.

    Parameters:
    queue (EventQueue): The incoming queue of this dispatcher.
    """
    def set_incoming_queue(self, queue):
        self.incoming_queue = queue
    
    """
    Set the list of outgoing queues of this dispatcher.

    Parameters:
    queues (list): The list of ougoing queues of this dispatcher.
    """
    def set_outgoing_queues(self, queues):
        self.outgoing_queue = queues


"""
A util data class for connections between components.

Properties:
from_executor (ComponentExecutor): The component which is the start of the connection.
to_executor (OperatorExecutor): The component which is the end of the connection.
"""
class Connection:
    def __init__(self, from_executor, to_executor):
        self.from_executor = from_executor
        self.to_executor = to_executor


class Node(dict):
    def __init__(self, name, parallelism):
        super().__init__()
        self["name"] = name
        self["parallelism"] = str(parallelism)

class Edge(dict):
    def __init__(self, from_node, to_node):
        super().__init__()
        self["from"] = from_node["name"]
        self["to"] = to_node["name"]
        self["from_parallelism"] = from_node["parallelism"]
        self["to_parallelism"] = to_node["parallelism"]

class WebServer:
    def __init__(self, job_name, connection_list):
        self.job_name = job_name
        self.sources = []
        self.operators = []
        self.edges = []
        incoming_count_map = {}
        for connection in connection_list:
            from_node = Node(connection.from_executor.get_component().get_name(), connection.from_executor.get_component().get_parallelism())
            to_node = Node(connection.to_executor.get_component().get_name(), connection.to_executor.get_component().get_name())

            count = incoming_count_map.get(to_node, 0)
            incoming_count_map[from_node] = count
            count = incoming_count_map.get(to_node, 0)
            incoming_count_map[to_node, count + 1]
            self.edges.append(Edge(from_node, to_node))
        for n, c in incoming_count_map.items():
            if c == 0:
                self.sources.append(n)
            else:
                self.operators.append(n)
        
    def start(self):
        pass

    def index_handler(self, ctx):
        pass

    def plan_handler(self, ctx):
        pass


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