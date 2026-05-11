import sys
import webview
import json
import random
import threading
from src.data_loader import generate_nodes, load_jobs_from_csv
from src.optimizers import GeneticAlgorithmOptimizer, GreyWolfOptimizer, ParticleSwarmOptimizer, BeeColonyOptimization, WhaleOptimizationOptimizer
from src.models import Job
from src.baselines import round_robin_scheduler, shortest_job_first_scheduler
from src.engine import SimulationEngine

class Api:
    def __init__(self):
        self.nodes = generate_nodes()
        try:
            self.jobs = load_jobs_from_csv("data/clean_google_jobs.csv")
        except:
            self.jobs = [Job(job_id=f"job_{i}", workload_cu=float(i*2), duration=float(i)) for i in range(1, 101)]
        self._window = None

    def set_window(self, window):
        self._window = window

    def log(self, message):
        print(message)
        if self._window:
            safe_msg = message.replace('\\', '\\\\').replace('`', '\\`')
            try:
                self._window.evaluate_js(f"window.addDebugLog(`{safe_msg}`)")
            except:
                pass

    def get_nodes(self):
        """Returns the current list of nodes for the UI table."""
        node_data = []
        for n in self.nodes:
            node_data.append({
                "id": n.node_id,
                "capacity": n.capacity_cu,
                "price": n.price_per_hour
            })
        return node_data

    def update_node(self, node_id, capacity, price):
        for n in self.nodes:
            if n.node_id == node_id:
                n.capacity_cu = float(capacity)
                n.price_per_hour = float(price)
                return True
        return False

    def add_node(self, node_id, capacity, price):
        from src.models import Node
        self.nodes.append(Node(node_id=node_id, capacity_cu=float(capacity), price_per_hour=float(price)))
        return True

    def delete_node(self, node_id):
        self.nodes = [n for n in self.nodes if n.node_id != node_id]
        return True

    def run_simulation(self, payload):
        mode = payload.get("mode", "Single")
        algo1 = payload.get("algo1", "GA")
        algo2 = payload.get("algo2", "PSO")
        pop_size = int(payload.get("pop_size", 20))
        seed = int(payload.get("seed", 42))
        iter1 = int(payload.get("iter1", 50))
        iter2 = int(payload.get("iter2", 50))
        params1 = payload.get("params1", {})
        params2 = payload.get("params2", {})

        random.seed(seed)

        def run_algo(algo, iters, initial_pop, params):
            ext_freq = int(params.get("ext_freq", 0))
            ext_percent = float(params.get("ext_percent", 0.10))
            cost_weight = float(params.get("cost_weight", 0.5))
            if algo == "GA":
                pc = float(params.get("pc", 0.95))
                pm = float(params.get("pm", 0.02))
                opt = GeneticAlgorithmOptimizer(self.jobs, self.nodes, population_size=pop_size, generations=iters, crossover_rate=pc, mutation_rate=pm, ext_freq=ext_freq, ext_percent=ext_percent, cost_weight=cost_weight, log_callback=self.log)
                return opt.optimize(initial_pop)
            elif algo == "PSO":
                w = float(params.get("w", 0.7))
                c1 = float(params.get("c1", 1.5))
                c2 = float(params.get("c2", 1.5))
                opt = ParticleSwarmOptimizer(self.jobs, self.nodes, population_size=pop_size, iterations=iters, inertia_weight=w, c1=c1, c2=c2, ext_freq=ext_freq, ext_percent=ext_percent, cost_weight=cost_weight, log_callback=self.log)
                return opt.optimize(initial_pop)
            elif algo == "GWO":
                opt = GreyWolfOptimizer(self.jobs, self.nodes, population_size=pop_size, iterations=iters, ext_freq=ext_freq, ext_percent=ext_percent, cost_weight=cost_weight, log_callback=self.log)
                return opt.optimize(initial_pop)
            elif algo == "BCO":
                nc = int(params.get("nc", 5))
                opt = BeeColonyOptimization(self.jobs, self.nodes, population_size=pop_size, iterations=iters, nc=nc, ext_freq=ext_freq, ext_percent=ext_percent, cost_weight=cost_weight, log_callback=self.log)
                return opt.optimize(initial_pop)
            elif algo == "WOA":
                b_val = float(params.get("woa_b", 1.0))
                opt = WhaleOptimizationOptimizer(self.jobs, self.nodes, population_size=pop_size, iterations=iters, b=b_val, ext_freq=ext_freq, ext_percent=ext_percent, cost_weight=cost_weight, log_callback=self.log)
                return opt.optimize(initial_pop)
            elif algo == "RR":
                assignments = round_robin_scheduler(self.jobs, self.nodes)
                engine = SimulationEngine(self.jobs, self.nodes)
                for node in self.nodes: node.assigned_jobs = assignments.get(node.node_id, [])
                makespan = engine.calculate_makespan()
                cost = engine.calculate_execution_cost()
                history = [((1.0 - cost_weight) * makespan) + (cost_weight * cost * 10)] * iters
                return assignments, makespan, cost, history, []
            elif algorithm == "SJF":
                assignments = shortest_job_first_scheduler(self.jobs, self.nodes)
                engine = SimulationEngine(self.jobs, self.nodes)
                for node in self.nodes: node.assigned_jobs = assignments.get(node.node_id, [])
                makespan = engine.calculate_makespan()
                cost = engine.calculate_execution_cost()
                history = [((1.0 - cost_weight) * makespan) + (cost_weight * cost * 10)] * iters
                return assignments, makespan, cost, history, []
            else:
                raise ValueError("Unknown algorithm")

        try:
            self.log(f"\n--- Starting {mode} Execution ---")
            if mode == "Single":
                assignments, ms, cost, hist, final_pop = run_algo(algo1, iter1, None, params1)
                algo_name = algo1
                self.log(f"--- {algo1} finished ---")
            else:
                _, _, _, hist1, pop1 = run_algo(algo1, iter1, None, params1)
                assignments, ms, cost, hist2, final_pop = run_algo(algo2, iter2, pop1, params2)
                hist = hist1 + hist2
                algo_name = f"{algo1} + {algo2}"
                self.log(f"--- Hybrid {algo_name} finished ---")

            # Serialize assignments
            serialized_assignments = {}
            for node_id, job_list in assignments.items():
                serialized_assignments[node_id] = [{"id": j.job_id, "workload": j.workload_cu, "duration": j.duration} for j in job_list]

            return {
                "mode": mode, "algorithm": algo_name,
                "makespan": round(ms, 2), "cost": round(cost, 2),
                "convergence_history": hist,
                "assignments": serialized_assignments
            }
        except Exception as e:
            print(f"Error: {e}")
            return {"error": str(e)}


if __name__ == '__main__':
    api = Api()
    window = webview.create_window(
        'Cloud Optimizer CI Dashboard', 
        'ui/stitch/code.html', 
        js_api=api,
        width=1300, 
        height=850
    )
    api.set_window(window)
    webview.start(debug=True)