from Operator import Operator
from Stream import Stream

"""
The Stream class represents a data stream coming out of a component.
Operators with the correct type can be applied to this stream.

Properties:
operator_set (set): List of all operators to be applied to this stream.
"""
class Stream:
    def __init__(self):
        self.operator_set = set()
    
    """
    Apply an operator to this stream.

    Parameters:
    operator (Operator): The operator to be connected to the current stream.

    Returns:
    Stream: The outgoing stream of the operator.
    """
    def apply_operator(self, operator: Operator) -> Stream:
        if operator in self.operator_set:
            raise Exception(f"Operator {operator.getName()} is added to job twice")
        self.operator_set.add(operator)
        return operator.get_outgoing_stream()
    
    """
    Get the collection of operators applied to this stream.

    Returns:
    list: The collection of operators applied to this stream.
    """
    def get_applied_operators(self):
        return self.operator_set