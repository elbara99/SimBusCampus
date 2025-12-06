# 🚌 SimBusCampus: Smart Mobility Simulation

**University of Batna 2 — Department of Computer Science**

![SimBusCampus Dashboard](assets/logo.jpg)

## 📖 Overview
**SimBusCampus** is a Discrete-Event Simulation (DES) designed to optimize student transportation during peak hours. Built with **Python** and **SimPy**, it models the complex dynamics of student arrivals, bus scheduling, and queue management.

The project features a **high-end interactive dashboard** that allows university administrators to visualize waiting times and test different fleet strategies in real-time.

---

## 🚀 Key Features
*   **Real-time Simulation**: Powered by `simpy` to model every second of the morning rush.
*   **Interactive Dashboard**: A futuristic 3D Neumorphic UI built with `streamlit`.
*   **Scenario Testing**: Compare "Baseline" vs. "Extra Bus" vs. "High Capacity" strategies.
*   **Advanced Analytics**:
    *   📉 **Queue Dynamics**: Watch the queue grow and shrink over time.
    *   ⏱️ **Wait Time Distribution**: Analyze how long students wait.
    *   🚌 **Bus Utilization**: See if buses are running full or empty.

---

## 🛠️ Tech Stack
*   **Core**: Python 3.9+
*   **Simulation**: SimPy
*   **Data**: Pandas, NumPy
*   **Visualization**: Plotly, Matplotlib
*   **UI Framework**: Streamlit

---

## 📦 Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/elbara99/SimBusCampus.git
    cd SimBusCampus
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Dashboard**:
    ```bash
    streamlit run src/dashboard.py
    ```

---

## 📊 Project Structure
```text
SimBusCampus/
├── data/               # Synthetic arrival data
├── src/
│   ├── sim_model.py    # The Simulation Engine (SimPy)
│   ├── dashboard.py    # The Interactive Web App
│   ├── experiments.py  # Batch Scenario Runner
│   └── analysis.py     # Static Plot Generation
├── assets/             # Images and Logos
├── results/            # Simulation Output Logs
└── REPORT.md           # Full Scientific Report
```

---

## 🧪 Simulation Scenarios
We tested three main strategies to reduce student wait times:

| Scenario | Buses | Capacity | Avg Wait Time | Improvement |
| :--- | :---: | :---: | :---: | :---: |
| **Baseline** | 2 | 50 | ~26 min | — |
| **High Capacity** | 2 | 70 | ~17 min | 35% |
| **Extra Bus** | 3 | 50 | **~7 min** | **72%** |

*Conclusion: Increasing frequency (Extra Bus) is more effective than increasing capacity.*

---

## 👨‍💻 Author
**Elbara**  
*Department of Computer Science, University of Batna 2*

---
*Built for the Future of Campus Mobility.*
