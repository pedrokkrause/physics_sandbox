# Physics Sandbox

**Physics Sandbox** is a minimal, extensible Python engine for simulating classical mechanics using only Newton’s laws. Build particle–spring systems, add custom forces, and watch complex rotational behaviors—like precession, nutation, and the intermediate-axis theorem—emerge naturally, without directly using the formulas of rotational mechanics.

https://github.com/user-attachments/assets/303774ed-6e29-48f2-ba16-f0718d8c103e

---

## Features

* **Pure Newtonian Core:** Model any system using point masses and springs; no rigid body equations needed.
* **Custom Forces:** Add external fields or custom force laws with simple Python functions.
* **Emergent Rotational Motion:** See phenomena like precession, nutation, and tumbling arise from basic principles.
* **VPython Visualization:** Real-time 3D viewer for interactive exploration.
* **Energy Tracking:** Monitor kinetic and potential energy for checks and analysis.
* **Headless/Scriptable:** Use `physics.py` alone for batch simulations or analysis—visualization is optional.
* **Self-Contained Examples:** Ready-to-run scripts demonstrating core concepts and advanced effects.

---

## Installation

**Option 1: Download ZIP**

1. Go to [the repository page](https://github.com/pedrokkrause/physics_sandbox).
2. Click the green **Code** button, then choose **Download ZIP**.
3. Extract the ZIP file to a folder on your computer.
4. Open that folder in your terminal or command prompt.

**Option 2: Using Git**

```bash
git clone https://github.com/pedrokkrause/physics_sandbox.git
cd physics_sandbox
```

**Install Required Python Packages**

You need [Python](https://www.python.org/downloads/) (version 3.7 or higher recommended).
Install the required packages with:

```bash
pip install numpy vpython
```

*(If you see an error, try `pip3` instead of `pip`.)*

> **Note:** VPython is only needed for visualization. You can run simulations without graphics if you prefer.

---

## Quickstart

**Example: Simple Pendulum**

This example simulates a pendulum as two masses connected by a very stiff spring (representing a rigid rod), with gravity as an external force.

```python
from physics import *
from visualization import *
import numpy as np

# Create a simulation with a small timestep for accuracy
sim = Simulation(dt=5e-6)

# Add a fixed pivot and a moving bob
pivot = sim.add_particle(mass=1.0, position=(0, 0, 1), movable=False)
bob = sim.add_particle(mass=1.0, position=(0, 0, 0), velocity=(2, 0, 0))

# Connect the two with a very stiff spring (acts like a rigid rod)
sim.add_spring(pivot, bob, k=100000)

# Add gravity as a force field
g = 9.8
def gravity(particle):
    return np.array([0, 0, -g])
sim.add_field(gravity)

# Optional: Set up real-time visualization
vis = Visualization(
    simulation=sim,
    resolution=(1900, 900),
    sphere_radius=1 / 14,
    sphere_color=color.blue,
    spring_radius=1 / 50,
    spring_color=color.gray(luminance=0.7)
)

# Run the simulation
i = 0
while True:
    if i % 1000 == 0:
        vis.update()
    sim.update()
    i += 1
```

> **Note:**
> The line `if i % 1000 == 0:` ensures that the visualization refreshes every 1000 simulation steps.
> As the physics updates much faster than the screen refresh rate, this ensures a smooth animation and efficient performance

---

## Headless Usage

You can use **physics.py** by itself for non-interactive simulations, automated testing, or integration with data analysis tools—no visualization required.

```python
from physics import Simulation

sim = Simulation(dt=1e-3)
# ... configure your system ...
for _ in range(10000):
    sim.update()
# Analyze, plot, or export results as needed
```

---

## Example Demos

This repository includes several self-contained example scripts that illustrate key capabilities:

| Example File          | Demonstrates                                      |
| --------------------- | ------------------------------------------------- |
| `coulomb_force.py`    | Inverse-square forces                             |
| `dzhanibekov.py`      | Intermediate-axis theorem (Dzhanibekov effect)    |
| `wave_propagation.py` | 2D wave propagation in a mass-spring lattice      |
| `gyroscope.py`        | Gyroscopic precession & nutation                  |
| `cube_vibration.py`   | 3D lattice, energy analysis, particle speed graph |

Run any script with:

```bash
python <example_file>.py
```

> **Note:** The example scripts assume `physics.py` and `visualization.py` are in the same folder as the script you’re running.

---

## Usage Guide

### Creating Systems

* **Particles:**
  Add particles with `sim.add_particle(mass, position, velocity)`

* **Springs:**
  Connect particles with `sim.add_spring(p1, p2, k, rest_length)`

* **Custom Forces:**
  Define your own force as a Python function and add with `sim.add_field(force_function)`

* **Energy Monitoring:**
  Query system energy with `sim.get_energy()`

### Visualization

* `visualization.py` provides a ready-to-use VPython interface for real-time 3D visualization and interaction.
* Customizable appearance through arguments (sphere size, color, spring thickness, etc).

---

## Extending Physics Sandbox

* **Custom Particle Properties:**
  Extend `Particle` objects with your own attributes (e.g., charge, volume).
* **Advanced Analytics:**
  Integrate with plotting libraries (e.g., matplotlib) to graph motion, energy, or other quantities.
* **New Visualizations:**
  Modify or expand `visualization.py` for new views or outputs.
* **Create New Examples:**
  Use existing demos as templates for your own physical scenarios.

---

## Contributing

Contributions, issues, and feature requests are welcome!
Feel free to open a pull request or an issue for suggestions, bug reports, or new demos.

---

## License

This project is licensed under the [MIT License](LICENSE).
