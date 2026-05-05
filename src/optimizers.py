import random
from typing import List, Dict, Tuple
from .models import Job, Node
from .engine import SimulationEngine # Assuming SimulationEngine can be used for fitness evaluation

class GeneticAlgorithmOptimizer:
    def __init__(self, jobs: List[Job], nodes: List[Node],
                 population_size: int = 20,
                 crossover_rate: float = 0.95,
                 mutation_rate: float = 0.02,
                 generations: int = 50):
        self.jobs = jobs
        self.nodes = nodes
        self.population_size = population_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.generations = generations

        # Map job IDs to their index for easier chromosome representation
        self.job_id_to_index = {job.job_id: i for i, job in enumerate(jobs)}
        self.node_id_to_index = {node.node_id: i for i, node in enumerate(nodes)}
        self.index_to_node_id = {i: node.node_id for i, node in enumerate(nodes)}


    def _initialize_population(self) -> List[List[int]]:
        """
        Initializes a population of random job-to-node assignments (chromosomes).
        Each chromosome is a list where index is job index and value is node index.
        """
        population = []
        num_nodes = len(self.nodes)
        num_jobs = len(self.jobs)
        for _ in range(self.population_size):
            chromosome = [random.randint(0, num_nodes - 1) for _ in range(num_jobs)]
            population.append(chromosome)
        return population

    def _chromosome_to_assignments(self, chromosome: List[int]) -> Dict[str, List[Job]]:
        """
        Converts a chromosome (job-to-node index mapping) into a job assignment dictionary.
        """
        assignments: Dict[str, List[Job]] = {node.node_id: [] for node in self.nodes}
        for job_index, node_index in enumerate(chromosome):
            job = self.jobs[job_index]
            node_id = self.index_to_node_id[node_index]
            assignments[node_id].append(job)
        return assignments

    def _calculate_fitness(self, chromosome: List[int]) -> float:
        """
        Calculates the fitness of a single chromosome.
        Lower fitness value is better (minimization problem).
        Fitness = Makespan + (Cost * 100)
        """
        # Create a temporary list of nodes for simulation to avoid modifying original nodes
        temp_nodes = [Node(n.node_id, n.capacity_cu) for n in self.nodes]
        
        # Apply the assignments from the chromosome to the temporary nodes
        assignments = self._chromosome_to_assignments(chromosome)
        for node in temp_nodes:
            node.assigned_jobs = assignments.get(node.node_id, [])
            # For utilization calculation, we need to sum workloads of assigned jobs
            node.current_utilization_cu = sum(job.workload_cu for job in node.assigned_jobs)

        engine = SimulationEngine(self.jobs, temp_nodes)
        makespan = engine.calculate_makespan()
        cost = engine.calculate_execution_cost()

        fitness = makespan + (cost * 100)
        return fitness

    def _select_parents(self, population: List[List[int]], fitnesses: List[float]) -> Tuple[List[int], List[int]]:
        """
        Selects two parents using tournament selection.
        """
        # Assuming lower fitness is better, so select individuals with lower fitness
        # For simplicity, using a basic roulette wheel selection where better fitness has higher chance
        # Invert fitness for selection probability if minimizing: higher (better) fitness = lower value
        # Or, just use a simple tournament selection (pick N random, choose best)
        
        # For now, let's just pick two random parents.
        # This needs to be improved with proper selection (e.g., tournament, roulette wheel)
        parent1 = random.choice(population)
        parent2 = random.choice(population)
        return parent1, parent2

    def _crossover(self, parent1: List[int], parent2: List[int]) -> Tuple[List[int], List[int]]:
        """
        Performs single-point crossover between two parents.
        """
        if random.random() < self.crossover_rate:
            # Perform single-point crossover
            crossover_point = random.randint(1, len(parent1) - 1)
            offspring1 = parent1[:crossover_point] + parent2[crossover_point:]
            offspring2 = parent2[:crossover_point] + parent1[crossover_point:]
            return offspring1, offspring2
        else:
            return parent1, parent2 # No crossover, return parents as offspring

    def _mutate(self, chromosome: List[int]) -> List[int]:
        """
        Mutates a chromosome by randomly changing a job's assigned node.
        """
        num_nodes = len(self.nodes)
        mutated_chromosome = list(chromosome) # Create a mutable copy
        for i in range(len(mutated_chromosome)):
            if random.random() < self.mutation_rate:
                mutated_chromosome[i] = random.randint(0, num_nodes - 1)
        return mutated_chromosome

    def optimize(self) -> Dict[str, List[Job]]:
        """
        Runs the Genetic Algorithm to find an optimal job-to-node assignment.
        Returns the best assignment found.
        """
        population = self._initialize_population()
        best_chromosome = None
        best_fitness = float('inf')

        for generation in range(self.generations):
            fitnesses = [self._calculate_fitness(c) for c in population]

            # Find the best individual in current population
            current_best_fitness = min(fitnesses)
            current_best_chromosome = population[fitnesses.index(current_best_fitness)]

            if current_best_fitness < best_fitness:
                best_fitness = current_best_fitness
                best_chromosome = current_best_chromosome

            new_population = []
            for _ in range(self.population_size // 2): # Create new population through selection, crossover, mutation
                parent1, parent2 = self._select_parents(population, fitnesses)
                offspring1, offspring2 = self._crossover(parent1, parent2)
                
                new_population.append(self._mutate(offspring1))
                new_population.append(self._mutate(offspring2))

            population = new_population[:self.population_size] # Ensure population size is maintained

            print(f"Generation {generation+1}: Best Fitness = {best_fitness:.2f}")

        if best_chromosome is None:
            raise Exception("Genetic Algorithm failed to find a solution.")

        return self._chromosome_to_assignments(best_chromosome)
