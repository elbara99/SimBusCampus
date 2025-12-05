import pandas as pd
import numpy as np
import os

def generate_synthetic_data(filepath="data/arrivals_sample.csv", n_students=500, duration=120):
    """Generates synthetic arrival data using exponential distribution."""
    # Avg inter-arrival time
    beta = duration / n_students
    inter_arrivals = np.random.exponential(scale=beta, size=n_students)
    arrival_times = np.cumsum(inter_arrivals)
    
    # Filter to max duration
    arrival_times = arrival_times[arrival_times <= duration]
    
    df = pd.DataFrame({
        "student_id": range(len(arrival_times)),
        "arrival_time": arrival_times
    })
    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath, index=False)
    print(f"Generated {len(df)} arrivals in {filepath}")

def load_data(filepath="data/arrivals_sample.csv"):
    """Loads arrival data, generating it if missing."""
    if not os.path.exists(filepath):
        generate_synthetic_data(filepath)
    
    df = pd.read_csv(filepath)
    return df.to_dict('records')
