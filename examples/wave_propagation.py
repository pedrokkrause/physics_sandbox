# =======================================================
# Imports
# =======================================================
from physics import *
from visualization import *
import numpy as np

# =======================================================
# Global Parameters
# =======================================================
DT = 0.005  # Integrator time-step
NX = 30  # particles along X
NY = 30  # particles along Y
LX = 3.0  # physical width  (physics-x)
LY = 3.0  # physical height (physics-y)
K = 100  # spring stiffness
MASS = 1.0  # particle mass
DRIVE_PERIOD = 1.0  # oscillation period for centre node

# Derived spacings
DX = LX / NX
DY = LY / NY

# =======================================================
# Simulation Setup
# =======================================================
sim = Simulation(dt=DT, damping=False)


# Helper to flatten (i, j) → list index
def idx(i: int, j: int) -> int:
    """Row-major index into sim.particles for grid coordinates (i, j)."""
    return NY * i + j


# -------------------------------------------------------
# Particle Grid
# -------------------------------------------------------
for i in range(NX):
    for j in range(NY):
        # Clamp boundary: outer frame is fixed
        movable = not (i == 0 or j == 0 or i == NX - 1 or j == NY - 1)
        sim.add_particle(
            mass=MASS,
            position=(-LX / 2 + i * DX,  # centre the grid at origin
                      -LY / 2 + j * DY,
                      0.0),
            movable=movable
        )

# -------------------------------------------------------
# Springs (horizontal & vertical nearest neighbours)
# -------------------------------------------------------
for i in range(NX - 1):
    for j in range(NY - 1):
        p1 = sim.particles[idx(i, j)]
        p2 = sim.particles[idx(i + 1, j)]  # right neighbour
        p3 = sim.particles[idx(i, j + 1)]  # top neighbour
        sim.add_spring(p1, p2, K, DX * 0.1)
        sim.add_spring(p1, p3, K, DY * 0.1)

# Centre particle – driven vertically
middle = sim.particles[idx(NX//2, NY//2)]

# =======================================================
# Visualization
# =======================================================
visual_sim = Visualization(
    simulation=sim,
    resolution=(1900, 900),
    sphere_radius= 0,
    sphere_color=color.blue,
    spring_radius=DX / 2,
    spring_color=color.gray(luminance=0.7)
)


# =======================================================
# Main Loop wrapped in play() + Run button
# =======================================================
def play():
    i = 0
    while True:
        # Harmonic driving of the centre node (z-direction)
        middle.pos[2] = 0.1 * sin(2 * pi / DRIVE_PERIOD * sim.time)

        # Throttle rendering to every second physics step
        if i % 2 == 0:
            visual_sim.update()

        sim.update()
        i += 1


# VPython button to start the simulation
button(bind=play, text="Run")

# Keep program alive when the script finishes
input()
