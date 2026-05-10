import sys
import webview
import json
import random
import threading
from src.data_loader import generate_nodes
from src.optimizers import GeneticAlgorithmOptimizer, GreyWolfOptimizer, ParticleSwarmOptimizer, BeeColonyOptimization
from src.models import Job

class Api:
    def __init__(self):
        self.nodes = generate_nodes()
        self.jobs = [Job(job_id=f"job_{i}", workload_cu=float(i*2), duration=float(i)) for i in range(1, 11)]
        self._window = None

    def set_window(self, window):
        self._window = window

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

    def run_simulation(self, pop_size, iterations, algorithm, seed, hyperparams):
        """Runs the specified algorithm and returns real results."""
        pop_size = int(pop_size)
        iterations = int(iterations)
        seed = int(seed)
        
        print(f"Running {algorithm} with pop={pop_size}, iter={iterations}, seed={seed}, hyperparams={hyperparams}")
        
        # Set the random seed
        random.seed(seed)

        result_data = {
            "algorithm": algorithm,
            "makespan": 0.0,
            "cost": 0.0,
            "convergence_history": []
        }

        try:
            ext_freq = int(hyperparams.get("ext_freq", 0))
            ext_percent = float(hyperparams.get("ext_percent", 0.10))
            
            if algorithm == "GA":
                pc = float(hyperparams.get("pc", 0.95))
                pm = float(hyperparams.get("pm", 0.02))
                optimizer = GeneticAlgorithmOptimizer(self.jobs, self.nodes, population_size=pop_size, generations=iterations, crossover_rate=pc, mutation_rate=pm, ext_freq=ext_freq, ext_percent=ext_percent)
                assignments, makespan, cost, history = optimizer.optimize()
            elif algorithm == "PSO":
                w = float(hyperparams.get("w", 0.7))
                c1 = float(hyperparams.get("c1", 1.5))
                c2 = float(hyperparams.get("c2", 1.5))
                optimizer = ParticleSwarmOptimizer(self.jobs, self.nodes, population_size=pop_size, iterations=iterations, inertia_weight=w, c1=c1, c2=c2, ext_freq=ext_freq, ext_percent=ext_percent)
                assignments, makespan, cost, history = optimizer.optimize()
            elif algorithm == "GWO":
                optimizer = GreyWolfOptimizer(self.jobs, self.nodes, population_size=pop_size, iterations=iterations, ext_freq=ext_freq, ext_percent=ext_percent)
                assignments, makespan, cost, history = optimizer.optimize()
            elif algorithm == "BCO":
                b = int(hyperparams.get("b", 20))
                nc = int(hyperparams.get("nc", 5))
                # population_size is mapped to B for BCO.
                optimizer = BeeColonyOptimization(self.jobs, self.nodes, population_size=b, iterations=iterations, nc=nc, ext_freq=ext_freq, ext_percent=ext_percent)
                assignments, makespan, cost, history = optimizer.optimize()
            else:
                raise ValueError("Unknown algorithm")

            # Store the real calculated values
            result_data["makespan"] = round(makespan, 2)
            result_data["cost"] = round(cost, 2)
            result_data["convergence_history"] = history
                
        except Exception as e:
            print(f"Error during optimization: {e}")
            return {"error": str(e)}

        print(f"Simulation finished successfully. Returning real results to UI.")
        return result_data


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