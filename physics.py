import numpy as np
from math import sqrt

# Calculates the norm of a vector or the norm squared
vnorm = lambda x: sqrt(x.dot(x))
vnorm2 = lambda x: x.dot(x)

class Particle:
    def __init__(self, mass, position, velocity=None, movable=True, properties=None):
        self.mass = mass
        self.pos = np.asarray(position, float)
        self.vel = (np.zeros(3) if velocity is None else np.asarray(velocity, float))
        self.acc = np.zeros(3)
        self.movable = movable

        if callable(properties):  # factory style
            properties(self)
        elif properties is not None:  # dict style
            for k, v in properties.items():
                setattr(self, k, v)
        else:  # default
            self.type = None

    def update(self, dt):
        self.vel = self.vel + self.acc * dt
        self.pos = self.pos + self.vel * dt

    def energy(self):
        return 0.5 * self.mass * vnorm2(self.vel)

# Defines a Hooke's law force between two particles
class Spring:
    def __init__(self, p1, p2, k, L0=None):
        self.p1 = p1
        self.p2 = p2
        self.k = k
        if L0 is None:
            self.L0 = self.length()
        else:
            self.L0 = L0

    def length(self):
        return vnorm(self.p2.pos - self.p1.pos)

    def axis(self):
        return self.p2.pos - self.p1.pos

    def force(self, axis):
        return self.k * (1 - self.L0 / vnorm(axis)) * axis

    def damping_force(self, axis, b):
        n = axis / vnorm(axis)
        v_rel = self.p2.vel - self.p1.vel
        Ldot = v_rel.dot(n)
        F = b*Ldot * n
        return F

    def energy(self):
        return 0.5 * self.k * abs(vnorm(self.p2.pos - self.p1.pos)-self.L0)**2

class Simulation:
    def __init__(self, dt, damping=False, dissipation_coefficient=0.5):
        self.dt = dt
        self.particles = []
        self.movable_particles = []
        self.springs = []
        self.fields = []
        self.time = 0.0
        self.damping = damping
        self.dissipation_coefficient = dissipation_coefficient

    def add_particle(self, mass, position, velocity=None, movable=True, properties=None):
        if velocity is None:
            velocity = np.zeros(3)
        particle = Particle(mass, position, velocity, movable, properties)
        self.particles.append(particle)
        if movable:
            self.movable_particles.append(particle)
        return particle

    def add_spring(self, p1, p2, k, L0=None):
        spring = Spring(p1, p2, k, L0)
        self.springs.append(spring)
        return spring

    def add_field(self, function):
        self.fields.append(function)

    def update_particle(self, particle):
        for field in self.fields:
            particle.acc += field(particle)

        particle.update(self.dt)
        particle.acc[:] = 0.0

    def update_spring(self, spring):
        spring_axis = spring.axis()
        force = spring.force(spring_axis)
        if self.damping:
            drag = spring.damping_force(spring_axis, self.dissipation_coefficient)
            spring.p1.acc += (force + drag) / spring.p1.mass
            spring.p2.acc -= (force + drag) / spring.p2.mass
        else:
            spring.p1.acc += force / spring.p1.mass
            spring.p2.acc -= force / spring.p2.mass

    def update(self):
        self.time += self.dt
        for spring in self.springs:
            self.update_spring(spring)
        for particle in self.movable_particles:
            self.update_particle(particle)

    def get_energy(self):
        kinetic = sum(p.energy() for p in self.particles)
        potential = sum(s.energy() for s in self.springs)
        return (kinetic, potential)