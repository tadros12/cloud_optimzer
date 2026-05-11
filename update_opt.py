import sys

with open("src/optimizers.py", "r") as f:
    content = f.read()

content = content.replace("from typing import List, Dict, Tuple", "from typing import List, Dict, Tuple, Any")

content = content.replace(
    "def optimize(self) -> Tuple[Dict[str, List[Job]], float, float, List[float]]:\n        population = self._initialize_population()",
    "def optimize(self, initial_population=None) -> Tuple[Dict[str, List[Job]], float, float, List[float], List[List[Any]]]:\n        if initial_population is not None:\n            population = [[int(round(x)) for x in p] for p in initial_population]\n        else:\n            population = self._initialize_population()"
)

content = content.replace(
    "def optimize(self) -> Tuple[Dict[str, List[Job]], float, float, List[float]]:\n        population = []\n        for _ in range(self.population_size):\n            pos = [random.uniform(0, self.num_nodes - 1) for _ in range(self.num_jobs)]\n            population.append(pos)",
    "def optimize(self, initial_population=None) -> Tuple[Dict[str, List[Job]], float, float, List[float], List[List[Any]]]:\n        if initial_population is not None:\n            population = [[float(x) for x in p] for p in initial_population]\n        else:\n            population = []\n            for _ in range(self.population_size):\n                pos = [random.uniform(0, self.num_nodes - 1) for _ in range(self.num_jobs)]\n                population.append(pos)"
)

content = content.replace(
    "def optimize(self) -> Tuple[Dict[str, List[Job]], float, float, List[float]]:\n        # Initialize particles\n        particles = [[random.uniform(0, self.num_nodes - 1) for _ in range(self.num_jobs)] for _ in range(self.population_size)]",
    "def optimize(self, initial_population=None) -> Tuple[Dict[str, List[Job]], float, float, List[float], List[List[Any]]]:\n        if initial_population is not None:\n            particles = [[float(x) for x in p] for p in initial_population]\n        else:\n            particles = [[random.uniform(0, self.num_nodes - 1) for _ in range(self.num_jobs)] for _ in range(self.population_size)]"
)

content = content.replace(
    "def optimize(self) -> Tuple[Dict[str, List[Job]], float, float, List[float]]:\n        bees = [[] for _ in range(self.population_size)]",
    "def optimize(self, initial_population=None) -> Tuple[Dict[str, List[Job]], float, float, List[float], List[List[Any]]]:\n        if initial_population is not None:\n            bees = [[int(round(x)) for x in p] for p in initial_population]\n        else:\n            bees = [[] for _ in range(self.population_size)]"
)

content = content.replace(
    "def optimize(self) -> Tuple[Dict[str, List[Job]], float, float, List[float]]:\n        # Initialize solutions uniformly randomly in space [0, num_nodes - 1]\n        sols = np.random.uniform(0.0, float(self.num_nodes - 1), size=(self.population_size, self.num_jobs))",
    "def optimize(self, initial_population=None) -> Tuple[Dict[str, List[Job]], float, float, List[float], List[List[Any]]]:\n        if initial_population is not None:\n            sols = np.array(initial_population, dtype=float)\n        else:\n            sols = np.random.uniform(0.0, float(self.num_nodes - 1), size=(self.population_size, self.num_jobs))"
)

content = content.replace(
    "        assignments = self._chromosome_to_assignments(best_chromosome)\n        return assignments, best_makespan, best_cost, history",
    "        assignments = self._chromosome_to_assignments(best_chromosome)\n        return assignments, best_makespan, best_cost, history, population"
)

content = content.replace(
    "        assignments = self._chromosome_to_assignments(alpha_pos)\n        return assignments, best_makespan, best_cost, history",
    "        assignments = self._chromosome_to_assignments(alpha_pos)\n        return assignments, best_makespan, best_cost, history, population"
)

content = content.replace(
    "        assignments = self._chromosome_to_assignments(gbest)\n        return assignments, gbest_makespan, gbest_cost, history",
    "        assignments = self._chromosome_to_assignments(gbest)\n        return assignments, gbest_makespan, gbest_cost, history, particles"
)

content = content.replace(
    "        assignments = self._chromosome_to_assignments(best_sol)\n        return assignments, best_makespan, best_cost, history",
    "        assignments = self._chromosome_to_assignments(best_sol)\n        return assignments, best_makespan, best_cost, history, sols.tolist()"
)

bco_end_old = """        for bee in bees:
            if len(bee) < self.num_jobs:
                bee = bee + [random.randint(0, self.num_nodes - 1) for _ in range(self.num_jobs - len(bee))]
            fit, ms, cst = self._evaluate(bee)
            if fit < best_fitness:
                best_fitness = fit
                best_chromosome = bee
                best_makespan = ms
                best_cost = cst
                
        return self._chromosome_to_assignments(best_chromosome), best_makespan, best_cost, history"""

bco_end_new = """        final_pop = []
        for bee in bees:
            if len(bee) < self.num_jobs:
                b = bee + [random.randint(0, self.num_nodes - 1) for _ in range(self.num_jobs - len(bee))]
            else:
                b = bee.copy()
            final_pop.append(b)
            fit, ms, cst = self._evaluate(b)
            if fit < best_fitness:
                best_fitness = fit
                best_chromosome = b
                best_makespan = ms
                best_cost = cst
                
        return self._chromosome_to_assignments(best_chromosome), best_makespan, best_cost, history, final_pop"""

content = content.replace(bco_end_old, bco_end_new)

# Drop missing assignments correctly in BCO (Hybrid local refinement)
bco_while = "while t < self.iterations:\n            all_assigned = all(len(bee) == self.num_jobs for bee in bees)\n            if all_assigned:\n                break"
bco_while_new = "while t < self.iterations:\n            all_assigned = all(len(bee) == self.num_jobs for bee in bees)\n            if all_assigned:\n                for bee in bees:\n                    drop_count = min(self.nc, max(1, self.num_jobs // 3))\n                    for _ in range(drop_count):\n                        if bee: bee.pop(random.randrange(len(bee)))"
content = content.replace(bco_while, bco_while_new)

with open("src/optimizers.py", "w") as f:
    f.write(content)

