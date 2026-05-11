import re

with open("hybrid_gui.py", "r") as f:
    content = f.read()

content = content.replace("ui/stitch/code.html", "ui/stitch/hybrid.html")
content = content.replace("Cloud Optimizer CI Dashboard", "Cloud Optimizer CI Hybrid Dashboard")

old_run_sim = """    def run_simulation(self, pop_size, iterations, algorithm, seed, hyperparams):
        \"\"\"Runs the specified algorithm and returns real results.\"\"\"
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
            cost_weight = float(hyperparams.get("cost_weight", 0.5))
            
            if algorithm == "GA":
                pc = float(hyperparams.get("pc", 0.95))
                pm = float(hyperparams.get("pm", 0.02))
                optimizer = GeneticAlgorithmOptimizer(self.jobs, self.nodes, population_size=pop_size, generations=iterations, crossover_rate=pc, mutation_rate=pm, ext_freq=ext_freq, ext_percent=ext_percent, cost_weight=cost_weight)
                assignments, makespan, cost, history = optimizer.optimize()
            elif algorithm == "PSO":
                w = float(hyperparams.get("w", 0.7))
                c1 = float(hyperparams.get("c1", 1.5))
                c2 = float(hyperparams.get("c2", 1.5))
                optimizer = ParticleSwarmOptimizer(self.jobs, self.nodes, population_size=pop_size, iterations=iterations, inertia_weight=w, c1=c1, c2=c2, ext_freq=ext_freq, ext_percent=ext_percent, cost_weight=cost_weight)
                assignments, makespan, cost, history = optimizer.optimize()
            elif algorithm == "GWO":
                optimizer = GreyWolfOptimizer(self.jobs, self.nodes, population_size=pop_size, iterations=iterations, ext_freq=ext_freq, ext_percent=ext_percent, cost_weight=cost_weight)
                assignments, makespan, cost, history = optimizer.optimize()
            elif algorithm == "BCO":
                b = int(hyperparams.get("b", 20))
                nc = int(hyperparams.get("nc", 5))
                # population_size is mapped to B for BCO.
                optimizer = BeeColonyOptimization(self.jobs, self.nodes, population_size=b, iterations=iterations, nc=nc, ext_freq=ext_freq, ext_percent=ext_percent, cost_weight=cost_weight)
                assignments, makespan, cost, history = optimizer.optimize()
            elif algorithm == "WOA":
                b_val = float(hyperparams.get("woa_b", 1.0))
                optimizer = WhaleOptimizationOptimizer(self.jobs, self.nodes, population_size=pop_size, iterations=iterations, b=b_val, ext_freq=ext_freq, ext_percent=ext_percent, cost_weight=cost_weight)
                assignments, makespan, cost, history = optimizer.optimize()
            elif algorithm == "RR":
                assignments = round_robin_scheduler(self.jobs, self.nodes)
                engine = SimulationEngine(self.jobs, self.nodes)
                for node in self.nodes: node.assigned_jobs = assignments.get(node.node_id, [])
                makespan = engine.calculate_makespan()
                cost = engine.calculate_execution_cost()
                history = [((1.0 - cost_weight) * makespan) + (cost_weight * cost * 10)] * iterations
            elif algorithm == "SJF":
                assignments = shortest_job_first_scheduler(self.jobs, self.nodes)
                engine = SimulationEngine(self.jobs, self.nodes)
                for node in self.nodes: node.assigned_jobs = assignments.get(node.node_id, [])
                makespan = engine.calculate_makespan()
                cost = engine.calculate_execution_cost()
                history = [((1.0 - cost_weight) * makespan) + (cost_weight * cost * 10)] * iterations
            else:
                raise ValueError("Unknown algorithm")

            # Serialize assignments
            serialized_assignments = {}
            for node_id, job_list in assignments.items():
                serialized_assignments[node_id] = [{"id": j.job_id, "workload": j.workload_cu, "duration": j.duration} for j in job_list]

            # Store the real calculated values
            result_data["makespan"] = round(makespan, 2)
            result_data["cost"] = round(cost, 2)
            result_data["convergence_history"] = history
            result_data["assignments"] = serialized_assignments
                
        except Exception as e:
            print(f"Error during optimization: {e}")
            return {"error": str(e)}

        print(f"Simulation finished successfully. Returning real results to UI.")
        return result_data"""

new_run_sim = """    def run_simulation(self, payload):
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
                opt = GeneticAlgorithmOptimizer(self.jobs, self.nodes, population_size=pop_size, generations=iters, crossover_rate=pc, mutation_rate=pm, ext_freq=ext_freq, ext_percent=ext_percent, cost_weight=cost_weight)
                return opt.optimize(initial_pop)
            elif algo == "PSO":
                w = float(params.get("w", 0.7))
                c1 = float(params.get("c1", 1.5))
                c2 = float(params.get("c2", 1.5))
                opt = ParticleSwarmOptimizer(self.jobs, self.nodes, population_size=pop_size, iterations=iters, inertia_weight=w, c1=c1, c2=c2, ext_freq=ext_freq, ext_percent=ext_percent, cost_weight=cost_weight)
                return opt.optimize(initial_pop)
            elif algo == "GWO":
                opt = GreyWolfOptimizer(self.jobs, self.nodes, population_size=pop_size, iterations=iters, ext_freq=ext_freq, ext_percent=ext_percent, cost_weight=cost_weight)
                return opt.optimize(initial_pop)
            elif algo == "BCO":
                nc = int(params.get("nc", 5))
                opt = BeeColonyOptimization(self.jobs, self.nodes, population_size=pop_size, iterations=iters, nc=nc, ext_freq=ext_freq, ext_percent=ext_percent, cost_weight=cost_weight)
                return opt.optimize(initial_pop)
            elif algo == "WOA":
                b_val = float(params.get("woa_b", 1.0))
                opt = WhaleOptimizationOptimizer(self.jobs, self.nodes, population_size=pop_size, iterations=iters, b=b_val, ext_freq=ext_freq, ext_percent=ext_percent, cost_weight=cost_weight)
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
            if mode == "Single":
                assignments, ms, cost, hist, final_pop = run_algo(algo1, iter1, None, params1)
                algo_name = algo1
            else:
                _, _, _, hist1, pop1 = run_algo(algo1, iter1, None, params1)
                assignments, ms, cost, hist2, final_pop = run_algo(algo2, iter2, pop1, params2)
                hist = hist1 + hist2
                algo_name = f"{algo1} + {algo2}"

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
            return {"error": str(e)}"""

content = content.replace(old_run_sim, new_run_sim)

with open("hybrid_gui.py", "w") as f:
    f.write(content)
