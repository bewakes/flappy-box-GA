import math
import random

MUTATION_TYPES = ['flip', 'interchange']
CROSSOVER_TYPES = ['uniform', 'one_point', 'two_point']
SELECTION_METHODS = ['elitism', 'roulette_wheel', 'rank_selection']


def u(s=0, e=1):
    return random.uniform(s, e)


class GeneticAlgorithm:
    def __init__(self, population_size=10, mutation_rate=0.01,
                 crossover_rate=0.3, mutation_type='flip',
                 crossover_type='uniform', chromosome_size=100,
                 selection_method='elitism'):

        self.population_size = population_size
        self.chromosome_size = chromosome_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        # TODO: Validate types
        self.crossover_type = crossover_type
        self.mutation_type = mutation_type
        self.selection_method = selection_method

        self.population = [
            [random.choice([0, 1]) for _ in range(self.chromosome_size)]
            for _ in range(population_size)
        ]

    def mutate(self, c):
        if self.mutation_type == 'flip':
            number_of_mutations = max(1, self.chromosome_size//1000)  # Mutate 0.1 % of genes
            mutation_points = [random.randrange(self.chromosome_size) for _ in range(number_of_mutations)]
            new_c = list(c)
            for i in mutation_points:
                new_c[i] = int(not c[i])
            return new_c

    def crossover(self, c1, c2):
        if self.crossover_type == 'one_point':
            crossover_point = random.randrange(1, self.chromosome_size)
            return c1[:crossover_point] + c2[crossover_point:]
        elif self.crossover_type == 'uniform':
            p1_prob = (1 - self.mutation_rate) / 2
            p2_prob = 1 - self.mutation_rate
            child = []
            for i in range(self.chromosome_size):
                r = u()
                if r <= p1_prob:
                    child.append(c1[i])
                elif r <= p2_prob:
                    child.append(c2[i])
                else:
                    child.append(random.choice([0, 1]))
            return child
        # TODO: implement other
        else:
            return c1, c2

    def do_roulette_selection(self, fitness):
        """
        @fitness: [population 0 fitness, population 1 fitness, ... population N fitness]
        """
        parents = []
        total_fitness = sum(fitness)

        for _ in range(self.population_size):
            p = 0
            s = u(0, total_fitness)
            for i, f in enumerate(fitness):
                p += f
                if p >= s:
                    parents.append(self.population[i])
                    break
        # Now we have population ready to crossover
        next_gen = []
        indices = list(range(self.population_size))
        random.shuffle(indices)
        for x in range(0, self.population_size, 2):  # Assumes even population size
            should_crossover = u() < self.crossover_rate
            if should_crossover:
                next_gen.extend(self.crossover(parents[x], parents[x+1]))
            else:
                next_gen.extend((parents[x], parents[x+1]))

        return [self.mutate(x) if u() < self.mutation_rate else x for x in next_gen]

    def do_elitism(self, fitness):
        sorted_population = sorted(
            zip(fitness, self.population),
            key=lambda x: x[0],
            reverse=True
        )
        # Select 10% of the best
        decile = math.ceil(0.1 * self.population_size)
        half_decile = decile // 2
        best = [x[1] for x in sorted_population[:decile]]
        next_gen = list(best)

        for _ in range(self.population_size - len(best)):
            parent1 = random.choice(best[:half_decile])
            parent2 = random.choice(best[half_decile:])
            child = self.crossover(parent1, parent2)
            next_gen.append(child)
        return next_gen

    def next_generation(self, fitness):
        """
        @fitness: [population 0 fitness, population 1 fitness, ... population N fitness]
        """
        if self.selection_method == 'elitism':
            self.population = self.do_elitism(fitness)
        elif self.selection_method == 'roulette_wheel':
            self.population = self.do_roulette_selection(fitness)
        else:
            raise Exception("invalid selection method")
        return self.population
