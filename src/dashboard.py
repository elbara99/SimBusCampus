import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.preprocessing import load_data
from src.sim_model import run_sim

# --- Page Config ---
st.set_page_config(
    page_title="SimBusCampus",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for 3D / Neumorphism ---
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #1e1e2f 0%, #27293d 100%);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #27293d;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* 3D Cards */
    div[data-testid="metric-container"] {
        background: linear-gradient(145deg, #2a2c40, #232536);
        box-shadow:  5px 5px 10px #1a1b29,
                     -5px -5px 10px #343751;
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        color: white;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #ffffff !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    /* Custom Button (3D Effect) */
    div.stButton > button {
        background: linear-gradient(145deg, #4facfe, #00f2fe);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 12px;
        font-weight: bold;
        box-shadow:  4px 4px 8px #151621,
                     -4px -4px 8px #393c59;
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow:  6px 6px 12px #151621,
                     -6px -6px 12px #393c59;
    }
    div.stButton > button:active {
        transform: translateY(2px);
        box-shadow: inset 4px 4px 8px #1e3c72,
                    inset -4px -4px 8px #2a5298;
    }
    
    /* Plotly Chart Container */
    .js-plotly-plot {
        background: #27293d;
        border-radius: 15px;
        box-shadow:  5px 5px 10px #1a1b29,
                     -5px -5px 10px #343751;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- Header Section ---
col_logo, col_title = st.columns([1, 5])
with col_logo:
    try:
        st.image("assets/logo.jpg", width=120)
    except:
        st.markdown("# 🏛️")
with col_title:
    st.title("SimBusCampus")
    st.markdown("### University of Batna 2 - Smart Mobility Simulation")

st.markdown("---")

# --- Sidebar Configuration ---
with st.sidebar:
    try:
        st.image("assets/logo.jpg", use_container_width=True)
    except:
        pass
    st.markdown("## ⚙️ Control Panel")
    st.info("Adjust the simulation parameters below.")
    
    nb_buses = st.slider("🚌 Number of Buses", 1, 10, 2)
    capacity = st.slider("👥 Bus Capacity", 10, 100, 50)
    boarding_time = st.slider("⏱️ Boarding Time (min)", 0.1, 2.0, 0.3)
    trip_time = st.slider("🔄 Round Trip Time (min)", 5, 60, 20)
    sim_time = st.number_input("⏳ Duration (min)", value=150)
    
    st.markdown("---")
    run_btn = st.button("🚀 Run Simulation")

# --- Main Logic ---
if run_btn:
    arrivals = load_data()
    
    with st.spinner("Simulating campus traffic..."):
        res = run_sim(arrivals, nb_buses, capacity, boarding_time, trip_time, sim_time)
    
    # Session State for Comparison
    if 'last_res' not in st.session_state:
        st.session_state['last_res'] = None
    last_res = st.session_state['last_res']
    
    def get_delta(curr, key):
        if last_res:
            return f"{curr - last_res[key]:.2f}"
        return None

    # --- Metrics Row ---
    st.markdown("### 📊 Key Performance Indicators")
    m1, m2, m3, m4 = st.columns(4)
    
    with m1:
        st.metric("Avg Wait Time", f"{res['avg_wait_time']:.2f} min", 
                  delta=get_delta(res['avg_wait_time'], 'avg_wait_time'), delta_color="inverse")
    with m2:
        st.metric("Total Transported", f"{res['total_transported']}", 
                  delta=get_delta(res['total_transported'], 'total_transported'))
    with m3:
        util_pct = res['avg_bus_utilization'] * 100
        last_util = last_res['avg_bus_utilization'] * 100 if last_res else 0
        delta_util = f"{util_pct - last_util:.1f}%" if last_res else None
        st.metric("Avg Bus Util", f"{util_pct:.1f}%", delta=delta_util)
    with m4:
        max_wait = max(res['raw_wait_times']) if res['raw_wait_times'] else 0
        last_max = max(last_res['raw_wait_times']) if last_res and last_res['raw_wait_times'] else 0
        delta_max = f"{max_wait - last_max:.2f}" if last_res else None
        st.metric("Max Wait Time", f"{max_wait:.2f} min", delta=delta_max, delta_color="inverse")

    st.session_state['last_res'] = res
    
    st.markdown("---")

    # --- Interactive Plots (Plotly) ---
    c_left, c_right = st.columns(2)
    
    with c_left:
        st.markdown("#### 📈 Queue Dynamics")
        q_df = pd.DataFrame(res['queue_over_time'], columns=["Time", "Length"])
        
        fig_q = px.line(q_df, x="Time", y="Length", 
                        title="Student Queue Over Time",
                        template="plotly_dark",
                        line_shape="hv") # step chart
        fig_q.update_traces(line_color='#4facfe', line_width=3, fill='tozeroy', fillcolor='rgba(79, 172, 254, 0.1)')
        fig_q.update_layout(
            hovermode="x unified", 
            height=350,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        st.plotly_chart(fig_q, use_container_width=True)
        
    with c_right:
        st.markdown("#### ⏱️ Wait Time Distribution")
        fig_hist = px.histogram(x=res['raw_wait_times'], nbins=20,
                                title="Distribution of Wait Times",
                                template="plotly_dark",
                                labels={'x': 'Wait Time (min)'})
        fig_hist.update_traces(marker_color='#00f2fe', opacity=0.8, marker_line_color='white', marker_line_width=1)
        fig_hist.update_layout(
            bargap=0.1, 
            height=350,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        st.plotly_chart(fig_hist, use_container_width=True)

else:
    # Empty State
    st.markdown("""
    <div style="text-align: center; padding: 50px; color: #8b8d9f;">
        <h3>👋 Welcome to SimBusCampus</h3>
        <p>Adjust the settings in the sidebar and click <b>Run Simulation</b> to see the results.</p>
    </div>
    """, unsafe_allow_html=True)
