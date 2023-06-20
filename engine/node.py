class Node(dict):
    def __init__(self, name, parallelism):
        super().__init__()
        self["name"] = name
        self["parallelism"] = str(parallelism)