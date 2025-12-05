import pandas as pd
import matplotlib.pyplot as plt
import os
from src.preprocessing import load_data
from src.sim_model import run_sim

def analyze_results():
    # 1. Plot Summary Results
    if os.path.exists("results/results.csv"):
        df = pd.read_csv("results/results.csv")
        plt.figure(figsize=(8, 5))
        plt.bar(df['scenario'], df['avg_wait_time'], color=['#4c72b0', '#55a868', '#c44e52'])
        plt.title("Average Wait Time by Scenario")
        plt.ylabel("Minutes")
        plt.savefig("results/avg_wait_time.png")
        print("Saved results/avg_wait_time.png")
    else:
        print("results.csv not found. Run experiments.py first.")

    # 2. Detailed Plots (Run a fresh baseline sim)
    print("Generating detailed plots for Baseline...")
    arrivals = load_data()
    res = run_sim(arrivals, nb_buses=2, capacity=50, boarding_time=0.3, trip_time=20, sim_time=150)
    
    # Histogram
    plt.figure(figsize=(8, 5))
    plt.hist(res['raw_wait_times'], bins=20, color='skyblue', edgecolor='black')
    plt.title("Wait Time Distribution (Baseline)")
    plt.xlabel("Wait Time (min)")
    plt.ylabel("Count")
    plt.savefig("results/wait_time_hist.png")
    print("Saved results/wait_time_hist.png")
    
    # Queue over time
    times = [x[0] for x in res['queue_over_time']]
    lengths = [x[1] for x in res['queue_over_time']]
    plt.figure(figsize=(10, 5))
    plt.plot(times, lengths, drawstyle='steps-post')
    plt.title("Queue Length Over Time (Baseline)")
    plt.xlabel("Time (min)")
    plt.ylabel("Students in Queue")
    plt.grid(True, alpha=0.3)
    plt.savefig("results/queue_over_time.png")
    print("Saved results/queue_over_time.png")

if __name__ == "__main__":
    analyze_results()
