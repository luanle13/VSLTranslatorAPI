from Stream import Stream

"""
The base class for all components, including Source and Operator

Properties:
name (string): The name of this component.
parallelism (int): The number of instances of this component.
outgoing_stream (Stream): The outgoing event stream of this component. The stream is used to connect the downstream components
"""
class Component:
    def __init__(self, name, parallelism) -> None:
        self.name = name
        self.parallelism = parallelism
        self.outgoing_stream = Stream()

    """
    Get the name of this component.

    Returns
    string: The name of this component.
    """
    def get_name(self):
        return self.name

    """
    Get the parallelism (number of instances) of this component.

    Returns:
    int: The parallelism (number of instances) of this component.
    """
    def get_parallelism(self):
        return self.parallelism

    """
    Get the outgoing event stream of this component. The stream is used to connect the downstream components.

    Returns:
    Stream: The outgoing event stream of this component. The stream is used to connect the downstream components
    """
    def get_outgoing_stream(self):
        return self.outgoing_stream
