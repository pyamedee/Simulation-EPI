# -*- coding:Utf-8 -*-

import pyglet
from bouh import calculate_new_vectors
import numpy as np
from random import randrange
from math import sqrt


class App(pyglet.window.Window):

    def __init__(self, n, array, fps, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        self.fps = fps
        self.dt = 1. / self.fps

        self.batch = pyglet.graphics.Batch()

        self.n = n
        self.entities = np.empty(self.n, dtype=np.object)

        self.array = array
        self.go = False
        self.draw = False

        self.fps_display = pyglet.clock.ClockDisplay()

        self.entity_size = 6

        self.collision_distance = self.entity_size * 2
        self.squared_cd = self.collision_distance ** 2

        self.bg_image = pyglet.image.load('bg.jpg')

        self.sprite_image = pyglet.image.load('circle.png')
        self.sprite_image.anchor_x = self.sprite_image.width // 2
        self.sprite_image.anchor_y = self.sprite_image.width // 2
        self.init_sprites()

        self.clock = pyglet.clock.Clock()
        pyglet.clock.schedule_interval(self.update, self.dt)

    def init_sprites(self):
        scale = self.entity_size / (self.sprite_image.width / 2)

        for i in range(self.n):
            self.entities[i] = pyglet.sprite.Sprite(self.sprite_image,
                                                    x=self.array[i, 0],
                                                    y=self.array[i, 1],
                                                    batch=self.batch)
            self.entities[i].scale = scale

    def on_draw(self):

        if self.draw:
            self.bg_image.blit(0, 0)
            self.batch.draw()
        # self.clock.tick()
        # try:
        #     self.set_caption(str(self.clock.get_fps()))
        # except ZeroDivisionError:
        #     pass

    def on_key_press(self, symbol, *args, **kwargs):
        super(App, self).on_key_press(symbol, *args, **kwargs)
        if symbol == pyglet.window.key.SPACE:
            if self.width > 900:
                self.go ^= True
                self.draw = self.go
        elif symbol == pyglet.window.key.F2:
            self.set_fullscreen(True, width=1920, height=1080)
            for _ in range(100):
                self.go = True
                self.update()
                self.go = False
        elif symbol == pyglet.window.key.F1:
            self.set_fullscreen(False, width=200, height=100)
            self.draw = False
            self.go = False

    def update(self, *_, **__):
        if self.go:
            calculate_new_vectors(self.array, self.collision_distance, self.squared_cd)
            for i, entity in enumerate(self.entities):
                pos = self.array[i, :2]
                if pos[1] > self.height - self.entity_size:
                    self.array[i, 3] = -np.abs(self.array[i, 3])
                if pos[1] < self.entity_size:
                    self.array[i, 3] = np.abs(self.array[i, 3])
                if pos[0] > self.width - self.entity_size:
                    self.array[i, 2] = -np.abs(self.array[i, 2])
                if pos[0] < self.entity_size:
                    self.array[i, 2] = np.abs(self.array[i, 2])
                entity.x, entity.y = self.array[i, :2]
            self.array[:, :2] += self.array[:, 2:] / 30


if __name__ == '__main__':
    w = 1920
    h = 1080
    ax = np.arange(0, w, 8 ** 2)
    ay = np.arange(0, h, 8 ** 2)
    a = np.empty((ax.shape[0] * ay.shape[0], 4), dtype=np.float64)
    i = 0
    for x in ax:
        for y in ay:
            vx = randrange(-50, 51)
            a[i] = x, y, vx, sqrt(2500 - vx ** 2)
            i += 1

    n = ax.shape[0] * ay.shape[0]

    # n = 2
    # a = np.array((
    #     (45, 350, 50, 0),
    #     (60, 450, 40, -30)
    #               ), dtype=np.float64)

    app = App(n, a, 60, width=200, height=100, fullscreen=False)
    pyglet.app.run()
