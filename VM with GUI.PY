import random
import customtkinter as ctk
from tkinter import filedialog
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ---------------- Genetic Algorithm Logic ----------------

def load_data(file_path):
    with open(file_path) as f:
        lines = [line for line in f if not line.startswith("#")]
        num_vms, num_pms = map(int, lines[0].split())
        vm_data = [tuple(map(int, line.split())) for line in lines[1:num_vms+1]]
        pm_data = [tuple(map(int, line.split())) for line in lines[num_vms+1:]]
    return num_vms, num_pms, vm_data, pm_data

def random_solution(num_vms, num_pms):
    return [random.randint(0, num_pms - 1) for _ in range(num_vms)]

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

def crossover(p1, p2):
    point = random.randint(1, len(p1) - 1)
    return p1[:point] + p2[point:]

def mutate(ind, num_pms, rate=0.1):
    for i in range(len(ind)):
        if random.random() < rate:
            ind[i] = random.randint(0, num_pms - 1)
    return ind

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

        population = next_gen

    return population[0]

# ---------------- Gantt Chart Drawing ----------------

def show_gantt_chart(solution, num_pms):
    fig, ax = plt.subplots(figsize=(7, 4))

    colors = plt.cm.get_cmap('tab20', len(solution))

    pm_map = {pm: [] for pm in range(num_pms)}
    for vm_idx, pm_idx in enumerate(solution):
        pm_map[pm_idx].append(vm_idx)

    for pm_idx, vms in pm_map.items():
        for idx, vm_id in enumerate(vms):
            ax.broken_barh([(idx, 1)], (pm_idx - 0.4, 0.8),
                           facecolors=colors(vm_id),
                           edgecolor='black')
            ax.text(idx + 0.5, pm_idx, f"VM{vm_id}", va='center', ha='center', fontsize=8, color="white")

    ax.set_yticks(range(num_pms))
    ax.set_yticklabels([f"PM {i}" for i in range(num_pms)])
    ax.set_xlabel("VM Index within PM")
    ax.set_title("Gantt Chart: VM Placement")

    plt.tight_layout()
    return fig

# ---------------- GUI Part ----------------

class VMApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("VM Placement using Genetic Algorithm")
        self.geometry("600x500")
        ctk.set_appearance_mode("dark")

        self.file_path = None

        self.label = ctk.CTkLabel(self, text="Virtual Machine Placement Optimizer", font=("Arial", 20, "bold"))
        self.label.pack(pady=20)

        self.browse_btn = ctk.CTkButton(self, text="Load VMP Data File", command=self.browse_file)
        self.browse_btn.pack(pady=10)

        self.run_btn = ctk.CTkButton(self, text="▶ Run Genetic Algorithm", command=self.run_ga)
        self.run_btn.pack(pady=10)

        self.output_box = ctk.CTkTextbox(self, width=550, height=280)
        self.output_box.pack(pady=20)

    def browse_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if path:
            self.file_path = path
            self.output_box.insert("end", f"✔ File loaded: {os.path.basename(path)}\n")

    def run_ga(self):
        if not self.file_path:
            self.output_box.insert("end", "⚠ Please load a data file first.\n")
            return

        try:
            num_vms, num_pms, vm_data, pm_data = load_data(self.file_path)
            best = genetic_algorithm(vm_data, pm_data)
            self.output_box.insert("end", "\n Final VM Placement:\n")
            for i, pm in enumerate(best):
                self.output_box.insert("end", f"VM {i} → PM {pm}\n")

            # Show Gantt Chart in a new window
            fig = show_gantt_chart(best, num_pms)
            chart_window = ctk.CTkToplevel(self)
            chart_window.title("Gantt Chart")
            chart_window.geometry("750x400")

            canvas = FigureCanvasTkAgg(fig, master=chart_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        except Exception as e:
            self.output_box.insert("end", f" Error: {str(e)}\n")

if __name__ == "__main__":
    app = VMApp()
    app.mainloop()
