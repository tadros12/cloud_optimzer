# Cloud Optimizer: Computational Intelligence for Task Scheduling

## Project Overview
This project explores the application of various Computational Intelligence (CI) metaheuristic algorithms to optimize task scheduling in cloud computing environments. The primary goal is to efficiently assign a set of jobs to a pool of heterogeneous compute nodes, minimizing both the total execution time (Makespan) and the operational cost.

## Key Features

-   **Multiple Metaheuristic Algorithms:** Implements and compares Genetic Algorithm (GA), Particle Swarm Optimization (PSO), Grey Wolf Optimizer (GWO), Bee Colony Optimization (BCO), and Whale Optimization Algorithm (WOA).
-   **Deterministic Baselines:** Includes Round Robin (RR) and Shortest Job First (SJF) schedulers for performance benchmarking.
-   **Hybrid Optimization Mode:** Allows for chaining two metaheuristic algorithms sequentially (e.g., GA for global search followed by PSO for local refinement) to leverage their combined strengths.
-   **Diversity Extension Mechanism:** A novel restart mechanism that combats premature convergence by replacing a percentage of the worst-performing solutions with new random ones every N generations.
-   **Dynamic UI with Real-time Visualization:** A responsive web-based UI (rendered via `pywebview`) provides interactive control over algorithms and parameters, with live plotting of convergence, makespan, and cost.
-   **Real-time Debugging Console:** A built-in, floating console that streams algorithm progress, diversity events, and fitness updates directly from the Python backend.
-   **Interactive Node Management:** Users can add, update, and delete compute nodes directly from the UI to observe their impact on scheduling.

## Getting Started

### Prerequisites

To run this application, you will need `Python 3.8+` and `uv` (a fast Python package installer and resolver).

1.  **Install `uv` (if you haven't already):**
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
    Ensure `uv` is added to your PATH.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/cloud-optimizer.git # Replace with actual repo URL
    cd cloud-optimizer
    ```
2.  **Create and activate the virtual environment with `uv`:**
    ```bash
    uv venv
    source .venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    uv pip install -r requirements.txt
    ```

## How to Run

After installation, you can launch the application:

```bash
python main_gui.py
```

This will open the graphical user interface where you can configure and run simulations.

## Project Structure

-   `main_gui.py`: The entry point for the desktop GUI, bridging the web frontend with the Python backend.
-   `src/`: Contains the core Python logic for the simulation and algorithms.
    -   `src/models.py`: Defines data structures for `Job` and `Node`.
    -   `src/engine.py`: The simulation engine that calculates makespan and cost for a given schedule.
    -   `src/optimizers.py`: Implementations of various CI metaheuristic algorithms (GA, PSO, GWO, BCO, WOA).
    -   `src/baselines.py`: Implementations of deterministic scheduling baselines (RR, SJF).
    -   `src/data_loader.py`: Handles loading job data and generating nodes.
-   `ui/stitch/code.html`: The web-based frontend interface (HTML, Tailwind CSS, JavaScript).
-   `data/`: Stores dataset files (e.g., `clean_google_jobs.csv`).
-   `CI-project-docs/`: Contains the detailed technical report of the system design (LaTeX).
-   `CI-theoretical-paper/`: Contains the theoretical paper discussing the algorithms and approach (LaTeX).
-   `experiment_results.csv`: Stores the results from automated experimental runs for comparison.

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
