from .node import Node
from .edge import Edge


"""
A util data class for connections between components.

Properties:
from_executor (ComponentExecutor): The component which is the start of the connection.
to_executor (OperatorExecutor): The component which is the end of the connection.
"""
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