# Cloud Task Scheduler

This branch contains a Streamlit dashboard for comparing cloud job scheduling strategies across a configurable cluster of compute nodes.

## What it does

- Loads workload data from `data/clean_google_jobs.csv`
- Lets you configure cluster nodes with custom speed and hourly cost values
- Compares multiple scheduling approaches on the same workload
- Reports makespan, execution cost, and resource utilization
- Visualizes scheduling outcomes in an interactive dashboard

## Included scheduling strategies

- Shortest Job First (SJF)
- Round Robin (RR)
- Random
- Genetic Algorithm (GA)
- Particle Swarm Optimization (PSO)

## Project structure

- `/app.py` - Streamlit application entry point
- `/src/models.py` - job and node models
- `/src/data_loader.py` - workload loading helpers
- `/src/baselines.py` - baseline scheduling algorithms
- `/src/engine.py` - simulation metrics and execution engine
- `/src/optimizers.py` - GA and PSO optimizers
- `/data/clean_google_jobs.csv` - sample workload data

## Run locally

### Option 1: Python environment

```bash
pip install -r requirements.txt
streamlit run app.py
```

### Option 2: Docker

```bash
docker compose up --build
```

Then open `http://localhost:8501`.

## Dashboard workflow

1. Review or adjust the cluster nodes in the sidebar.
2. Load the workload dataset.
3. Select one or more schedulers.
4. Tune GA or PSO parameters if needed.
5. Run the simulation and compare metrics.

## Notes

- The dashboard starts with five default cloud instance profiles.
- Cost is calculated from node runtime and hourly price.
- Makespan and utilization are computed from the simulated job assignments in `src/engine.py`.
