# SimBusCampus: A Discrete-Event Simulation for University Mobility Optimization

**University of Batna 2**  
**Department of Computer Science**  
**Project Report**

---

## Abstract

This report presents **SimBusCampus**, a Discrete-Event Simulation (DES) system designed to model and optimize student transportation during peak morning hours. Using Python and the SimPy framework, the project simulates student arrivals, queueing dynamics, and bus boarding processes. The system includes an interactive dashboard built with Streamlit, allowing decision-makers to visualize the impact of varying fleet sizes, bus capacities, and scheduling strategies. Experimental results demonstrate that adding a single bus reduces average waiting times significantly more than increasing individual bus capacity, providing actionable insights for campus logistics.

---

## 1. Introduction

### 1.1 Problem Statement
University campuses often face significant logistical challenges during morning peak hours (07:30 – 09:30). The "last mile" transportation from city centers or dormitories to campus gates is a bottleneck, leading to:
*   Long student queues.
*   Unpredictable waiting times.
*   Late arrivals to lectures.
*   Inefficient use of transport resources.

### 1.2 Objectives
The primary objective of this project is to build a computational model of the bus stop system to:
1.  **Quantify Performance**: Measure average waiting times, queue lengths, and bus utilization.
2.  **Test Scenarios**: Compare the effectiveness of different interventions (e.g., adding buses vs. larger buses) without the cost of real-world trials.
3.  **Visualize Data**: Provide an interactive tool for stakeholders to explore simulation results in real-time.

---

## 2. Methodology

### 2.1 Discrete-Event Simulation (DES)
Unlike continuous simulation (which models time as a smooth flow), DES models a system as a sequence of discrete events in time. The state of the system changes only when an event occurs (e.g., a student arrives, a bus departs). Between events, no change is assumed to occur, allowing the simulation to jump in time efficiently.

### 2.2 Technology Stack
*   **Python**: The core programming language, chosen for its rich ecosystem in data science.
*   **SimPy**: A process-based discrete-event simulation framework. It allows modeling active components (students, buses) as Python generator functions.
*   **Streamlit**: A framework for turning data scripts into shareable web apps. Used here for the interactive dashboard.
*   **Plotly**: Used for generating interactive, high-fidelity visualizations of queue dynamics and wait time distributions.

### 2.3 Model Architecture
The simulation consists of three main entities:
1.  **The Environment**: Manages the simulation clock and event scheduling.
2.  **The Student**: Modeled as an entity that arrives at a specific time (generated via an Exponential Distribution to mimic Poisson arrivals) and requests a resource (the bus).
3.  **The Bus**: Modeled as a cyclic process that:
    *   Arrives at the stop.
    *   Boards students from the queue (taking $t_{board}$ seconds per student).
    *   Departs when full or the queue is empty.
    *   Travels for a fixed round-trip time ($t_{trip}$).

---

## 3. Implementation Details

### 3.1 Project Structure
The codebase is organized modularly to separate data, logic, and presentation:
```text
SimBusCampus/
├── data/               # Synthetic arrival datasets
├── src/
│   ├── sim_model.py    # Core SimPy logic (The Engine)
│   ├── preprocessing.py# Data generation (The Input)
│   ├── experiments.py  # Batch scenario runner
│   └── dashboard.py    # Interactive Web UI
├── results/            # Output logs and charts
└── README.md           # Documentation
```

### 3.2 Simulation Logic (`sim_model.py`)
The core logic is encapsulated in the `run_sim` function. Key algorithms include:

**Student Generation:**
```python
def student_generator(env, arrivals):
    for p in arrivals:
        yield env.timeout(p['arrival_time'] - env.now)
        queue.append(p) # Student joins the queue
```

**Bus Process:**
```python
def bus_process(env, capacity):
    while True:
        # Boarding Logic
        boarded = 0
        while boarded < capacity and queue:
            student = queue.pop(0)
            yield env.timeout(BOARDING_TIME) # Time to tap card/sit
            boarded += 1
        
        # Trip Logic
        yield env.timeout(TRIP_TIME)
```

### 3.3 User Interface
The dashboard was designed with a "3D Neumorphic" aesthetic to align with modern design trends. It features:
*   **Control Panel**: Sliders to adjust $N_{buses}$, $Capacity$, and $T_{trip}$.
*   **Real-time Metrics**: Displays "Avg Wait Time" and "Bus Utilization" with delta indicators comparing the current run to the previous one.
*   **Interactive Charts**: Zoomable line charts for queue length and histograms for wait times.

---

## 4. Results and Analysis

We conducted experiments using a synthetic dataset of 500 students arriving over a 120-minute peak period.

### 4.1 Scenario A: Baseline
*   **Configuration**: 2 Buses, Capacity 50.
*   **Observation**: The system quickly becomes overwhelmed. The queue grows linearly because the arrival rate ($\lambda$) exceeds the service rate ($\mu$).
*   **Result**: Average wait time is high (~26 minutes), with some students waiting over 45 minutes.

### 4.2 Scenario B: High Capacity
*   **Configuration**: 2 Buses, Capacity 70 (+40% increase).
*   **Observation**: Larger buses clear the queue more effectively per trip, but the *frequency* of service remains low. Students still wait a long time for the bus to return.
*   **Result**: Average wait time drops to ~17 minutes. An improvement, but not optimal.

### 4.3 Scenario C: Extra Bus
*   **Configuration**: 3 Buses, Capacity 50.
*   **Observation**: Adding a bus increases the service frequency. The gap between bus arrivals shrinks from 10 minutes to 6.6 minutes.
*   **Result**: Average wait time plummets to ~7 minutes.
*   **Conclusion**: **Frequency is more important than capacity** for this specific arrival pattern.

### 4.4 Bus Utilization
In Scenario C, bus utilization dropped slightly (buses were not always 100% full), indicating that the system had enough slack to handle unexpected surges in student arrivals.

---

## 5. Conclusion and Future Work

### 5.1 Conclusion
The **SimBusCampus** project successfully demonstrates the power of simulation in solving campus logistics problems. The tool provides University of Batna 2 administrators with a risk-free environment to test policies. Our analysis suggests that investing in an additional vehicle is the most effective strategy for reducing student wait times, yielding a 72% improvement over the baseline.

### 5.2 Future Work
1.  **Stochastic Travel Times**: Model traffic jams by making trip times variable (e.g., Normal Distribution) rather than fixed.
2.  **Smart Dispatching**: Implement logic where buses depart early if they have been waiting too long, even if not full.
3.  **Real Data Integration**: Replace synthetic data with actual swipe-card logs from the university transport service.

---

## 6. References
1.  SimPy Documentation. (2024). *Discrete Event Simulation for Python*.
2.  Banks, J. (2010). *Discrete-Event System Simulation*. Pearson.
3.  Streamlit. (2024). *The fastest way to build and share data apps*.
