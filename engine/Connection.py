from ComponentExecutor import ComponentExecutor
from OperatorExecutor import OperatorExecutor

"""
A util data class for connections between components.

Properties:
from_executor (ComponentExecutor): The component which is the start of the connection.
to_executor (OperatorExecutor): The component which is the end of the connection.
"""
class Connection:
    def __init__(self, from_executor: ComponentExecutor, to_executor: OperatorExecutor) -> None:
        self.from_executor: ComponentExecutor = from_executor
        self.to_executor: OperatorExecutor = to_executor