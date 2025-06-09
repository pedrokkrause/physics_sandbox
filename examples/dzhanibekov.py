# =======================================================
# Imports
# =======================================================
from physics import *
from visualization import *

# =======================================================
# Simulation-wide Parameters
# =======================================================
DT = 0.00005  # time-step
D1 = 1.0  # ±x offset for light masses
D2 = 1.0  # ±y offset for heavy masses
M1 = 1.0  # mass of central & side particles
M2 = 2.0  # mass of upper & lower particles
K_SPRING = 1_000_000  # spring stiffness
V_Z = 10.0  # initial z-velocity of p4 (and –p5)
DV_XY = 0.001  # small initial x- & y-velocity components

# =======================================================
# Simulation Object & Particles
# =======================================================
sim = Simulation(dt=DT)

# Central particle
p1 = sim.add_particle(mass=M1, position=(0.0, 0.0, 0.0))

# Light side particles (left & right)
p2 = sim.add_particle(mass=M1, position=(D1, 0.0, 0.0))
p3 = sim.add_particle(mass=M1, position=(-D1, 0.0, 0.0))

# Heavy top & bottom particles
p4 = sim.add_particle(
    mass=M2,
    position=(0.0, D2, 0.0),
    velocity=(DV_XY, DV_XY, V_Z)
)
p5 = sim.add_particle(
    mass=M2,
    position=(0.0, -D2, 0.0),
    velocity=(-DV_XY, -DV_XY, -V_Z)
)

# =======================================================
# Spring Network
# =======================================================
# Springs from the centre
sim.add_spring(p1, p2, K_SPRING)
sim.add_spring(p1, p3, K_SPRING)
sim.add_spring(p1, p4, K_SPRING)
sim.add_spring(p1, p5, K_SPRING)

# Springs connecting sides to tops/bottoms
sim.add_spring(p2, p4, K_SPRING)
sim.add_spring(p3, p4, K_SPRING)
sim.add_spring(p2, p5, K_SPRING)
sim.add_spring(p3, p5, K_SPRING)

# Remaining edges
sim.add_spring(p2, p3, K_SPRING)
sim.add_spring(p4, p5, K_SPRING)

# =======================================================
# Visualization
# =======================================================
visual_sim = Visualization(
    simulation=sim,
    resolution=(1900, 900),
    sphere_radius=1 / 14,
    sphere_color=color.blue,
    spring_radius=1 / 50,
    spring_color=color.gray(luminance=0.7)
)

ground = box(
    pos=vec(0, -2 * D2, 0),
    axis=vec(1, 0, 0),
    size=vec(D2 * 2, 0.1, D2 * 2)
)

# Trail for the first side particle (p2)
attach_trail(visual_sim.particles[1], color=color.green, pps=30, retain=10)


# =======================================================
# Main Loop wrapped in play() + Run button
# =======================================================
def play():
    i = 0
    while True:
        if i % 250 == 0:
            visual_sim.update()
        sim.update()
        i += 1


# VPython button to start the simulation
play_button = button(bind=play, text="Run")

# Keep the program alive (optional end-of-file pause)
input()
