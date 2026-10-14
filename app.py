"""Streamlit frontend for the AI-Based Autonomous Navigation System."""
import json
from pathlib import Path
import pandas as pd
import streamlit as st

from src.navigation.simulator import run_simulation
from src.navigation.visualization import render_map_figure

st.set_page_config(page_title="Autonomous Navigation Lab", page_icon="🧭", layout="wide")

st.title("🧭 AI-Based Autonomous Navigation System")
st.caption("Virtual grid-world simulation • path planning • obstacle avoidance • measurable test runs")

with st.sidebar:
    st.header("Simulation controls")
    scenario = st.selectbox("Environment preset", ["easy", "moderate", "challenging"], index=1)
    algorithm = st.selectbox("Path-planning algorithm", ["astar", "dijkstra", "bfs"], index=0,
                             help="A* uses a heuristic; Dijkstra uses uniform-cost search; BFS is shortest-path for unweighted grids.")
    grid_size = st.slider("Grid size", min_value=12, max_value=40, value=24, step=2)
    density = st.slider("Obstacle density", min_value=0.05, max_value=0.35, value=0.20, step=0.01)
    seed = st.number_input("Random seed", min_value=0, max_value=100000, value=7, step=1)
    run_clicked = st.button("▶ Run navigation", type="primary", use_container_width=True)
    st.divider()
    st.caption("This is a software simulation, not a safety-certified or real-world vehicle controller.")

if "result" not in st.session_state:
    st.session_state.result = None

if run_clicked or st.session_state.result is None:
    with st.spinner("Generating environment and planning a route..."):
        st.session_state.result = run_simulation(
            scenario=scenario, algorithm=algorithm, seed=int(seed),
            grid_size=grid_size, obstacle_density=float(density)
        )

result = st.session_state.result
left, right = st.columns([1.7, 1])
with left:
    st.subheader("Environment and planned route")
    st.pyplot(render_map_figure(result), use_container_width=True)
    st.caption("Legend: green = start, red = goal, black = obstacle, blue = planned route, yellow = explored cells.")
with right:
    st.subheader("Run metrics")
    m1, m2 = st.columns(2)
    m1.metric("Status", "SUCCESS" if result.success else "NO PATH")
    m2.metric("Path length", f"{result.path_length:.1f}" if result.success else "—")
    m3, m4 = st.columns(2)
    m3.metric("Planning time", f"{result.planning_time_ms:.2f} ms")
    m4.metric("Expanded nodes", result.nodes_expanded)
    m5, m6 = st.columns(2)
    m5.metric("Obstacle count", result.obstacle_count)
    m6.metric("Collision checks", result.collision_checks)
    st.write("**Scenario:**", result.scenario.title())
    st.write("**Algorithm:**", result.algorithm.upper())
    st.write("**Seed:**", result.seed)
    st.write("**Grid:**", f"{result.grid_size} × {result.grid_size}")
    st.write("**Path status:**", result.message)

st.subheader("How the pipeline works")
st.markdown("""
1. **Environment generation** creates a reproducible grid with obstacles.
2. **Perception layer** exposes obstacle occupancy to the planner (simulated map input).
3. **Planning** searches for a collision-free route using the selected algorithm.
4. **Navigation validation** checks that every route cell is in bounds and obstacle-free.
5. **Evaluation** records path length, planning time, expanded nodes, and collision checks.
""")

with st.expander("Run report (JSON)"):
    report = json.dumps(result.to_dict(), indent=2)
    st.code(report, language="json")
    st.download_button("Download run report", data=report, file_name="navigation_run.json",
                       mime="application/json")

if result.path:
    df = pd.DataFrame([{"step": i, "x": cell[0], "y": cell[1]} for i, cell in enumerate(result.path)])
    with st.expander("Planned waypoint table"):
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.download_button("Download waypoints (CSV)", data=df.to_csv(index=False),
                           file_name="planned_waypoints.csv", mime="text/csv")

st.divider()
st.caption("Portfolio note: describe this as a simulated navigation prototype. Do not claim real-vehicle validation.")
