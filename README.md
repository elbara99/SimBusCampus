# SimBusCampus

A discrete-event simulation (DES) of a university bus stop using Python and SimPy.

## Overview
This project models student arrivals during morning peak hours and simulates the bus boarding process. It allows comparing different scenarios (e.g., adding buses, increasing capacity) to optimize waiting times.

## Architecture
- **data/**: Contains synthetic arrival data.
- **src/**:
    - `sim_model.py`: Core SimPy simulation logic.
    - `preprocessing.py`: Data generation and loading.
    - `experiments.py`: Runs multiple scenarios and saves results.
    - `analysis.py`: Generates plots from results.
    - `dashboard.py`: Interactive Streamlit app.
- **results/**: Stores output CSVs and plots.

## Installation
1. Create a virtual environment (optional).
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Run Experiments
Run the batch scenarios (Baseline, Extra Bus, High Capacity):
```bash
python -m src.experiments
```
Results will be saved to `results/results.csv`.

### Analyze Results
Generate plots (histograms, queue length):
```bash
python -m src.analysis
```
Images will be saved in `results/`.

### Run Dashboard
Launch the interactive web app:
```bash
streamlit run src/dashboard.py
```
