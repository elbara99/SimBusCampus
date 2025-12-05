import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.preprocessing import load_data
from src.sim_model import run_sim

st.set_page_config(page_title="SimBusCampus", layout="wide")

st.title("🚌 SimBusCampus Dashboard")
st.markdown("Discrete-event simulation of university bus stop performance.")

# Sidebar
st.sidebar.header("Configuration")
nb_buses = st.sidebar.slider("Number of Buses", 1, 10, 2)
capacity = st.sidebar.slider("Bus Capacity", 10, 100, 50)
boarding_time = st.sidebar.slider("Boarding Time per Student (min)", 0.1, 2.0, 0.3)
trip_time = st.sidebar.slider("Round Trip Time (min)", 5, 60, 20)
sim_time = st.sidebar.number_input("Simulation Duration (min)", value=150)

if st.button("Run Simulation", type="primary"):
    arrivals = load_data()
    
    with st.spinner("Running simulation..."):
        res = run_sim(arrivals, nb_buses, capacity, boarding_time, trip_time, sim_time)
    
    # Comparison Logic
    if 'last_res' not in st.session_state:
        st.session_state['last_res'] = None
        
    last_res = st.session_state['last_res']
    
    # Helper for delta
    def get_delta(curr, key):
        if last_res:
            return f"{curr - last_res[key]:.2f}"
        return None

    # Metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Avg Wait Time", f"{res['avg_wait_time']:.2f} min", delta=get_delta(res['avg_wait_time'], 'avg_wait_time'), delta_color="inverse")
    c2.metric("Total Transported", f"{res['total_transported']}", delta=get_delta(res['total_transported'], 'total_transported'))
    c3.metric("Avg Bus Util", f"{res['avg_bus_utilization']*100:.1f}%", delta=get_delta(res['avg_bus_utilization']*100, 'avg_bus_utilization') if last_res else None)
    
    max_wait = max(res['raw_wait_times']) if res['raw_wait_times'] else 0
    last_max = max(last_res['raw_wait_times']) if last_res and last_res['raw_wait_times'] else 0
    delta_max = f"{max_wait - last_max:.2f}" if last_res else None
    
    c4.metric("Max Wait Time", f"{max_wait:.2f} min", delta=delta_max, delta_color="inverse")
    
    # Store current result for next time
    st.session_state['last_res'] = res
    
    # Plots
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("Queue Dynamics")
        q_df = pd.DataFrame(res['queue_over_time'], columns=["Time", "Length"])
        st.line_chart(q_df.set_index("Time"))
        
    with col_right:
        st.subheader("Wait Time Distribution")
        fig, ax = plt.subplots()
        ax.hist(res['raw_wait_times'], bins=20, color='#4c72b0', edgecolor='white')
        ax.set_xlabel("Minutes")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)
