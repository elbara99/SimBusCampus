import pandas as pd
import os
from src.preprocessing import load_data
from src.sim_model import run_sim

def run_experiments():
    arrivals = load_data()
    results = []
    
    # Define Scenarios
    scenarios = [
        {"name": "Baseline", "nb_buses": 2, "capacity": 50, "boarding_time": 0.3, "trip_time": 20},
        {"name": "Extra Bus", "nb_buses": 3, "capacity": 50, "boarding_time": 0.3, "trip_time": 20},
        {"name": "High Capacity", "nb_buses": 2, "capacity": 70, "boarding_time": 0.3, "trip_time": 20},
    ]
    
    print("Running experiments...")
    for sc in scenarios:
        print(f"  - {sc['name']}")
        res = run_sim(
            arrivals, 
            sc['nb_buses'], 
            sc['capacity'], 
            sc['boarding_time'], 
            sc['trip_time'], 
            sim_time=150
        )
        results.append({
            "scenario": sc['name'],
            "avg_wait_time": res['avg_wait_time'],
            "total_transported": res['total_transported']
        })
        
    df_res = pd.DataFrame(results)
    os.makedirs("results", exist_ok=True)
    df_res.to_csv("results/results.csv", index=False)
    print("Done. Results saved to results/results.csv")

if __name__ == "__main__":
    run_experiments()
