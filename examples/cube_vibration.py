# =======================================================
# Imports
# =======================================================
from physics import *
from visualization import *
from itertools import product
from collections import deque
from vpython import vec, label, graph, gcurve, color, button

# =======================================================
# Global Parameters
# =======================================================
DT = 0.0003  # integrator time-step
MASS = 1.0  # mass of every particle
L = 1.0  # nearest-neighbour spacing
INIT_V = 3.0  # initial +x velocity of the “kick” particle
K_SPRING = 500.0  # spring stiffness
HISTORY_LEN = 1000  # max points in deque/plots
VIS_UPDATE = 10  # physics steps per redraw

# =======================================================
# Simulation Setup
# =======================================================
sim = Simulation(dt=DT, damping=True)

particle1 = None  # the particle we kick (+x)
particle2 = None  # the one directly opposite (–x)
# (we’ll use their x-velocities for plots)

# -------------------------------------------------------
# Create 3×3×3 cubic lattice centred at the origin
# -------------------------------------------------------
for coord in product((-1, 0, 1), repeat=3):
    if coord == (-1, 0, 0):
        particle1 = sim.add_particle(MASS, coord, (INIT_V, 0, 0))
    elif coord == (1, 0, 0):
        particle2 = sim.add_particle(MASS, coord)  # at rest
    else:
        sim.add_particle(MASS, coord)

# -------------------------------------------------------
# Connect particles whose separation ≤ √2 L (diagonal included)
# -------------------------------------------------------
for i, p1 in enumerate(sim.particles[:-1]):
    for p2 in sim.particles[i + 1:]:
        if vnorm2(p1.pos - p2.pos) <= 2 * L ** 2:
            sim.add_spring(p1, p2, K_SPRING)

# =======================================================
# Visualization
# =======================================================
visual_sim = Visualization(
    simulation=sim,
    resolution=(1900, 900),
    sphere_radius=1 / 14,
    sphere_color=color.blue,
    spring_radius=1 / 100,
    spring_color=color.gray(luminance=0.7)
)

time_label = label(pixel_pos=True, pos=vec(50, 50, 0))

# =======================================================
# Graphs & Data Buffers
# =======================================================
pot_data = deque(maxlen=HISTORY_LEN)
kin_data = deque(maxlen=HISTORY_LEN)
tot_data = deque(maxlen=HISTORY_LEN)
spd1_data = deque(maxlen=HISTORY_LEN)
spd2_data = deque(maxlen=HISTORY_LEN)

energy_graph = graph(title='Energies', xtitle='Time', ytitle='Energy')
kin_curve = gcurve(color=color.orange, label='Kinetic', graph=energy_graph)
pot_curve = gcurve(color=color.blue, label='Potential', graph=energy_graph)
tot_curve = gcurve(color=color.purple, label='Total', graph=energy_graph)

speed_graph = graph(title='Speeds', xtitle='Time', ytitle='Speed')
spd1_curve = gcurve(color=color.blue, label='Speed 1', graph=speed_graph)
spd2_curve = gcurve(color=color.orange, label='Speed 2', graph=speed_graph)


# =======================================================
# Main Loop wrapped in play() + Run button
# =======================================================
def play():
    step = 0
    while True:
        # -------- per-frame visual & logging --------
        if step % VIS_UPDATE == 0:
            visual_sim.update()
            t = sim.time

            # Energies
            kin, pot = sim.get_energy()
            tot = kin + pot
            kin_data.append((t, kin))
            pot_data.append((t, pot))
            tot_data.append((t, tot))
            kin_curve.data = list(kin_data)
            pot_curve.data = list(pot_data)
            tot_curve.data = list(tot_data)

            # Selected particle speeds (x-component)
            spd1_data.append((t, particle1.vel[0]))
            spd2_data.append((t, particle2.vel[0]))
            spd1_curve.data = list(spd1_data)
            spd2_curve.data = list(spd2_data)

            time_label.text = f'{t:.4f}'

        # -------- physics update --------
        sim.update()
        step += 1


# VPython button to start the simulation
button(bind=play, text="Run")

# Keep program alive when the script finishes (if run outside Jupyter)
input()
