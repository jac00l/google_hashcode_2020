from time import time
import random
import statistics

epochs_duration = []
epochs_duration.append(time())

def library_heuristic(library, books_scores):
    if len(library[1]) == 1:
        return library[1][0]
    books = library[1]
    scores = [books_scores[x] for x in books]
    total_score = sum(scores)
    variance = statistics.variance(scores)
    return total_score / (max(0.01, variance) * library[0][1]) ** 1/2

def evaluate_solution(solution, books_scores):
    books_scanned = set()
    points = 0
    number_of_libraries = solution[0]
    for i in range(1, number_of_libraries+1):
        number_of_books = solution[i][1]
        for j in range(number_of_books):
            book_to_add = solution[i][2][j]
            if book_to_add not in books_scanned:
                books_scanned.add(book_to_add)
    solution_score = 0
    for i in books_scanned:
        solution_score += books_scores[i]
        
    return solution_score

def get_complete_solution(solution_indices, libraries, days_number, books_scores):
    time_pointer = days_number
    used_books = set()
    complete_solution = [len(solution_indices)]
    for i in solution_indices:
        time_pointer -= libraries[i][0][1]
        books_per_day = libraries[i][0][2]
        available_books = list(libraries[i][1])
        particular_solution = [i, 0, []]
        for x in available_books:
            if len(particular_solution[2]) >= time_pointer * books_per_day:
                break
            if x not in used_books:
                particular_solution[2].append(x)
                particular_solution[1] += 1
                used_books.add(x)
        particular_solution[2] = tuple(particular_solution[2])
        complete_solution.append(tuple(particular_solution))
    return tuple(complete_solution)

def get_random_solution(libraries_number, days_number, libraries, libraries_heuristics, books_scores):
    libraries_to_use = list(range(libraries_number))
    libraries_to_use_heuristics = list(libraries_heuristics)
    solution_indices = []
    time_pointer = 0
    while True:
        if not len(libraries_to_use):
            return get_complete_solution(solution_indices, libraries, days_number, books_scores)
        random_index = random.choices(list(range(0, len(libraries_to_use))), weights = libraries_to_use_heuristics, k = 1)[0]
        del libraries_to_use[random_index]
        del libraries_to_use_heuristics[random_index]
        if time_pointer + libraries[random_index][0][1] > days_number:
            break                                 
        solution_indices.append(random_index)
        time_pointer += libraries[random_index][0][1]
    return get_complete_solution(solution_indices, libraries, days_number, books_scores)

def get_initial_population(population_size, libraries_number, days_number, libraries, libraries_heuristics, books, timestamp, max_duration):
    population = []
    for i in range(population_size):
        population.append(get_random_solution(libraries_number, days_number, libraries, libraries_heuristics, books))
        if i % 2 and time() - timestamp >= max_duration / 2:
            return (i, population)
    return (population_size, population)

def get_greedy_solution(libraries_number, days_number, libraries, libraries_heuristics, books_scores):
    libraries_to_use = list(range(libraries_number))
    libraries_to_use.sort(key = lambda x: library_heuristic(libraries[x], books_scores), reverse = True)
    solution_indices = []
    time_pointer = 0
    for i in range(libraries_number):
        if time_pointer + libraries[libraries_to_use[i]][0][1] >= days_number:
            break
        solution_indices.append(libraries_to_use[i])
        time_pointer += libraries[libraries_to_use[i]][0][1]
    return get_complete_solution(solution_indices, libraries, days_number, books_scores)

def mutate(solution, libraries, days_number, books_scores):
    solution_indices = [solution[i][0] for i in range(1, len(solution))]
    for _ in range(3):
        nucleotide_a = random.randint(0, len(solution_indices) - 1)
        nucleotide_b = random.randint(0, len(solution_indices) - 1)
        solution_indices[nucleotide_a], solution_indices[nucleotide_b] = solution_indices[nucleotide_b], solution_indices[nucleotide_a]
    return get_complete_solution(solution_indices, libraries, days_number, books_scores)

def do_mutations(population, libraries, days_number, books_scores):
    mutated_solutions = []
    for solution in population:
        mutated_solutions.append(mutate(solution, libraries, days_number, books_scores))
    return mutated_solutions

def get_children(parent_a, parent_b, libraries, days_number, books_scores):
    parent_a_indices = [parent_a[i][0] for i in range(1, len(parent_a))]
    parent_b_indices = [parent_b[i][0] for i in range(1, len(parent_b))]
    split_point = random.randint(0, min(len(parent_a_indices), len(parent_b_indices)) - 1)
    child_a_indices = parent_a_indices[:split_point] + [x for x in parent_b_indices[split_point:] if x not in parent_a_indices[:split_point]]
    child_b_indices = parent_b_indices[:split_point] + [x for x in parent_a_indices[split_point:] if x not in parent_b_indices[:split_point]]
    for parent in (parent_a_indices, parent_b_indices):
        time_pointer = 0
        for i in range(len(parent)):
            if time_pointer >= days_number:
                parent_a_indices = parent[:i]
                break
            time_pointer += libraries[parent[i]][1]
        time_pointer = 0
    child_a = get_complete_solution(child_a_indices, libraries, days_number, books_scores)
    child_b = get_complete_solution(child_b_indices, libraries, days_number, books_scores)
    return (child_a, child_b)

def get_offspring(population, libraries, days_number, books_scores):
    offspring = []
    mating_pool = [evaluate_solution(population[i], books_scores) for i in range(len(population))] 
    for _ in range(len(population), 2):
        offspring.append(get_children(random.choices(population, weights = mating_pool, k = 2)), libraries, days_number, books_scores)
    return tuple(offspring)

max_duration = 300
population_size = 80

books_number, libraries_number, days_number = [int(x) for x in input().split()]
books_scores = tuple([int(x) for x in input().split()])
libraries = [None] * libraries_number
for i in range(libraries_number):
    libraries[i] = tuple([int(x) for x in input().split()]), tuple(sorted([int(x) for x in input().split()], key = lambda x: books_scores[x], reverse = True))
libraries = tuple(libraries)
libraries_heuristics = tuple([library_heuristic(library, books_scores) for library in libraries])

population_size, population = get_initial_population(population_size - 1, libraries_number, days_number, libraries, libraries_heuristics, books_scores, epochs_duration[0], max_duration)

population_size += 1
population.append(get_greedy_solution(libraries_number, days_number, libraries, libraries_heuristics, books_scores))

epochs_duration.append(time())
while epochs_duration[0] + max_duration - 5 >= time() + (epochs_duration[-1] - epochs_duration[-2]) * 2:
    mutations = do_mutations(population, libraries, days_number, books_scores)
    offspring = get_offspring(population, days_number, libraries, books_scores)
    population.extend(mutations)
    population.extend(offspring)
    population.sort(key = lambda x: evaluate_solution(x, books_scores), reverse = True)
    population = population[:population_size]
    epochs_duration.append(time())

print(population[0][0])
for i in range(1, len(population[0])):
    print(population[0][i][0], population[0][i][1], end = " ")
    print(" ".join([str(x) for x in population[0][i][2]]))