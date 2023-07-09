"""
This class serves as the connection between two executors.

Properties:
from_executor (ComponentExecutor): The executor which send the data.
to_executor (ComponentExecutor): The executor which receive the data.
"""
class Connection:
    def __init__(self, from_executor, to_executor):
        self.from_executor = from_executor
        self.to_executor = to_executor