class Edge(dict):
    def __init__(self, from_node, to_node):
        super().__init__()
        self["from"] = from_node["name"]
        self["to"] = to_node["name"]
        self["from_parallelism"] = from_node["parallelism"]
        self["to_parallelism"] = to_node["parallelism"]