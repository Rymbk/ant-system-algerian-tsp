"""
Algeria TSP - Ant Colony Optimization
Main Streamlit Application
"""
import streamlit as st
import time

from data.wilayas import WILAYAS
from algorithms.aco import AntColonyOptimization
from utils.distance import build_distance_matrix
from utils.visualization import plot_tour


def main():
    """Main application function."""
    st.set_page_config(
        page_title="Algeria TSP - ACO",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Enhanced CSS with gradient background
    st.markdown("""
        <style>
        /* Main gradient background */
        .main {
            background: linear-gradient(135deg, 
                #0f0f1e 0%, 
                #1a1a2e 25%, 
                #2d1b3d 50%, 
                #1a1a2e 75%, 
                #0f0f1e 100%);
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        }
        
        /* Metric cards */
        [data-testid="stMetricValue"] {
            font-size: 28px;
            color: #00ff88;
            font-weight: bold;
        }
        
        /* Headers - simple white */
        h1, h2, h3 {
            color: white !important;
        }
        
        /* Buttons */
        .stButton>button {
            width: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 12px;
            font-weight: bold;
            font-size: 16px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }
        
        /* Sliders */
        .stSlider {
            padding: 10px 0;
        }
        
        /* Select boxes */
        .stSelectbox {
            color: white;
        }
        
        /* Divider */
        hr {
            border-color: rgba(78, 205, 196, 0.3);
            margin: 20px 0;
        }
        
        /* Cards effect */
        div[data-testid="stVerticalBlock"] > div {
            background: rgba(255, 255, 255, 0.02);
            border-radius: 15px;
            padding: 5px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Title with simple bold white styling
    st.markdown("""
        <h1 style='text-align: center; font-size: 3em; margin-bottom: 10px; color: white; font-weight: 700;'>
            🗺️ Traveling Salesman Problem
        </h1>
        <h2 style='text-align: center; color: #b0b0b0; font-size: 1.3em; margin-top: 0; font-weight: 400;'>
            Algeria - Ant Colony Optimization
        </h2>
        <p style='text-align: center; color: #808080; font-size: 1em; margin-top: 5px;'>
            Optimizing routes across 58 Wilayas using bio-inspired algorithms
        </p>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'aco' not in st.session_state:
        distance_matrix = build_distance_matrix(WILAYAS)
        st.session_state.aco = None
        st.session_state.iteration = 0
        st.session_state.best_tour = None
        st.session_state.best_distance = None
        st.session_state.avg_distance = None
        st.session_state.distance_matrix = distance_matrix
        st.session_state.running = False
    
    # Sidebar controls
    with st.sidebar:
        st.markdown("### ⚙️ Control Panel")
        st.markdown("---")
        
        st.markdown("#### 📍 Route Selection")
        wilaya_names = [w['name'] for w in WILAYAS]
        
        start_wilaya = st.selectbox("🔴 Start Wilaya", wilaya_names, index=0)
        end_wilaya = st.selectbox("🟡 End Wilaya", wilaya_names, index=15)
        
        start_idx = wilaya_names.index(start_wilaya)
        end_idx = wilaya_names.index(end_wilaya)
        
        st.markdown("---")
        st.markdown("#### 🐜 Algorithm Parameters")
        
        num_ants = st.slider("🐜 Number of Ants", 10, 100, 30, 5)
        alpha = st.slider("α (Pheromone Weight)", 0.0, 5.0, 1.0, 0.1)
        beta = st.slider("β (Distance Weight)", 0.0, 10.0, 5.0, 0.5)
        evaporation = st.slider("💨 Evaporation Rate", 0.1, 0.9, 0.5, 0.05)
        max_iterations = st.slider("🔄 Max Iterations", 50, 500, 200, 25)
        
        st.markdown("---")
        st.markdown("#### 🎮 Controls")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("▶️ Start", use_container_width=True):
                st.session_state.aco = AntColonyOptimization(
                    st.session_state.distance_matrix,
                    num_ants, alpha, beta, evaporation, 100
                )
                st.session_state.iteration = 0
                st.session_state.running = True
                st.session_state.best_tour = None
                st.session_state.best_distance = None
        
        with col2:
            if st.button("🔄 Reset", use_container_width=True):
                st.session_state.aco = None
                st.session_state.iteration = 0
                st.session_state.running = False
                st.session_state.best_tour = None
                st.session_state.best_distance = None
                st.rerun()
        
        st.markdown("---")
        st.markdown("#### 📊 Statistics")
        
        # Progress bar
        progress = st.session_state.iteration / max_iterations if max_iterations > 0 else 0
        st.progress(progress)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Iteration", f"{st.session_state.iteration}")
        with col2:
            st.metric("Max", f"{max_iterations}")
        
        if st.session_state.best_distance:
            st.metric("🏆 Best Distance", f"{st.session_state.best_distance:.2f}")
        else:
            st.metric("🏆 Best Distance", "-")
        
        if st.session_state.avg_distance:
            st.metric("📈 Avg Distance", f"{st.session_state.avg_distance:.2f}")
        else:
            st.metric("📈 Avg Distance", "-")
        
        st.markdown("---")
        st.markdown("""
        <div style='background: rgba(0, 255, 136, 0.1); padding: 15px; border-radius: 10px; border-left: 4px solid #00ff88;'>
            <p style='margin: 0; font-size: 0.9em; color: #a0a0a0;'>
                <strong style='color: #00ff88;'>Legend:</strong><br>
                🔴 Start Point<br>
                🟡 End Point<br>
                🔵 Intermediate<br>
                ➡️ Direction
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content area
    chart_placeholder = st.empty()
    
    # Run algorithm
    if st.session_state.running and st.session_state.iteration < max_iterations:
        best_tour, best_distance, avg_distance = st.session_state.aco.run_iteration(
            start_idx, end_idx
        )
        
        st.session_state.best_tour = best_tour
        st.session_state.best_distance = best_distance
        st.session_state.avg_distance = avg_distance
        st.session_state.iteration += 1
        
        if st.session_state.iteration >= max_iterations:
            st.session_state.running = False
            st.balloons()
        
        time.sleep(0.05)
        st.rerun()
    
    # Display visualization
    with chart_placeholder.container():
        if st.session_state.best_tour:
            fig = plot_tour(WILAYAS, st.session_state.best_tour, start_idx, end_idx)
            st.pyplot(fig, use_container_width=True)
        else:
            fig = plot_tour(WILAYAS, None, start_idx, end_idx)
            st.pyplot(fig, use_container_width=True)


if __name__ == "__main__":
    main()