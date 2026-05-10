import random
import math
from typing import List, Dict, Tuple
from .models import Job, Node
from .engine import SimulationEngine

class GeneticAlgorithmOptimizer:
    def __init__(self, jobs: List[Job], nodes: List[Node],
                 population_size: int = 20,
                 crossover_rate: float = 0.95,
                 mutation_rate: float = 0.02,
                 generations: int = 50,
                 ext_freq: int = 0,
                 ext_percent: float = 0.10,
                 cost_weight: float = 0.5):
        self.jobs = jobs
        self.nodes = nodes
        self.population_size = population_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.ext_freq = ext_freq
        self.ext_percent = ext_percent
        self.cost_weight = cost_weight
        self.num_jobs = len(jobs)
        self.num_nodes = len(nodes)

        self.job_id_to_index = {job.job_id: i for i, job in enumerate(jobs)}
        self.index_to_node_id = {i: node.node_id for i, node in enumerate(nodes)}

    def _initialize_population(self) -> List[List[int]]:
        population = []
        for _ in range(self.population_size):
            chromosome = [random.randint(0, self.num_nodes - 1) for _ in range(self.num_jobs)]
            population.append(chromosome)
        return population

    def _chromosome_to_assignments(self, chromosome: List[int]) -> Dict[str, List[Job]]:
        assignments: Dict[str, List[Job]] = {node.node_id: [] for node in self.nodes}
        for job_index, node_index in enumerate(chromosome):
            job = self.jobs[job_index]
            node_id = self.index_to_node_id[node_index]
            assignments[node_id].append(job)
        return assignments

    def _evaluate(self, chromosome: List[int]) -> Tuple[float, float, float]:
        temp_nodes = [Node(n.node_id, n.capacity_cu, n.price_per_hour) for n in self.nodes]
        assignments = self._chromosome_to_assignments(chromosome)
        
        for node in temp_nodes:
            node.assigned_jobs = assignments.get(node.node_id, [])
            node.current_utilization_cu = sum(job.workload_cu for job in node.assigned_jobs)

        engine = SimulationEngine(self.jobs, temp_nodes)
        makespan = engine.calculate_makespan()
        cost = engine.calculate_execution_cost()
        fitness = ((1.0 - self.cost_weight) * makespan) + (self.cost_weight * cost * 10) # Using a smaller weight for cost so it doesn't overpower makespan
        return fitness, makespan, cost

    def optimize(self) -> Tuple[Dict[str, List[Job]], float, float, List[float]]:
        population = self._initialize_population()
        best_chromosome = None
        best_fitness = float('inf')
        best_makespan = 0.0
        best_cost = 0.0
        history = []

        for generation in range(self.generations):
            evaluated = [self._evaluate(c) for c in population]
            fitnesses = [e[0] for e in evaluated]

            current_best_idx = fitnesses.index(min(fitnesses))
            current_best_fitness = fitnesses[current_best_idx]

            if current_best_fitness < best_fitness:
                best_fitness = current_best_fitness
                best_chromosome = population[current_best_idx]
                best_makespan = evaluated[current_best_idx][1]
                best_cost = evaluated[current_best_idx][2]

            history.append(best_fitness)

            # Diversity Extension Mechanism
            if self.ext_freq > 0 and (generation + 1) % self.ext_freq == 0:
                num_replace = int(self.population_size * self.ext_percent)
                if num_replace > 0:
                    sorted_indices = sorted(range(self.population_size), key=lambda i: fitnesses[i], reverse=True)
                    for idx in sorted_indices[:num_replace]:
                        population[idx] = [random.randint(0, self.num_nodes - 1) for _ in range(self.num_jobs)]

            new_population = []
            for _ in range(self.population_size // 2):
                parent1 = random.choice(population)
                parent2 = random.choice(population)
                
                # Crossover
                if random.random() < self.crossover_rate:
                    crossover_point = random.randint(1, len(parent1) - 1)
                    offspring1 = parent1[:crossover_point] + parent2[crossover_point:]
                    offspring2 = parent2[:crossover_point] + parent1[crossover_point:]
                else:
                    offspring1, offspring2 = list(parent1), list(parent2)
                
                # Mutation
                for off in [offspring1, offspring2]:
                    for i in range(len(off)):
                        if random.random() < self.mutation_rate:
                            off[i] = random.randint(0, self.num_nodes - 1)
                    new_population.append(off)

            population = new_population[:self.population_size]

        assignments = self._chromosome_to_assignments(best_chromosome)
        return assignments, best_makespan, best_cost, history

class GreyWolfOptimizer:
    def __init__(self, jobs: List[Job], nodes: List[Node],
                 population_size: int = 5,
                 iterations: int = 50,
                 ext_freq: int = 0,
                 ext_percent: float = 0.10,
                 cost_weight: float = 0.5):
        self.jobs = jobs
        self.nodes = nodes
        self.population_size = population_size
        self.iterations = iterations
        self.ext_freq = ext_freq
        self.ext_percent = ext_percent
        self.cost_weight = cost_weight
        self.num_jobs = len(jobs)
        self.num_nodes = len(nodes)
        self.index_to_node_id = {i: node.node_id for i, node in enumerate(nodes)}

    def _chromosome_to_assignments(self, positions: List[float]) -> Dict[str, List[Job]]:
        assignments: Dict[str, List[Job]] = {node.node_id: [] for node in self.nodes}
        for job_index, pos in enumerate(positions):
            node_index = int(round(pos))
            node_index = max(0, min(node_index, self.num_nodes - 1))
            job = self.jobs[job_index]
            node_id = self.index_to_node_id[node_index]
            assignments[node_id].append(job)
        return assignments

    def _evaluate(self, positions: List[float]) -> Tuple[float, float, float]:
        temp_nodes = [Node(n.node_id, n.capacity_cu, n.price_per_hour) for n in self.nodes]
        assignments = self._chromosome_to_assignments(positions)
        
        for node in temp_nodes:
            node.assigned_jobs = assignments.get(node.node_id, [])
        
        engine = SimulationEngine(self.jobs, temp_nodes)
        makespan = engine.calculate_makespan()
        cost = engine.calculate_execution_cost()
        fitness = ((1.0 - self.cost_weight) * makespan) + (self.cost_weight * cost * 10)
        return fitness, makespan, cost

    def optimize(self) -> Tuple[Dict[str, List[Job]], float, float, List[float]]:
        population = []
        for _ in range(self.population_size):
            pos = [random.uniform(0, self.num_nodes - 1) for _ in range(self.num_jobs)]
            population.append(pos)

        alpha_pos, alpha_score = None, float("inf")
        beta_pos, beta_score = None, float("inf")
        delta_pos, delta_score = None, float("inf")
        
        best_makespan, best_cost = 0.0, 0.0
        history = []

        for t in range(self.iterations):
            current_fitnesses = []
            for i in range(self.population_size):
                fitness, makespan, cost = self._evaluate(population[i])
                current_fitnesses.append(fitness)

                if fitness < alpha_score:
                    delta_score, delta_pos = beta_score, beta_pos
                    beta_score, beta_pos = alpha_score, alpha_pos
                    alpha_score, alpha_pos = fitness, population[i].copy()
                    best_makespan, best_cost = makespan, cost
                elif fitness < beta_score:
                    delta_score, delta_pos = beta_score, beta_pos
                    beta_score, beta_pos = fitness, population[i].copy()
                elif fitness < delta_score:
                    delta_score, delta_pos = fitness, population[i].copy()

            history.append(alpha_score)
            
            # Diversity Extension Mechanism
            if self.ext_freq > 0 and (t + 1) % self.ext_freq == 0:
                num_replace = int(self.population_size * self.ext_percent)
                if num_replace > 0:
                    sorted_indices = sorted(range(self.population_size), key=lambda i: current_fitnesses[i], reverse=True)
                    for idx in sorted_indices[:num_replace]:
                        population[idx] = [random.uniform(0, self.num_nodes - 1) for _ in range(self.num_jobs)]

            a = 2.0 - t * (2.0 / self.iterations)

            for i in range(self.population_size):
                for j in range(self.num_jobs):
                    def get_x(pos, score, current):
                        if pos is None: return current
                        r1, r2 = random.random(), random.random()
                        A = 2.0 * a * r1 - a
                        C = 2.0 * r2
                        D = abs(C * pos[j] - current)
                        return pos[j] - A * D

                    X1 = get_x(alpha_pos, alpha_score, population[i][j])
                    X2 = get_x(beta_pos, beta_score, population[i][j])
                    X3 = get_x(delta_pos, delta_score, population[i][j])

                    population[i][j] = (X1 + X2 + X3) / 3.0
                    population[i][j] = max(0.0, min(population[i][j], float(self.num_nodes - 1)))

        assignments = self._chromosome_to_assignments(alpha_pos)
        return assignments, best_makespan, best_cost, history

class ParticleSwarmOptimizer:
    def __init__(self, jobs: List[Job], nodes: List[Node],
                 population_size: int = 20,
                 iterations: int = 50,
                 inertia_weight: float = 0.7,
                 c1: float = 1.5,
                 c2: float = 1.5,
                 ext_freq: int = 0,
                 ext_percent: float = 0.10,
                 cost_weight: float = 0.5):
        self.jobs = jobs
        self.nodes = nodes
        self.population_size = population_size
        self.iterations = iterations
        self.inertia_weight = inertia_weight
        self.c1 = c1
        self.c2 = c2
        self.ext_freq = ext_freq
        self.ext_percent = ext_percent
        self.cost_weight = cost_weight
        self.num_jobs = len(jobs)
        self.num_nodes = len(nodes)
        self.index_to_node_id = {i: node.node_id for i, node in enumerate(nodes)}

    def _chromosome_to_assignments(self, positions: List[float]) -> Dict[str, List[Job]]:
        assignments: Dict[str, List[Job]] = {node.node_id: [] for node in self.nodes}
        for job_index, pos in enumerate(positions):
            node_index = int(round(pos))
            node_index = max(0, min(node_index, self.num_nodes - 1))
            job = self.jobs[job_index]
            node_id = self.index_to_node_id[node_index]
            assignments[node_id].append(job)
        return assignments

    def _evaluate(self, positions: List[float]) -> Tuple[float, float, float]:
        temp_nodes = [Node(n.node_id, n.capacity_cu, n.price_per_hour) for n in self.nodes]
        assignments = self._chromosome_to_assignments(positions)
        for node in temp_nodes: node.assigned_jobs = assignments.get(node.node_id, [])
        engine = SimulationEngine(self.jobs, temp_nodes)
        makespan = engine.calculate_makespan()
        cost = engine.calculate_execution_cost()
        fitness = ((1.0 - self.cost_weight) * makespan) + (self.cost_weight * cost * 10)
        return fitness, makespan, cost

    def optimize(self) -> Tuple[Dict[str, List[Job]], float, float, List[float]]:
        # Initialize particles
        particles = [[random.uniform(0, self.num_nodes - 1) for _ in range(self.num_jobs)] for _ in range(self.population_size)]
        velocities = [[random.uniform(-1, 1) for _ in range(self.num_jobs)] for _ in range(self.population_size)]
        pbest = particles.copy()
        pbest_scores = [float('inf')] * self.population_size
        
        gbest = None
        gbest_score = float('inf')
        gbest_makespan = 0.0
        gbest_cost = 0.0
        history = []

        for t in range(self.iterations):
            for i in range(self.population_size):
                fitness, makespan, cost = self._evaluate(particles[i])
                if fitness < pbest_scores[i]:
                    pbest_scores[i] = fitness
                    pbest[i] = particles[i].copy()
                
                if fitness < gbest_score:
                    gbest_score = fitness
                    gbest = particles[i].copy()
                    gbest_makespan = makespan
                    gbest_cost = cost
            
            history.append(gbest_score)
            
            # Diversity Extension Mechanism
            if self.ext_freq > 0 and (t + 1) % self.ext_freq == 0:
                num_replace = int(self.population_size * self.ext_percent)
                if num_replace > 0:
                    sorted_indices = sorted(range(self.population_size), key=lambda i: pbest_scores[i], reverse=True)
                    for idx in sorted_indices[:num_replace]:
                        particles[idx] = [random.uniform(0, self.num_nodes - 1) for _ in range(self.num_jobs)]
                        velocities[idx] = [random.uniform(-1, 1) for _ in range(self.num_jobs)]
                        pbest_scores[idx] = float('inf')

            for i in range(self.population_size):
                for j in range(self.num_jobs):
                    r1, r2 = random.random(), random.random()
                    vel = (self.inertia_weight * velocities[i][j] + 
                           self.c1 * r1 * (pbest[i][j] - particles[i][j]) + 
                           self.c2 * r2 * (gbest[j] - particles[i][j]))
                    velocities[i][j] = max(-self.num_nodes, min(vel, self.num_nodes)) # clamp velocity
                    
                    particles[i][j] += velocities[i][j]
                    particles[i][j] = max(0.0, min(particles[i][j], float(self.num_nodes - 1)))

        assignments = self._chromosome_to_assignments(gbest)
        return assignments, gbest_makespan, gbest_cost, history

class BeeColonyOptimization:
    def __init__(self, jobs: List[Job], nodes: List[Node],
                 population_size: int = 20,
                 iterations: int = 50,
                 nc: int = 5,
                 ext_freq: int = 0,
                 ext_percent: float = 0.10,
                 cost_weight: float = 0.5):
        self.jobs = jobs
        self.nodes = nodes
        self.population_size = population_size
        self.iterations = iterations
        self.nc = nc
        self.ext_freq = ext_freq
        self.ext_percent = ext_percent
        self.cost_weight = cost_weight
        self.num_jobs = len(jobs)
        self.num_nodes = len(nodes)
        self.index_to_node_id = {i: node.node_id for i, node in enumerate(nodes)}
        
    def _chromosome_to_assignments(self, positions: List[int]) -> Dict[str, List[Job]]:
        assignments: Dict[str, List[Job]] = {node.node_id: [] for node in self.nodes}
        for job_index, node_index in enumerate(positions):
            node_index = int(round(node_index))
            node_index = max(0, min(node_index, self.num_nodes - 1))
            job = self.jobs[job_index]
            node_id = self.index_to_node_id[node_index]
            assignments[node_id].append(job)
        return assignments

    def _evaluate(self, positions: List[int]) -> Tuple[float, float, float]:
        temp_nodes = [Node(n.node_id, n.capacity_cu, n.price_per_hour) for n in self.nodes]
        assignments = self._chromosome_to_assignments(positions)
        for node in temp_nodes: node.assigned_jobs = assignments.get(node.node_id, [])
        engine = SimulationEngine(self.jobs, temp_nodes)
        makespan = engine.calculate_makespan()
        cost = engine.calculate_execution_cost()
        fitness = ((1.0 - self.cost_weight) * makespan) + (self.cost_weight * cost * 10)
        return fitness, makespan, cost

    def _partial_evaluate(self, path: List[int]) -> float:
        padded = list(path) + [random.randint(0, self.num_nodes - 1) for _ in range(self.num_jobs - len(path))]
        return self._evaluate(padded)[0]

    def optimize(self) -> Tuple[Dict[str, List[Job]], float, float, List[float]]:
        bees = [[] for _ in range(self.population_size)]
        history = []
        
        t = 0
        while t < self.iterations:
            all_assigned = all(len(bee) == self.num_jobs for bee in bees)
            if all_assigned:
                break
                
            # Forward pass
            for i in range(self.population_size):
                bee = bees[i]
                k = 1
                while k <= self.nc and len(bee) < self.num_jobs:
                    fitnesses = []
                    for node_idx in range(self.num_nodes):
                        fit = self._partial_evaluate(bee + [node_idx])
                        fitnesses.append(fit)
                    
                    max_fit = max(fitnesses)
                    min_fit = min(fitnesses)
                    if max_fit == min_fit:
                        probs = [1.0/self.num_nodes] * self.num_nodes
                    else:
                        inv_fit = [max_fit - f + 1e-6 for f in fitnesses]
                        tot = sum(inv_fit)
                        probs = [f/tot for f in inv_fit]
                        
                    r = random.random()
                    cum = 0.0
                    chosen = self.num_nodes - 1
                    for idx, p in enumerate(probs):
                        cum += p
                        if r <= cum:
                            chosen = idx
                            break
                    bee.append(chosen)
                    k += 1
                    
            # Backward pass
            bee_fitnesses = []
            for bee in bees:
                bee_fitnesses.append(self._partial_evaluate(bee))
                
            sorted_indices = sorted(range(self.population_size), key=lambda i: bee_fitnesses[i])
            
            # Recruiter / follower decision
            max_f = max(bee_fitnesses)
            min_f = min(bee_fitnesses)
            if max_f == min_f:
                norm_fit = [1.0] * self.population_size
            else:
                norm_fit = [(max_f - bee_fitnesses[i]) / (max_f - min_f) for i in range(self.population_size)]
            
            recruiters = []
            followers = []    
            for i in range(self.population_size):
                if random.random() < norm_fit[i]:
                    recruiters.append((bees[i], norm_fit[i]))
                else:
                    followers.append(i)
                    
            if not recruiters:
                recruiters.append((bees[sorted_indices[0]], norm_fit[sorted_indices[0]]))
                
            rp = [r[1] for r in recruiters]
            s_rp = sum(rp)
            if s_rp == 0:
                rp = [1.0/len(recruiters)] * len(recruiters)
            else:
                rp = [p/s_rp for p in rp]
                
            for idx in followers:
                r = random.random()
                cum = 0.0
                chosen_r = recruiters[-1][0]
                for r_idx, p in enumerate(rp):
                    cum += p
                    if r <= cum:
                        chosen_r = recruiters[r_idx][0]
                        break
                bees[idx] = list(chosen_r)
                
            best_fit_current = bee_fitnesses[sorted_indices[0]]
            history.append(best_fit_current)
            
            t += 1
            
        best_fitness = float('inf')
        best_chromosome = None
        best_makespan = 0.0
        best_cost = 0.0
        
        for bee in bees:
            if len(bee) < self.num_jobs:
                bee = bee + [random.randint(0, self.num_nodes - 1) for _ in range(self.num_jobs - len(bee))]
            fit, ms, cst = self._evaluate(bee)
            if fit < best_fitness:
                best_fitness = fit
                best_chromosome = bee
                best_makespan = ms
                best_cost = cst
                
        return self._chromosome_to_assignments(best_chromosome), best_makespan, best_cost, history

import numpy as np

class WhaleOptimizationOptimizer:
    def __init__(self, jobs: List[Job], nodes: List[Node],
                 population_size: int = 20,
                 iterations: int = 50,
                 b: float = 1.0,
                 a_step: float = None,
                 ext_freq: int = 0,
                 ext_percent: float = 0.10,
                 cost_weight: float = 0.5):
        self.jobs = jobs
        self.nodes = nodes
        self.population_size = population_size
        self.iterations = iterations
        self.b = b
        self.a_step = a_step if a_step is not None else (2.0 / iterations)
        self.a = 2.0
        self.ext_freq = ext_freq
        self.ext_percent = ext_percent
        self.cost_weight = cost_weight
        self.num_jobs = len(jobs)
        self.num_nodes = len(nodes)
        self.index_to_node_id = {i: node.node_id for i, node in enumerate(nodes)}

    def _chromosome_to_assignments(self, positions: np.ndarray) -> Dict[str, List[Job]]:
        assignments: Dict[str, List[Job]] = {node.node_id: [] for node in self.nodes}
        for job_index, pos in enumerate(positions):
            node_index = int(round(pos))
            node_index = max(0, min(node_index, self.num_nodes - 1))
            job = self.jobs[job_index]
            node_id = self.index_to_node_id[node_index]
            assignments[node_id].append(job)
        return assignments

    def _evaluate(self, positions: np.ndarray) -> Tuple[float, float, float]:
        temp_nodes = [Node(n.node_id, n.capacity_cu, n.price_per_hour) for n in self.nodes]
        assignments = self._chromosome_to_assignments(positions)
        for node in temp_nodes: node.assigned_jobs = assignments.get(node.node_id, [])
        engine = SimulationEngine(self.jobs, temp_nodes)
        makespan = engine.calculate_makespan()
        cost = engine.calculate_execution_cost()
        fitness = ((1.0 - self.cost_weight) * makespan) + (self.cost_weight * cost * 10)
        return fitness, makespan, cost

    def optimize(self) -> Tuple[Dict[str, List[Job]], float, float, List[float]]:
        # Initialize solutions uniformly randomly in space [0, num_nodes - 1]
        sols = np.random.uniform(0.0, float(self.num_nodes - 1), size=(self.population_size, self.num_jobs))
        
        best_fitness = float('inf')
        best_sol = None
        best_makespan = 0.0
        best_cost = 0.0
        history = []

        for t in range(self.iterations):
            current_fitnesses = []
            for i in range(self.population_size):
                fit, ms, cst = self._evaluate(sols[i])
                current_fitnesses.append(fit)
                if fit < best_fitness:
                    best_fitness = fit
                    best_sol = sols[i].copy()
                    best_makespan = ms
                    best_cost = cst
            
            history.append(best_fitness)
            
            # Diversity Extension Mechanism
            if self.ext_freq > 0 and (t + 1) % self.ext_freq == 0:
                num_replace = int(self.population_size * self.ext_percent)
                if num_replace > 0:
                    sorted_indices = np.argsort(current_fitnesses)[::-1] # descending
                    for idx in sorted_indices[:num_replace]:
                        sols[idx] = np.random.uniform(0.0, float(self.num_nodes - 1), size=self.num_jobs)

            new_sols = []
            for i in range(self.population_size):
                s = sols[i]
                if np.random.uniform(0.0, 1.0) > 0.5:
                    r = np.random.uniform(0.0, 1.0, size=self.num_jobs)
                    A = (2.0 * np.multiply(self.a, r)) - self.a
                    norm_A = np.linalg.norm(A)
                    if norm_A < 1.0:
                        C = 2.0 * np.random.uniform(0.0, 1.0, size=self.num_jobs)
                        D = np.linalg.norm(np.multiply(C, best_sol) - s)
                        new_s = best_sol - np.multiply(A, D)
                    else:
                        random_sol = sols[np.random.randint(self.population_size)]
                        C = 2.0 * np.random.uniform(0.0, 1.0, size=self.num_jobs)
                        D = np.linalg.norm(np.multiply(C, random_sol) - s)
                        new_s = random_sol - np.multiply(A, D)
                else:
                    D = np.linalg.norm(best_sol - s)
                    L = np.random.uniform(-1.0, 1.0, size=self.num_jobs)
                    new_s = np.multiply(np.multiply(D, np.exp(self.b * L)), np.cos(2.0 * np.pi * L)) + best_sol
                
                # Constrain solution
                new_s = np.clip(new_s, 0.0, float(self.num_nodes - 1))
                new_sols.append(new_s)

            sols = np.stack(new_sols)
            self.a -= self.a_step

        assignments = self._chromosome_to_assignments(best_sol)
        return assignments, best_makespan, best_cost, history
