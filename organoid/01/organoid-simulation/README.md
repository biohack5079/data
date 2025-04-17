# Organoid Simulation Project

This project simulates an organoid composed of several dozen cells, allowing for the exploration of cellular interactions and dynamics within a controlled environment.

## Overview

The organoid simulation aims to model the behavior of a collection of cells, each represented by a `Cell` class. The interactions between these cells are managed by the `Organoid` class, while the overall simulation process is orchestrated by the `Simulation` class. This project provides a framework for studying the effects of various parameters on cell behavior and organoid dynamics.

## Installation

To set up the project, follow these steps:

1. Clone the repository:
   ```
   git clone <repository-url>
   cd organoid-simulation
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the simulation, you can execute the `simulation.py` script. This will initialize the organoid and run the simulation over a specified time period.

Example:
```python
from src.simulation import Simulation

sim = Simulation()
sim.run()
```

## Testing

Unit tests are provided for each class in the `tests` directory. You can run the tests using:
```
pytest tests/
```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.