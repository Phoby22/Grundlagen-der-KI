import numpy as np

#i1 = {"A":0b001, "B":0b100, "C":0b100, "D":0b100, "E":0b001, "F":0b110, "score":0}
#i2 = {"A":0b110, "B":0b100, "C":0b100, "D":0b101, "E":0b001, "F":0b101, "score":0}
#i3 = {"A":0b100, "B":0b101, "C":0b001, "D":0b101, "E":0b001, "F":0b010, "score":0}
i1 = [0b001, 0b100, 0b100, 0b100, 0b001, 0b110]
i2 = [0b110, 0b100, 0b100, 0b101, 0b001, 0b101]
i3 = [0b100, 0b101, 0b001, 0b101, 0b001, 0b010]
i4 = [0b101, 0b101, 0b010, 0b001, 0b010, 0b001]

score_list = []
population = []
matingpool = []

def addIndividuum(i):
    population.append(i)

def calcFitness(population):
    global score_list
    score_list = []
    for i in population:
        score = 0
        if i[0] == i[1]:
            score += 1
        if i[0] == i[2]:
            score += 1
        if i[1] == i[2]:
            score += 1
        if i[1] == i[3]:
            score += 1
        if i[2] == i[3]:
            score += 1
        if i[3] == i[4]:
            score += 1
        score_list.append(score)

def testOptimum(score_list):
    for i in range(len(score_list)):
        if score_list[i] == 0:
            print("Finished Population:", population[i])
            return True
    return False

def selectIndividuum(score_list):
    global matingpool
    matingpool = []
    score_max = sum(score_list)

    counter = 0
    while counter < len(population):
        chance = 1
        randomNum = np.random.rand()
        for i in range(len(population)):
            score_chance = (score_max-score_list[i]) / score_max
            chance = chance - score_chance
            if randomNum >= chance:
                matingpool.append(population[i])
                break
        counter += 1

def crossover():
    global matingpool
    crossover_chance = np.random.rand()
    if crossover_chance <= 0.6:
        #print("Crossover Operation wird ausgeführt!")

        cut_point1 = np.random.randint(1, len(matingpool[1])-2)
        cut_point2 = np.random.randint(cut_point1+1, len(matingpool[1])-1)

        for i in range(1, len(matingpool), 2):
            child_1 = matingpool[i][:cut_point1] + matingpool[i-1][cut_point1:cut_point2] + matingpool[i][cut_point2:]
            child_2 = matingpool[i-1][:cut_point1] + matingpool[i][cut_point1:cut_point2] + matingpool[i-1][cut_point2:]
            matingpool[i] = child_1
            matingpool[i-1] = child_2

def mutation():
    global matingpool
    for chrom in range(len(matingpool)):
        for gen in range(len(matingpool[chrom])):
            mutation_chance = np.random.rand() * 100
            if mutation_chance <= 1 and checkConflict(chrom):
                length = max(1, matingpool[chrom][gen].bit_length())
                bit_index = np.random.randint(0, length)
                matingpool[chrom][gen] = matingpool[chrom][gen] ^ (1 << bit_index)

def checkConflict(chrom):
    global matingpool
    i = matingpool[chrom]

    conflicts = [(0,1), (0,2), (1,2), (1,3), (2,3), (3,4), (4,5)]

    for a,b in conflicts:
        if i[a] == i[b]:
            return True
    return False

def update_population():
    global matingpool
    global population
    population = matingpool.copy()

def main():
    addIndividuum(i1)
    addIndividuum(i2)
    addIndividuum(i3)
    addIndividuum(i4)

    pop_counter = 1
    while pop_counter <= 100:
        print("Population", pop_counter, ":", population)
        calcFitness(population)

        if testOptimum(score_list):
            print("Solution found!")
            break

        selectIndividuum(score_list)

        crossover()

        mutation()

        update_population()

        pop_counter += 1

if __name__ == '__main__':
    main()

