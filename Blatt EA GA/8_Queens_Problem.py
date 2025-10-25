import numpy as np

i1 = [0b0001, 0b0010, 0b0011, 0b0100, 0b0101, 0b0110, 0b0111, 0b1000]
i2 = [0b0100, 0b0010, 0b1000, 0b0011, 0b0101, 0b0001, 0b0110, 0b0111]
i3 = [0b0001, 0b0101, 0b1000, 0b0010, 0b0100, 0b0110, 0b0111, 0b0011]

population = []
mating_pool = []
score_list = []

def add_individual(i):
    population.append(i)

def calc_fitness():
    global population
    global score_list
    score_list = []
    for individual in population:
        score = 0
        for i in range(len(individual)):
            for f in range(i+1, len(individual)):
                if check_conflict(i+1, individual[i], f+1, individual[f]):
                    score += 1
        score_list.append(score)

def select_individual():
    global mating_pool
    global score_list
    mating_pool = []
    score_max = sum(score_list)

    counter = 0
    while counter < len(population):
        chance = 1
        random_num = np.random.rand()
        for i in range(len(population)):
            score_chance = (score_max-score_list[i]) / score_max
            chance = chance - score_chance
            if random_num >= chance:
                mating_pool.append(population[i])
                break
        counter += 1

def crossover():
    global mating_pool
    child_counter = 0
    while child_counter < 1:
        index1 = 0
        index2 = 0
        while index1 == index2:
            index1 = np.random.randint(0, len(mating_pool))
            index2 = np.random.randint(0, len(mating_pool))

        cut_point1 = np.random.randint(1, len(mating_pool[1])-2)
        cut_point2 = np.random.randint(cut_point1+1, len(mating_pool[1])-1)

        crossover_chance = np.random.rand()
        if crossover_chance > 0.6:
            break

        cut_1 = mating_pool[index1][cut_point1:cut_point2]
        cut_2 = mating_pool[index2][cut_point1:cut_point2]

        parent_1 = mating_pool[index1]
        parent_2 = mating_pool[index2]
        parent_1 = [x for x in parent_1 if x not in cut_1] + cut_1
        parent_2 = [x for x in parent_2 if x not in cut_2] + cut_2
        child_1 = []
        child_2 = []

        print("Schnittpunkte:", cut_1, cut_2)

        j = cut_point2
        while True:
            if j > 7:
                j = 0
            child_1.append(parent_1[j])
            child_2.append(parent_2[j])
            j += 1
            if j == cut_point2:
                break

        mating_pool[index1] = child_1
        mating_pool[index2] = child_2

        child_counter += 1

def mutate():
    global mating_pool
    for individual in mating_pool:
        mutate_chance = np.random.rand() * 100
        if mutate_chance <= 1:
            mutate_index_1 = np.random.randint(0, len(individual)-1)
            mutate_index_2 = np.random.randint(0, len(individual)-1)
            print("Mutate:", individual[mutate_index_1], individual[mutate_index_2])
            copy_mating_pool = individual[mutate_index_1]
            individual[mutate_index_1] = individual[mutate_index_2]
            individual[mutate_index_2] = copy_mating_pool

def test_optimum():
    global score_list
    for i in range(len(score_list)):
        if score_list[i] == 0:
            print("Finished Population:", population[i])
            return True
    return False

def check_conflict(x1, y1, x2, y2):
    if x1 == x2 or y1 == y2:
        return True
    if abs(x1 - x2) == abs(y1 - y2):
        return True
    return False

def update_population():
    global mating_pool
    global population
    population = mating_pool.copy()

def main():
    add_individual(i1)
    add_individual(i2)
    add_individual(i3)

    pop_counter = 0
    while pop_counter <= 100:
        calc_fitness()
        print("Fitness values:", score_list)

        if test_optimum():
            break

        select_individual()

        crossover()

        mutate()

        update_population()

        print("Population", pop_counter, ":", population)
        pop_counter += 1

if __name__ == '__main__':
    main()