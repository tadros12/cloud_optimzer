import streamlit as st
from typing import List, Dict, Any
import pandas as pd
import plotly.express as px

from src.models import Job, Node
from src.data_loader import load_jobs_from_csv, generate_nodes
from src.engine import SimulationEngine
from src.baselines import random_scheduler, shortest_job_first_scheduler, round_robin_scheduler
from src.optimizers import GeneticAlgorithmOptimizer
from src.dashboard import visualize_schedule

st.set_page_config(layout="wide")

def run_simulation(jobs: List[Job], nodes: List[Node], scheduler_name: str) -> Dict[str, Any]:
    """
    Runs a simulation with the specified scheduler and returns results.
    """
    engine = SimulationEngine(jobs, nodes)
    
    if scheduler_name == "Random":
        assignments = engine.run_scheduling(random_scheduler)
    elif scheduler_name == "Shortest Job First (SJF)":
        assignments = engine.run_scheduling(shortest_job_first_scheduler)
    elif scheduler_name == "Round Robin (RR)":
        assignments = engine.run_scheduling(round_robin_scheduler)
    elif scheduler_name == "Genetic Algorithm (GA)":
        ga_optimizer = GeneticAlgorithmOptimizer(jobs, nodes)
        assignments = ga_optimizer.optimize()
    else:
        st.error(f"Unknown scheduler: {scheduler_name}")
        return {}

    # Update actual node objects with assignments and utilization for metric calculation
    for node in nodes:
        node.assigned_jobs = assignments.get(node.node_id, [])
        node.current_utilization_cu = sum(job.workload_cu for job in node.assigned_jobs)

    makespan = engine.calculate_makespan()
    cost = engine.calculate_execution_cost()
    utilization = engine.calculate_resource_utilization()

    return {
        "makespan": makespan,
        "cost": cost,
        "utilization": utilization,
        "assignments": assignments
    }


st.title("Cloud Task Scheduling Optimization Simulator")

# --- Sidebar for Configuration ---
st.sidebar.header("Simulation Configuration")

num_nodes = st.sidebar.slider("Number of Nodes", 1, 20, 5)

st.sidebar.subheader("Node Configurations")
if 'node_configs' not in st.session_state or len(st.session_state['node_configs']) != num_nodes:
    st.session_state['node_configs'] = pd.DataFrame({
        "node_id": [f"node_{i+1}" for i in range(num_nodes)],
        "capacity_cu": [500.0] * num_nodes,
        "price_per_hour": [0.10] * num_nodes
    })

node_configs_df = st.sidebar.data_editor(st.session_state['node_configs'], num_rows="fixed", hide_index=True)

jobs_file_path = "data/clean_google_jobs.csv"

st.header("1. Data Loading")
if st.button("Load Jobs Data"):
    if jobs_file_path:
        try:
            jobs = load_jobs_from_csv(jobs_file_path)
            st.session_state['jobs'] = jobs
            st.success(f"Loaded {len(jobs)} jobs from {jobs_file_path}")
            st.dataframe(pd.DataFrame([job.__dict__ for job in jobs]).head())
        except FileNotFoundError:
            st.error(f"Error: '{jobs_file_path}' not found. Make sure it's in the project root.")
        except Exception as e:
            st.error(f"Error loading jobs data: {e}")
    else:
        st.warning("Please specify a jobs CSV file path.")

if 'jobs' not in st.session_state:
    st.info("Please load jobs data to proceed.")
    st.stop()

jobs = st.session_state['jobs']
nodes = [Node(row['node_id'], row['capacity_cu'], row['price_per_hour']) for _, row in node_configs_df.iterrows()]
st.write(f"Configured {len(nodes)} nodes based on your settings.")

# --- Select and Run Schedulers ---
st.header("2. Run Schedulers")
scheduler_options = ["Random", "Round Robin (RR)", "Shortest Job First (SJF)", "Genetic Algorithm (GA)"]
selected_schedulers = st.multiselect("Select Scheduling Algorithms to Compare", scheduler_options, default=["Random", "Shortest Job First (SJF)", "Genetic Algorithm (GA)"])

if st.button("Run Simulations"):
    results = {}
    for scheduler_name in selected_schedulers:
        st.subheader(f"Running {scheduler_name} Scheduler...")
        
        # Create fresh nodes for each simulation run to ensure fair comparison
        sim_nodes = [Node(row['node_id'], row['capacity_cu'], row['price_per_hour']) for _, row in node_configs_df.iterrows()] 
        
        simulation_results = run_simulation(jobs, sim_nodes, scheduler_name)
        if simulation_results:
            results[scheduler_name] = simulation_results
            st.write(f"**{scheduler_name} Results:**")
            st.write(f"Makespan: {simulation_results['makespan']:.2f}")
            st.write(f"Cost: ${simulation_results['cost']:.2f}")
            st.write(f"Utilization: {simulation_results['utilization']:.2%}")
            
            with st.expander(f"View {scheduler_name} Assignments"):
                visualize_schedule(simulation_results['assignments'], sim_nodes)

    if results:
        st.session_state['simulation_results'] = results
        st.success("Simulations completed!")

# --- Display Results and Visualizations ---
if 'simulation_results' in st.session_state:
    st.header("3. Simulation Results & Visualizations")
    all_results = st.session_state['simulation_results']

    makespan_data = [{"Algorithm": name, "Makespan": res['makespan']} for name, res in all_results.items()]
    cost_data = [{"Algorithm": name, "Cost": res['cost']} for name, res in all_results.items()]
    utilization_data = [{"Algorithm": name, "Utilization": res['utilization']} for name, res in all_results.items()]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Makespan Comparison")
        fig_makespan = px.bar(makespan_data, x='Algorithm', y='Makespan', title='Makespan Comparison')
        st.plotly_chart(fig_makespan, use_container_width=True)

    with col2:
        st.subheader("Cost Comparison")
        fig_cost = px.bar(cost_data, x='Algorithm', y='Cost', title='Execution Cost Comparison')
        st.plotly_chart(fig_cost, use_container_width=True)

    with col3:
        st.subheader("Utilization Comparison")
        fig_util = px.bar(utilization_data, x='Algorithm', y='Utilization', title='Resource Utilization Comparison')
        st.plotly_chart(fig_util, use_container_width=True)