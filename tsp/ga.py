import random

MUTATION_TYPES = ['flip', 'interchange']
CROSSOVER_TYPES = ['one_point', 'two_point']
SELECTION_METHODS = ['roulette_wheel', 'rank_selection']


def u(s=0, e=1):
    return random.uniform(s, e)


class GeneticAlgorithm:
    def __init__(self, population_size=10, mutation_rate=0.01,
                 crossover_rate=0.3, mutation_type='flip',
                 crossover_type='one_point', chromosome_size=100,
                 selection_method='roulette_wheel'):

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
            number_of_mutations = max(1, self.chromosome_size//100)  # Mutate 0.1 % of genes
            mutation_points = [random.randrange(self.chromosome_size) for _ in range(number_of_mutations)]
            new_c = list(c)
            for i in mutation_points:
                new_c[i] = int(not c[i])
            return new_c

    def crossover(self, c1, c2):
        if self.crossover_type == 'one_point':
            crossover_point = random.randrange(1, self.chromosome_size)
            child1 = c1[:crossover_point] + c2[crossover_point:]
            child2 = c2[:crossover_point] + c1[crossover_point:]
            return child1, child2
        # TODO: implement other
        else:
            return c1, c2

    def do_roulette_selection(self, fitness):
        parents = []
        total_fitness = sum(fitness)
        for x in range(self.population_size):
            p = 0
            s = u(0, total_fitness)
            for i, f in enumerate(fitness):
                p += f
                if p >= s:
                    parents.append(self.population[i])
                    break
        return parents

    def next_generation(self, fitness):
        if self.selection_method == 'roulette_wheel':
            parents = self.do_roulette_selection(fitness)
        else:
            raise Exception("invalid selection method")
        # Now we have population ready to crossover
        next_gen = []
        indices_set = set(range(self.population_size))
        for x in range(self.population_size//2):  # Assumes even population size
            p1_ind = random.choice(list(indices_set))
            indices_set.remove(p1_ind)
            p2_ind = random.choice(list(indices_set))
            indices_set.remove(p2_ind)

            should_crossover = u() < self.crossover_rate
            if should_crossover:
                next_gen.extend(self.crossover(parents[p1_ind], parents[p2_ind]))
            else:
                next_gen.extend((parents[p1_ind], parents[p2_ind]))

        mutated = [self.mutate(x) if u() < self.mutation_rate else x for x in next_gen]
        return mutated
