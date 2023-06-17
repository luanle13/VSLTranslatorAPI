from typing import List
from Connection import Connection

class Node(dict):
    def __init__(self, name: str, parallelism: str):
        super().__init__()
        self["name"] = name
        self["parallelism"] = str(parallelism)

class Edge(dict):
    def __init__(self, from_node: Node, to_node: Node):
        super().__init__()
        self["from"] = from_node["name"]
        self["to"] = to_node["name"]
        self["from_parallelism"] = from_node["parallelism"]
        self["to_parallelism"] = to_node["parallelism"]

class WebServer:
    def __init__(self, job_name: str, connection_list: List[Connection]) -> None:
        self.job_name = job_name
        self.sources = []
        self.operators = []
        self.edges = []
        incoming_count_map = {}
        for connection in connection_list:
            from_node: Node = Node(connection.from_executor.get_component().get_name(), connection.from_executor.get_component().get_parallelism())
            to_node: Node = Node(connection.to_executor.get_component().get_name(), connection.to_executor.get_component().get_name())

            count: int = incoming_count_map.get(to_node, 0)
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