import pandas as pd
import random
from typing import List
from .models import Job, Node

def load_jobs_from_csv(file_path: str) -> List[Job]:
    """
    Loads job data from a CSV file into a list of Job objects.
    If 'duration' is missing, it simulates a random duration between 1 and 10.
    """
    df = pd.read_csv(file_path)
    jobs = []
    has_duration = 'duration' in df.columns
    
    for index, row in df.iterrows():
        job = Job(
            job_id=str(row['job_id']),
            workload_cu=float(row['workload_cu']),
            duration=float(row['duration']) if has_duration else random.uniform(1.0, 10.0)
        )
        jobs.append(job)
    return jobs

def generate_nodes(num_nodes: int, capacity_cu: float, price_per_hour: float = 0.0) -> List[Node]:
    """
    Generates a list of Node objects with specified capacity.
    """
    nodes = []
    for i in range(num_nodes):
        node = Node(node_id=f"node_{i+1}", capacity_cu=capacity_cu, price_per_hour=price_per_hour)
        nodes.append(node)
    return nodes
