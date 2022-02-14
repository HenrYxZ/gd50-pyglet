import random

import numpy as np
import pyglet
import time


# Local modules
from physics import State


MIN_V0X = 5
MAX_V0X = 30
MIN_V0Y = 5
MAX_V0Y = 30


def random_velocity(min_v, max_v):
    v = random.uniform(min_v, max_v)
    if random.random() < 0.5:
        v *= -1
    return v


class ParticleSettings:
    """
    Settings for a particle system

    Attributes:
        start_color(ndarray): Color the particles have at the beginning
        end_color(ndarray): Color at the end of the lifespan RGB in 0-255
        start_opacity(float): Opacity the particles have at the beginning
        end_opacity(float): Opacity value at the end of the lifespan
        min_lifespan(float): Minimum life duration in seconds
        max_lifespan(float): Maximum life duration in seconds
    """
    def __init__(
        self, start_color, end_color, start_opacity, end_opacity, min_lifespan,
        max_lifespan
    ):
        self.start_color = start_color
        self.end_color = end_color
        self.start_opacity = start_opacity
        self.end_opacity = end_opacity
        self.min_lifespan = min_lifespan
        self.max_lifespan = max_lifespan


class Particle:
    """
    Particle that represents a unit of a particle system and displays a
    sprite.

    Attributes:
        sprite(Sprite): Sprite that represents the particle
        state(State): Object that stores the physical state
        creation_time(float): Time when the particle was created
        settings(ParticleSettings): A collection of settings for a particle
        dead(bool): If this particle reached its lifespan
        lifespan(float): Life duration of the particle in seconds
    """
    def __init__(self, sprite, state, creation_time, settings):
        self.sprite = sprite
        self.state = state
        self.creation_time = creation_time
        self.settings = settings
        self.dead = False
        self.lifespan = random.uniform(
            settings.min_lifespan, settings.max_lifespan
        )
        self.sprite.color = settings.start_color

    def update(self, dt, current_time, forces):
        """
        Update if the particle is dead, its physical state and color

        Args:
            dt(float): Seconds since the last update
            current_time(float): Current time in seconds
            forces(list[float]): List of forces acting on the particle
        """
        # Set dead particles
        elapsed_time = current_time - self.creation_time
        if elapsed_time > self.lifespan:
            self.dead = True
            return
        # Update physical state
        self.state.pos += self.state.v * dt
        for force in forces:
            a = force / self.state.m
            self.state.v += a * dt
            self.sprite.x = self.state.pos[0]
            self.sprite.y = self.state.pos[1]
        # Update color
        t = elapsed_time / self.lifespan
        self.sprite.color = (
            (1 - t) * self.settings.start_color +
            t * self.settings.end_color
        )
        self.sprite.opacity = (
            (1 - t) * self.settings.start_opacity +
            t * self.settings.end_opacity
        )


class ParticleSystem:
    """
    System that can emit particles.

    Attributes:
        img(Image): Image to use for each particle
        max_count(int): Maximum number of particles allowed in the system
        forces(list[float]): Forces that will affect the system in N
        particles(list[Particle]): Particles that belong to the system
        get_v0x(func): A function that returns a new initial velocity in
            the x-axis for a particle when called
        get_v0y(func): A function that returns a new initial velocity in
            the y-axis for a particle when called
        batch(Batch): A batch object that groups sprites in a single draw call
    """
    def __init__(self, img, max_count):
        self.img = img
        self.max_count = max_count
        self.forces = []
        self.particles = []
        # default initial velocities are uniformly random in a range in every
        # direction
        self.get_v0x = lambda: random_velocity(MIN_V0X, MAX_V0X)
        self.get_v0y = lambda: random_velocity(MIN_V0Y, MAX_V0Y)
        self.batch = pyglet.graphics.Batch()

    def emit(self, x, y, num, settings):
        """
        Create the given number of particles.

        Args:
            x(float): Position of the emission in the x-axis
            y(float): Position of the emission in the y-axis
            num(int): Number of particles to create
            settings(ParticleSettings): Settings for the particles

        Returns:
            list[Particles]: The new particles created
        """
        creation_time = time.time()
        new_particles = []
        for i in range(num):
            # if limit was reached break
            if len(self.particles) == self.max_count:
                break
            sprite = pyglet.sprite.Sprite(self.img, x, y, batch=self.batch)
            pos = np.array([sprite.x, sprite.y])
            v = np.array([self.get_v0x(), self.get_v0y()])
            m = 1
            state = State(pos, v, 0, m)
            particle = Particle(sprite, state, creation_time, settings)
            new_particles.append(particle)
        # add new particles to the list
        self.particles.extend(new_particles)
        return new_particles

    def update(self, dt):
        """
        Update the system after dt seconds have passed

        Args:
            dt(float): Amount of seconds since the last update
        """
        current_time = time.time()
        for particle in self.particles:
            particle.update(dt, current_time, self.forces)
        # Remove dead particles
        for particle in filter(lambda l: l.dead, self.particles):
            self.particles.remove(particle)
            particle.sprite.delete()

    def draw(self):
        self.batch.draw()
