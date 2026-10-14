# Project notes and proof checklist

Capture authentic evidence after running the app:
- [ ] Dashboard with a successful route
- [ ] Same seed with A* and Dijkstra for comparison
- [ ] Challenging map or a no-route test (if you add a map editor)
- [ ] CLI run and generated `latest_run.json`
- [ ] Passing unit-test terminal output
- [ ] GitHub repository and rendered README

Suggested commit sequence:
1. `chore: scaffold navigation project`
2. `feat: add deterministic occupancy-grid world`
3. `feat: implement A-star Dijkstra and BFS planners`
4. `feat: add route validation and evaluation metrics`
5. `feat: build Streamlit simulation dashboard`
6. `test: cover planner and route validity`
7. `docs: add setup guide and architecture notes`

Interview explanation:
"I built a virtual grid-world navigation prototype. It creates a map of free and blocked cells, runs a selected graph-search algorithm, validates that the resulting path avoids obstacles, and displays performance metrics. It demonstrates planning and evaluation fundamentals; sensor perception and real-robot control are future integrations."
