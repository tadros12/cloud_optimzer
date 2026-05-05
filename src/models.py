from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class Job:
    job_id: str
    workload_cu: float  # Workload in Compute Units
    duration: float     # Duration of the job

@dataclass
class Node:
    node_id: str
    capacity_cu: float  # Capacity in Compute Units
    price_per_hour: float = 0.0 # Price per hour of usage
    current_utilization_cu: float = 0.0 # Current utilized capacity in Compute Units
    assigned_jobs: List[Job] = field(default_factory=list) # Jobs assigned to this node

