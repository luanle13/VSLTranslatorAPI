from Source import Source
from Stream import Stream

"""
The class is used by users to set up their jobs and run.

Properties:
name (str): The name of this job.
source_set (set): The list of sources in this job.
"""
class Job:
    def __init__(self, job_name: str) -> None:
        self.name = job_name
        self.source_set = set()
    
    """
    Add a source into the job.
    A stream is returned which will be used to connect to other operators.

    Parameters:
    source (Source): The source object to be added into the job.

    Returns:
    stream (Stream): A stream that can be used to connect to other operators.
    """
    def add_source(self, source: Source) -> Stream:
        if source in self.source_set:
            raise Exception(f"Source {source.get_name()} is added to job twice")
        self.source_set.add(source)
        return source.get_outgoing_stream()

    """
    Get the name of this job.

    Returns:
    str: The name of this job.
    """
    def get_name(self) -> str:
        return self.name
    
    """
    Get the list of sources in this job.
    This function is used by JobRunner to traverse the graph.

    Returns:
    The list of sources in this job.
    """
    def get_sources(self) -> set:
        return self.source_set