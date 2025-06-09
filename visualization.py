from vpython import *
from math import cbrt

# Convert a (x,y,z) vector to the (x,z,y) VPython vector
pvec = lambda v: vec(v[0],v[2],v[1])

class Visualization:
    def __init__(self, simulation, resolution, sphere_color, sphere_radius, spring_color, spring_radius):
        canvas(width=resolution[0], height=resolution[1])

        self.simulation = simulation
        self.particles = []
        self.springs = []

        for particle in simulation.particles:
            p = sphere(color=sphere_color, radius=sphere_radius*cbrt(particle.mass), pos=pvec(particle.pos))
            self.particles.append(p)

        for spring in simulation.springs:
            axis = spring.p2.pos - spring.p1.pos
            pos = spring.p1.pos
            s = cylinder(pos=pvec(pos), axis=pvec(axis), radius=spring_radius, color=spring_color)
            self.springs.append(s)

    def update(self):
        for vp,sp in zip(self.particles, self.simulation.particles):
            vp.pos = pvec(sp.pos)

        for vs,ss in zip(self.springs, self.simulation.springs):
            dif = ss.p2.pos - ss.p1.pos
            vs.pos = pvec(ss.p1.pos)
            vs.axis = pvec(dif)
