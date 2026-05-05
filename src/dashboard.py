import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Any
from .models import Job, Node

def plot_makespan(results: Dict[str, float]):
    """
    Plots the makespan for different scheduling algorithms.
    `results` is a dictionary where keys are algorithm names and values are makespan.
    """
    algorithms = list(results.keys())
    makespans = list(results.values())

    plt.figure(figsize=(10, 6))
    sns.barplot(x=algorithms, y=makespans)
    plt.title('Makespan Comparison of Scheduling Algorithms')
    plt.xlabel('Scheduling Algorithm')
    plt.ylabel('Makespan (arbitrary units)')
    plt.grid(axis='y', linestyle='--')
    plt.tight_layout()
    plt.show()

def plot_costs(results: Dict[str, float]):
    """
    Plots the execution costs for different scheduling algorithms.
    `results` is a dictionary where keys are algorithm names and values are costs.
    """
    algorithms = list(results.keys())
    costs = list(results.values())

    plt.figure(figsize=(10, 6))
    sns.barplot(x=algorithms, y=costs)
    plt.title('Execution Cost Comparison of Scheduling Algorithms')
    plt.xlabel('Scheduling Algorithm')
    plt.ylabel('Cost ($)')
    plt.grid(axis='y', linestyle='--')
    plt.tight_layout()
    plt.show()

def plot_resource_utilization(results: Dict[str, float]):
    """
    Plots the resource utilization for different scheduling algorithms.
    `results` is a dictionary where keys are algorithm names and values are utilization (0-1).
    """
    algorithms = list(results.keys())
    utilization = list(results.values())

    plt.figure(figsize=(10, 6))
    sns.barplot(x=algorithms, y=utilization)
    plt.title('Resource Utilization Comparison of Scheduling Algorithms')
    plt.xlabel('Scheduling Algorithm')
    plt.ylabel('Average Resource Utilization')
    plt.ylim(0, 1)
    plt.grid(axis='y', linestyle='--')
    plt.tight_layout()
    plt.show()

def visualize_schedule(assignments: Dict[str, List[Job]], nodes: List[Node]):
    """
    Visualizes the job assignments on nodes (e.g., a Gantt chart style visualization).
    This is a conceptual placeholder and would require more detailed job start/end times.
    """
    print("Conceptual Visualization: Job assignments on nodes.")
    for node in nodes:
        jobs_on_node = assignments.get(node.node_id, [])
        job_names = [job.job_id for job in jobs_on_node]
        if job_names:
            print(f"Node {node.node_id}: {', '.join(job_names)}")
        else:
            print(f"Node {node.node_id}: No jobs assigned.")
