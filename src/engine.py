from typing import List, Dict
from .models import Job, Node

class SimulationEngine:
    def __init__(self, jobs: List[Job], nodes: List[Node]):
        self.jobs = jobs
        self.nodes = nodes
        self.scheduled_jobs_on_nodes: Dict[str, List[Job]] = {node.node_id: [] for node in nodes}

    def run_scheduling(self, scheduler_function) -> Dict[str, List[Job]]:
        """
        Runs a scheduling algorithm and assigns jobs to nodes.
        The scheduler_function should take (jobs, nodes) and return assignments.
        """
        # Reset node utilization and assignments for a fresh run
        for node in self.nodes:
            node.current_utilization_cu = 0.0
            node.assigned_jobs = []

        self.scheduled_jobs_on_nodes = scheduler_function(self.jobs, self.nodes)
        return self.scheduled_jobs_on_nodes

    def calculate_makespan(self) -> float:
        """
        Calculates the makespan of the current schedule.
        (Max completion time among all nodes)
        """
        # This is a placeholder. Actual calculation needs job start/end times on nodes.
        # For now, let's assume makespan is sum of duration for all assigned jobs
        # on the most heavily loaded node.
        max_makespan = 0.0
        for node in self.nodes:
            node_makespan = sum(job.duration for job in node.assigned_jobs)
            if node_makespan > max_makespan:
                max_makespan = node_makespan
        return max_makespan

    def calculate_execution_cost(self) -> float:
        """
        Calculates the total execution cost based on each node's price per hour.
        """
        total_cost = 0.0
        for node in self.nodes:
            # We assume node_utilization_hours is the duration of jobs on that node.
            # And cost is based on the node's hourly rate multiplied by the time it runs jobs.
            # Simplified: total duration of jobs * node's price_per_hour
            node_running_time = sum(job.duration for job in node.assigned_jobs)
            total_cost += node_running_time * node.price_per_hour
        return total_cost

    def calculate_resource_utilization(self) -> float:
        """
        Calculates the average resource utilization across all nodes.
        """
        # Placeholder: Sum of utilized CU / Sum of total capacity CU
        total_utilized_cu = sum(node.current_utilization_cu for node in self.nodes)
        total_capacity_cu = sum(node.capacity_cu for node in self.nodes)
        if total_capacity_cu == 0:
            return 0.0
        return total_utilized_cu / total_capacity_cu

    def calculate_speedup(self) -> float:
        """
        Calculates the speedup compared to a baseline (e.g., single processor).
        Requires a reference makespan.
        """
        # Placeholder: Needs a sequential makespan as reference
        return 1.0 # Default if no reference

    def calculate_efficiency(self) -> float:
        """
        Calculates the efficiency of the schedule.
        (Speedup / Number of processors)
        """
        # Placeholder: Needs speedup and number of nodes
        num_nodes = len(self.nodes)
        if num_nodes == 0:
            return 0.0
        return self.calculate_speedup() / num_nodes
