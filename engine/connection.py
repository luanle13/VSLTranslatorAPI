class Connection:
    def __init__(self, from_executor, to_executor):
        self.from_executor = from_executor
        self.to_executor = to_executor