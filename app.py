import streamlit as st
import pandas as pd
import plotly.express as px
import time
from typing import List, Dict, Any

from src.models import Job, Node
from src.data_loader import load_jobs_from_csv
from src.engine import SimulationEngine
from src.baselines import random_scheduler, shortest_job_first_scheduler, round_robin_scheduler
from src.optimizers import GeneticAlgorithmOptimizer, PSO

# --- 1. PAGE CONFIG & MATURE UI STYLING ---
st.set_page_config(page_title="Cloud Task Scheduler", layout="wide")

st.markdown("""
    <style>
    .terminal-log {
        background-color: #0e1117; color: #4cd7f6; font-family: 'JetBrains Mono', 'Courier New', monospace;
        padding: 15px; border-radius: 8px; height: 250px; overflow-y: auto; 
        border: 1px solid #303638; box-shadow: inset 0 0 10px rgba(0,0,0,0.5);
    }
    .system-title { font-weight: 700; color: #e0e0e0; margin-bottom: 0px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='system-title'>Cloud Task Scheduler</h1>", unsafe_allow_html=True)
st.markdown("Evaluate scheduling policies for cloud job placement with cost and makespan metrics.")
st.markdown("---")


def _default_nodes() -> List[Dict[str, Any]]:
    return [
        {"node_id": "node_1", "instance": "t2.micro", "speed_cu": 1.0, "cost_per_hour": 0.0116},
        {"node_id": "node_2", "instance": "t3.small", "speed_cu": 2.0, "cost_per_hour": 0.0208},
        {"node_id": "node_3", "instance": "c6g.medium", "speed_cu": 4.0, "cost_per_hour": 0.0340},
        {"node_id": "node_4", "instance": "m5.large", "speed_cu": 8.0, "cost_per_hour": 0.0960},
        {"node_id": "node_5", "instance": "r5.large", "speed_cu": 16.0, "cost_per_hour": 0.1260},
    ]


def _ensure_custom_nodes() -> None:
    if "custom_nodes" not in st.session_state:
        st.session_state["custom_nodes"] = _default_nodes()


def _build_nodes_from_state() -> List[Node]:
    return [
        Node(
            node_id=node_cfg["node_id"],
            capacity_cu=float(node_cfg["speed_cu"]),
            price_per_hour=float(node_cfg["cost_per_hour"]),
        )
        for node_cfg in st.session_state["custom_nodes"]
    ]


# --- 2. CORE SIMULATION FUNCTION ---
def run_simulation(
    jobs: List[Job],
    nodes: List[Node],
    scheduler_name: str,
    pop_size: int,
    generations: int,
) -> Dict[str, Any]:
    engine = SimulationEngine(jobs, nodes)
    
    if scheduler_name == "Random":
        assignments = engine.run_scheduling(random_scheduler)
    elif scheduler_name == "Shortest Job First (SJF)":
        assignments = engine.run_scheduling(shortest_job_first_scheduler)
    elif scheduler_name == "Round Robin (RR)":
        assignments = engine.run_scheduling(round_robin_scheduler)
    elif scheduler_name == "Genetic Algorithm (GA)":
        ga_optimizer = GeneticAlgorithmOptimizer(
            jobs,
            nodes,
            population_size=pop_size,
            generations=generations,
        )
        assignments = ga_optimizer.optimize()
    elif scheduler_name == "Particle Swarm (PSO)":
        pso_optimizer = PSO(jobs, nodes, swarm_size=pop_size, max_iter=generations)
        assignments = pso_optimizer.optimize()
    else:
        return {}

    # Update node utilization for metrics
    for node in nodes:
        node.assigned_jobs = assignments.get(node.node_id, [])
        node.current_utilization_cu = sum(job.workload_cu for job in node.assigned_jobs)

    return {
        "makespan": engine.calculate_makespan(),
        "cost": engine.calculate_execution_cost(),
        "utilization": engine.calculate_resource_utilization(),
        "assignments": assignments
    }

# --- 3. SIDEBAR: CLOUD CONFIGURATION ---
_ensure_custom_nodes()

st.sidebar.header("Cluster Nodes")
nodes_df = pd.DataFrame(st.session_state["custom_nodes"]).rename(
    columns={
        "node_id": "Node",
        "instance": "Instance",
        "speed_cu": "Speed (CU)",
        "cost_per_hour": "Cost ($/hr)",
    }
)
st.sidebar.dataframe(nodes_df, use_container_width=True, hide_index=True)

st.sidebar.subheader("Add Node")
new_speed = st.sidebar.number_input("Speed (CU)", min_value=0.1, value=2.0, step=0.1)
new_cost = st.sidebar.number_input("Cost ($/hr)", min_value=0.0, value=0.02, step=0.0001, format="%.4f")

if st.sidebar.button("Add Node", use_container_width=True):
    next_index = len(st.session_state["custom_nodes"]) + 1
    st.session_state["custom_nodes"].append(
        {
            "node_id": f"node_{next_index}",
            "instance": "custom",
            "speed_cu": float(new_speed),
            "cost_per_hour": float(new_cost),
        }
    )
    st.rerun()

clear_col, reset_col = st.sidebar.columns(2)
if clear_col.button("Clear Nodes", use_container_width=True):
    st.session_state["custom_nodes"] = []
    st.rerun()
if reset_col.button("Reset Nodes", use_container_width=True):
    st.session_state["custom_nodes"] = _default_nodes()
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.header("Algorithm Selection")
scheduler_options = [
    "Shortest Job First (SJF)",
    "Round Robin (RR)",
    "Random",
    "Genetic Algorithm (GA)",
    "Particle Swarm (PSO)",
]
selected_schedulers = st.sidebar.multiselect(
    "Schedulers",
    scheduler_options,
    default=["Shortest Job First (SJF)", "Genetic Algorithm (GA)", "Particle Swarm (PSO)"],
)

st.sidebar.subheader("Optimizer Parameters")
pop_size = st.sidebar.slider("Population/Swarm Size", 10, 200, 30, step=5)
generations = st.sidebar.slider("Iterations", 10, 300, 60, step=5)
jobs_file_path = "data/clean_google_jobs.csv"

# --- 4. MAIN DASHBOARD: DATA PREP & LOGGING ---
col_log, col_data = st.columns([2, 1])

with col_data:
    st.subheader("Workload Data")
    if st.button("Load Workload Data", use_container_width=True):
        try:
            st.session_state['jobs'] = load_jobs_from_csv(jobs_file_path)
            st.success(f"Successfully loaded {len(st.session_state['jobs'])} jobs.")
        except Exception as e:
            st.error(f"Error loading jobs: Make sure {jobs_file_path} exists.")

    if 'jobs' in st.session_state:
        st.dataframe(pd.DataFrame([j.__dict__ for j in st.session_state['jobs']]).head(), use_container_width=True)

with col_log:
    st.subheader("Execution Log")
    log_placeholder = st.empty()
    logs = ["> System initialized. Waiting for execution command..."]
    log_placeholder.markdown("<div class='terminal-log'>" + "<br>".join(logs) + "</div>", unsafe_allow_html=True)
    
    if st.button("Run Simulation", type="primary", use_container_width=True):
        if 'jobs' not in st.session_state:
            st.error("Load workload data first.")
        elif not st.session_state["custom_nodes"]:
            st.error("Add at least one cluster node first.")
        elif not selected_schedulers:
            st.error("Select at least one scheduler.")
        else:
            def update_log(msg):
                logs.append(f"> {msg}")
                log_placeholder.markdown("<div class='terminal-log'>" + "<br>".join(logs) + "</div>", unsafe_allow_html=True)

            results = {}
            progress_bar = st.progress(0)
            total_steps = len(selected_schedulers)

            update_log(f"Using {len(st.session_state['custom_nodes'])} configured cluster nodes.")
            
            for i, scheduler_name in enumerate(selected_schedulers):
                update_log(f"Running {scheduler_name}...")
                time.sleep(0.2)
                
                sim_nodes = _build_nodes_from_state()
                
                simulation_results = run_simulation(
                    st.session_state['jobs'],
                    sim_nodes,
                    scheduler_name,
                    pop_size,
                    generations,
                )
                results[scheduler_name] = simulation_results
                
                update_log(
                    f"{scheduler_name} finished. Makespan: {simulation_results['makespan']:.2f}s | Cost: ${simulation_results['cost']:.4f}"
                )
                progress_bar.progress((i + 1) / total_steps)

            st.session_state['simulation_results'] = results
            update_log("Simulation complete.")
            time.sleep(0.2)

# --- 5. RESULTS & VISUALIZATIONS ---
if 'simulation_results' in st.session_state:
    st.markdown("---")
    st.header("Simulation Results")
    all_results = st.session_state['simulation_results']

    # KPI Layout
    makespan_data = [{"Algorithm": name, "Makespan": res['makespan']} for name, res in all_results.items()]
    cost_data = [{"Algorithm": name, "Cost": res['cost']} for name, res in all_results.items()]
    util_data = [{"Algorithm": name, "Utilization": res['utilization']} for name, res in all_results.items()]

    chart_col1, chart_col2, chart_col3 = st.columns(3)

    with chart_col1:
        fig_time = px.bar(makespan_data, x='Algorithm', y='Makespan', title='Makespan', color='Algorithm')
        st.plotly_chart(fig_time, use_container_width=True)

    with chart_col2:
        fig_cost = px.bar(cost_data, x='Algorithm', y='Cost', title='Total Cost', color='Algorithm')
        st.plotly_chart(fig_cost, use_container_width=True)

    with chart_col3:
        fig_util = px.bar(util_data, x='Algorithm', y='Utilization', title='Resource Utilization', color='Algorithm')
        fig_util.update_layout(yaxis_tickformat='.0%')
        st.plotly_chart(fig_util, use_container_width=True)

    # --- BUG FIX: THE ASSIGNMENT INSPECTOR ---
    st.markdown("### Node Assignment Inspector")
    st.markdown("Expand each scheduler to inspect node-level assignments.")
    
    for scheduler_name, res in all_results.items():
        with st.expander(f"Scheduler: {scheduler_name}"):
            assignment_data = []
            for node_id, assigned_jobs in res['assignments'].items():
                job_ids = [str(j.job_id) for j in assigned_jobs]
                total_cu = sum(j.workload_cu for j in assigned_jobs)
                assignment_data.append({
                    "Node ID": node_id,
                    "Total Jobs Assigned": len(assigned_jobs),
                    "Total Workload (CU)": round(total_cu, 2),
                    "Job IDs": ", ".join(job_ids) if job_ids else "IDLE"
                })
            
            # Using standard dataframe solves all custom object rendering bugs
            df_assignments = pd.DataFrame(assignment_data)
            st.dataframe(df_assignments, use_container_width=True, hide_index=True)
