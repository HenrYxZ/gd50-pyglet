import pyglet

from pyglet.gl import GL_POINTS
from random import randint, uniform


window = pyglet.window.Window(width=960, height=540)
fps_display = pyglet.window.FPSDisplay(window=window)
label = pyglet.text.Label(x=10, y=window.height-40)
batch = pyglet.graphics.Batch()


particles = []


class Particle:
    def __init__(self, x, y, vel_x, vel_y, vlist, life):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.vlist = vlist
        self.life = life


def update_particles(_):
    for particle in particles:

        particle.life -= 1
        if particle.life < 0:
            particle.vlist.delete()
            particles.remove(particle)

        particle.x += particle.vel_x
        particle.y += particle.vel_y
        particle.vel_x *= 0.95

        # Update the vertex list in-place, rather than re-creating it:
        particle.vlist.vertices[:] = particle.x, particle.y

    # Create some new particles
    for _ in range(10):
        x = 480
        y = 500
        vel_x = uniform(-5, 5)
        vel_y = uniform(-2, -3)
        color = randint(0, 255), randint(0, 255), randint(0, 255)
        vlist = batch.add(1, GL_POINTS, None, ('v2f', (x, y)), ('c3B', color))
        life = randint(50, 150)
        particles.append(Particle(x, y, vel_x, vel_y, vlist, life))


@window.event
def on_draw():
    window.clear()
    fps_display.draw()
    label.text = "Number of active particles: {}".format(len(particles))
    label.draw()
    batch.draw()


pyglet.gl.glPointSize(2)
pyglet.clock.schedule_interval(update_particles, 1/60)
pyglet.app.run()
