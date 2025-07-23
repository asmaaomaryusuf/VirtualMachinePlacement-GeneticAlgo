import random

# read data from file
def load_data(file_path):
    with open(file_path) as f:
        lines = [line for line in f if not line.startswith("#")]
        num_vms, num_pms = map(int, lines[0].split())
        vm_data = [tuple(map(int, line.split())) for line in lines[1:num_vms+1]]
        pm_data = [tuple(map(int, line.split())) for line in lines[num_vms+1:]]
    return num_vms, num_pms, vm_data, pm_data

# random indevedual
def random_solution(num_vms, num_pms):
    return [random.randint(0, num_pms - 1) for _ in range(num_vms)]

# calc fitness
def fitness(solution, vm_data, pm_data):
    usage = {i: {"cpu": 0, "ram": 0} for i in range(len(pm_data))}
    used = set()
    overload = 0

    for vm_idx, pm_idx in enumerate(solution):
        cpu, ram = vm_data[vm_idx]
        usage[pm_idx]["cpu"] += cpu
        usage[pm_idx]["ram"] += ram
        used.add(pm_idx)

    for pm_idx, res in usage.items():
        if res["cpu"] > pm_data[pm_idx][0] or res["ram"] > pm_data[pm_idx][1]:
            overload += 1

    return 1 / (1 + overload + len(used))

# crossover
def crossover(p1, p2):
    point = random.randint(1, len(p1) - 1)
    return p1[:point] + p2[point:]

# mutation
def mutate(ind, num_pms, rate=0.1):
    for i in range(len(ind)):
        if random.random() < rate:
            ind[i] = random.randint(0, num_pms - 1)
    return ind

# GA loop
def genetic_algorithm(vm_data, pm_data, generations=100, pop_size=30):
    num_vms = len(vm_data)
    num_pms = len(pm_data)
    population = [random_solution(num_vms, num_pms) for _ in range(pop_size)]

    for gen in range(generations):
        population = sorted(population, key=lambda x: fitness(x, vm_data, pm_data), reverse=True)
        next_gen = population[:5]  # elitism
        while len(next_gen) < pop_size:
            p1 = random.choice(population[:10])
            p2 = random.choice(population[:10])
            child = crossover(p1, p2)
            child = mutate(child, num_pms)
            next_gen.append(child)

        best_fit = fitness(population[0], vm_data, pm_data)
        print(f"Gen {gen}: Fitness = {best_fit:.4f}")

        population = next_gen

    return population[0]

# Main
if __name__ == "__main__":
    num_vms, num_pms, vm_data, pm_data = load_data("vmp-data.txt")
    best = genetic_algorithm(vm_data, pm_data)

    print("\n Final VM placement:")
    for i, pm in enumerate(best):
        print(f"VM {i} → PM {pm}")
