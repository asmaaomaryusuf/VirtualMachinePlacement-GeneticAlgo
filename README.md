# VirtualMachinePlacement-GeneticAlgo

This project applies a Genetic Algorithm (GA) to solve the Virtual Machine Placement problem efficiently. The aim is to assign a set of virtual machines (VMs) to physical machines (PMs) to optimize resource usage and avoid overload, improving overall system performance.

---

## Problem Statement
The Virtual Machine Placement (VMP) problem involves allocating virtual machines with specific resource demands (e.g., CPU, RAM) to physical machines with limited capacity, aiming to optimize placement by minimizing overload and maximizing utilization. VMP is a challenging NP-hard problem common in cloud computing and data centers.

---

## Why Genetic Algorithm?
Genetic Algorithms are robust metaheuristic optimization techniques inspired by natural evolution. They effectively search large, complex spaces and find near-optimal solutions for problems like VMP without requiring gradient information.

---

## Key advantages:

Handles large search spaces

Does not need problem-specific mathematical models

Flexible and adaptable to different constraints

---

## How It Works
Initialization: Create an initial population of random VM-to-PM placements.

Fitness Evaluation: Calculate fitness based on overload penalties and resource usage.

Selection: Select parent solutions (e.g., best individuals) for reproduction.

Crossover: Combine two parents to create offspring with mixed VM placements.

Mutation: Randomly alter offspring VM assignments to maintain diversity.

Termination: Iterate over generations until convergence or max generations reached.

---

## Project Structure

genetic-vm-placement/

vmp-data.txt          # Input file: number of VMs, PMs, and their resource specs  
vmp_ga.py             # Main script implementing the Genetic Algorithm  
README.md             # Project documentation (this file)  
