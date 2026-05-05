import random
from typing import List, Dict
from .models import Job, Node

def random_scheduler(jobs: List[Job], nodes: List[Node]) -> Dict[str, List[Job]]:
    """
    Assigns each job to a randomly selected node.
    """
    if not nodes:
        raise ValueError("No nodes available for scheduling.")

    assignments: Dict[str, List[Job]] = {node.node_id: [] for node in nodes}
    node_current_utilization: Dict[str, float] = {node.node_id: 0.0 for node in nodes}

    for job in jobs:
        chosen_node = random.choice(nodes)
        assignments[chosen_node.node_id].append(job)
        node_current_utilization[chosen_node.node_id] += job.workload_cu

    for node in nodes:
        node.assigned_jobs = assignments[node.node_id]
        node.current_utilization_cu = node_current_utilization[node.node_id]

    return assignments

def shortest_job_first_scheduler(jobs: List[Job], nodes: List[Node]) -> Dict[str, List[Job]]:
    """
    Assigns jobs using the Shortest Job First (SJF) approach.
    Jobs are sorted by duration, and then assigned to the node that would finish earliest.
    """
    if not nodes:
        raise ValueError("No nodes available for scheduling.")

    sorted_jobs = sorted(jobs, key=lambda job: job.duration)

    assignments: Dict[str, List[Job]] = {node.node_id: [] for node in nodes}
    node_finish_times: Dict[str, float] = {node.node_id: 0.0 for node in nodes}
    node_current_utilization: Dict[str, float] = {node.node_id: 0.0 for node in nodes}


    for job in sorted_jobs:
        earliest_finish_node_id = min(node_finish_times, key=node_finish_times.get)
        
        assignments[earliest_finish_node_id].append(job)
        node_finish_times[earliest_finish_node_id] += job.duration 
        node_current_utilization[earliest_finish_node_id] += job.workload_cu

    for node in nodes:
        node.assigned_jobs = assignments[node.node_id]
        node.current_utilization_cu = node_current_utilization[node.node_id]

    return assignments

def round_robin_scheduler(jobs: List[Job], nodes: List[Node]) -> Dict[str, List[Job]]:
    """
    Assigns jobs to nodes in a round-robin fashion.
    """
    if not nodes:
        raise ValueError("No nodes available for scheduling.")

    assignments: Dict[str, List[Job]] = {node.node_id: [] for node in nodes}
    node_current_utilization: Dict[str, float] = {node.node_id: 0.0 for node in nodes}

    node_count = len(nodes)
    for i, job in enumerate(jobs):
        chosen_node = nodes[i % node_count]
        assignments[chosen_node.node_id].append(job)
        node_current_utilization[chosen_node.node_id] += job.workload_cu

    for node in nodes:
        node.assigned_jobs = assignments[node.node_id]
        node.current_utilization_cu = node_current_utilization[node.node_id]

    return assignments

