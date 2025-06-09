# =======================================================
# Imports
# =======================================================
from physics import *
from visualization import *
import numpy as np

# =======================================================
# Constants & Parameters
# =======================================================
DT = 0.00001  # Integrator time-step
K_COULOMB = 0.5  # Scaled Coulomb constant  (arbitrary units)

M1, C1 = 5.0, 10.0  # Mass & charge of central particle
M2, C2 = 1.0, -0.5  # Mass & charge of first orbiting particle
M3, C3 = 1.0, -0.5  # Mass & charge of second orbiting particle

# Initial positions & velocities
POS1 = np.zeros(3)
VEL1 = np.zeros(3)

POS2 = (3.0, -1.0, 0.0)
VEL2 = (-0.5, 1.0, 0.0)

POS3 = (3.0, 1.0, 0.0)
VEL3 = (-0.5, -1.0, 0.0)

# =======================================================
# Extend Particle class with 'charge' attribute
# =======================================================
setattr(Particle, "charge", 0)

# =======================================================
# Simulation Setup
# =======================================================
sim = Simulation(dt=DT)


def coulomb(particle):
    """
    Acceleration on `particle` due to Coulomb forces from all other
    particles in the simulation.  Uses inverse-square law in 3-D.
    """
    acc = np.zeros(3)
    for other in sim.particles:
        if other is particle:
            continue
        r = particle.pos - other.pos
        acc += (K_COULOMB * particle.charge * other.charge
                / (particle.mass * vnorm(r) ** 3)) * r
    return acc


sim.add_field(coulomb)

# =======================================================
# Particle Creation
# =======================================================
p1 = sim.add_particle(mass=M1, position=POS1, velocity=VEL1)
p1.charge = C1
p2 = sim.add_particle(mass=M2, position=POS2, velocity=VEL2)
p2.charge = C2
p3 = sim.add_particle(mass=M3, position=POS3, velocity=VEL3)
p3.charge = C3

# =======================================================
# Visualization
# =======================================================
visual_sim = Visualization(
    simulation=sim,
    resolution=(1900, 900),
    sphere_radius=1 / 14,
    sphere_color=color.white,
    spring_radius=1 / 50,
    spring_color=color.gray(luminance=0.7)
)

# Trails to visualise motion
attach_trail(visual_sim.particles[0], color=color.red, pps=100, retain=100)
attach_trail(visual_sim.particles[1], color=color.green, pps=100, retain=100)
attach_trail(visual_sim.particles[2], color=color.green, pps=100, retain=100)


# =======================================================
# Main Loop wrapped in play() + Run button
# =======================================================
def play():
    i = 0
    while True:
        if i % 250 == 0:  # Slow down rendering without missing physics steps
            visual_sim.update()
        sim.update()
        i += 1


# VPython button to start the simulation
button(bind=play, text="Run")

# Keep program alive when run as a script
input()
