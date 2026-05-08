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

def generate_nodes(num_nodes: int = 5, capacity_cu: float = 0.0, price_per_hour: float = 0.0) -> List[Node]:
    """
    Generates a list of Node objects representing AWS instances by default.
    """
    if num_nodes == 5 and capacity_cu == 0.0:
        aws_defaults = [
            {"id": "t2.micro", "capacity_cu": 1.0, "price": 0.0116},
            {"id": "t3.small", "capacity_cu": 2.0, "price": 0.0208},
            {"id": "c6g.medium", "capacity_cu": 4.0, "price": 0.034},
            {"id": "m5.large", "capacity_cu": 8.0, "price": 0.096},
            {"id": "r5.large", "capacity_cu": 16.0, "price": 0.126}
        ]
        nodes = []
        for instance in aws_defaults:
            nodes.append(Node(node_id=instance["id"], capacity_cu=instance["capacity_cu"], price_per_hour=instance["price"]))
        return nodes

    nodes = []
    for i in range(num_nodes):
        node = Node(node_id=f"node_{i+1}", capacity_cu=capacity_cu, price_per_hour=price_per_hour)
        nodes.append(node)
    return nodes
