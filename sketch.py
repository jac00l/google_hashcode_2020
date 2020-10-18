evalutate_solution(solution) -> (int; value of a given solution)
    return solution_score

get_random_solution(libraries_number, days_number, libraries) -> (tuple of type solution; particular and complete solution)
    return random_solution

get_initial_population(population_size, libraries_number, days_number, libraries) -> (tuple of type population; initial population)
    for _ in range(population_size):
        get_random_solution()
    return initial_population

get_children(days_number, soultion_a, solution_b) -> (lits of two solutions of type solution; offspring from two original solutions)
    return [children_a, children_b]

get_offspring(days_number, population) -> (list of type population; offspring, size equals population_size - each pair generates two, new solutions)
    for _ in range(population_size):
        get_children()
    return offspring

mutate(solution) -> (tuple of type solution; new solution obtained by mutating old solution)
    return mutated_solution

do_mutations(population) -> (list of mutated solutions; mutated solutions, size equals population_size - each solution generates new one)
    for _ in range(population_size):
        mutate()
    return [mutated_solutions]

# main
read_data()

start_time = current_time()
epochs_duration = []

population_size = value
population = get_initial_population(population_size)

while (start_time + {5 minutes}) >= (current_time + epochs_duration[-1] * 2):
    offspring = get_offspring(days_number, population)
    mutations = do_mutations(population)
    population += offspring
    population += mutations
    population.sort()
    population[:population_size]
    epochs_duration += current_time()

return population[0]
