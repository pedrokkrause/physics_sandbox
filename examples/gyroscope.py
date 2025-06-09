# =============================
# Imports
# =============================
from physics import *
from visualization import *
import numpy as np

# =============================
# Constants and Parameters
# =============================
DT = 0.00001
K = 1_000_000
V_ROT = 30.0
MASS = 1.0
L1 = 3.0
L2 = 1.0
G = 9.8

# =============================
# Simulation Setup
# =============================
sim = Simulation(dt=DT)


def gravity(particle):
    return np.array([0.0, 0.0, -G])


sim.add_field(gravity)

# =============================
# Particle Creation
# =============================
p1 = sim.add_particle(
    mass=MASS,
    position=(0.0, 0.0, 0.0),
    movable=False
)
p2 = sim.add_particle(
    mass=MASS,
    position=(L1, 0.0, 0.0)
)
p3 = sim.add_particle(
    mass=MASS,
    position=(L1, L2, 0.0),
    velocity=(0.0, 0.0, V_ROT)
)
p4 = sim.add_particle(
    mass=MASS,
    position=(L1, 0.0, L2),
    velocity=(0.0, -V_ROT, 0.0)
)
p5 = sim.add_particle(
    mass=MASS,
    position=(L1, -L2, 0.0),
    velocity=(0.0, 0.0, -V_ROT)
)
p6 = sim.add_particle(
    mass=MASS,
    position=(L1, 0.0, -L2),
    velocity=(0.0, V_ROT, 0.0)
)

# =============================
# Spring Connections
# =============================
# Principal axis
sim.add_spring(p1, p2, K)

# Around center
sim.add_spring(p2, p3, K)
sim.add_spring(p2, p4, K)
sim.add_spring(p2, p5, K)
sim.add_spring(p2, p6, K)

# Outer ring
sim.add_spring(p3, p4, K)
sim.add_spring(p4, p5, K)
sim.add_spring(p5, p6, K)
sim.add_spring(p6, p3, K)

# Ring to origin
sim.add_spring(p1, p3, K)
sim.add_spring(p1, p4, K)
sim.add_spring(p1, p5, K)
sim.add_spring(p1, p6, K)

# =============================
# Visualization Setup
# =============================
visual_sim = Visualization(
    simulation=sim,
    resolution=(1900, 900),
    sphere_radius=1 / 14,
    sphere_color=color.blue,
    spring_radius=1 / 50,
    spring_color=color.gray(luminance=0.7)
)
attach_trail(visual_sim.particles[1], color=color.green, pps=10, retain=1000)

ground = box(
    pos=vector(0, -1.1 * L1, 0),
    axis=vector(1, 0, 0),
    size=vector(L1 * 2, 0.5, L1 * 2)
)

# =============================
# Analytical Prediction (Gyro)
# =============================
theta = 0
theta1 = 0
phi = 0
phi1 = 0

M = 5 * MASS
I3 = 4 * MASS * L2 ** 2
I1 = I3 / 2 + M * L1 ** 2
w = V_ROT / L2


def update_gyro():
    global theta, theta1, phi, phi1, sim, w, M

    # ---------- second derivatives ----------
    theta2 = phi1/cos(phi) * (2 * theta1 * sin(phi) - I3/I1 * w)
    phi2 = theta1*cos(phi) * (-theta1*sin(phi) + (I3/I1) * w) - M*G*L1/I1 * cos(phi)

    # ---------- integrate ----------
    phi1 += phi2 * sim.dt
    phi += phi1 * sim.dt
    theta1 += theta2 * sim.dt
    theta += theta1 * sim.dt

    # ---------- Cartesian position ----------
    return (
        L1 * cos(phi) * cos(theta),
        L1 * sin(phi),
        L1 * cos(phi) * sin(theta)
    )


prediction = sphere(
    color=color.red,
    radius=1 / 14,
    pos=vec(L1 * np.cos(phi) * np.cos(theta), L1 * np.sin(phi), L1 * np.cos(phi) * np.sin(theta))
)
attach_trail(prediction, color=color.orange, pps=10, retain=1000)


# =============================
# Helper Functions
# =============================
def center_of_mass():
    total_pos = np.zeros(3)
    total_vel = np.zeros(3)
    for particle in (p2, p3, p4, p5, p6):
        total_pos += particle.pos * particle.mass
        total_vel += particle.vel * particle.mass
    return total_pos / M


CM = center_of_mass()
CM_visual = sphere(
    color=color.magenta,
    radius=1 / 14,
    pos=pvec(CM)
)

visual_sim.particles[1].radius = 1 / 50


# =============================
# Main Loop & UI
# =============================
def play():
    i = 0
    while True:
        if i % 250 == 0:
            visual_sim.update()
            prediction.pos = vec(*update_gyro())
            CM = center_of_mass()
            CM_visual.pos = pvec(CM)
        else:
            update_gyro()
        sim.update()
        i += 1


play_button = button(bind=play, text="Run")
input()
