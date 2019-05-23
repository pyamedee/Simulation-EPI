# -*- coding:Utf-8 -*-

import pyglet
from physic_utils import calculate_new_vectors
import numpy as np
import numpy.random as rd
from random import randrange
from math import sqrt
import math

# x 307
# y 186
# x2 1607
# y2 878


class Anim(pyglet.sprite.Sprite):
    def __init__(self, vx, vy, *args, **kwargs):
        super(Anim, self).__init__(*args, **kwargs)
        self.v = np.array((vx, vy), dtype=np.float)

    def update_(self):
        v = self.v / 30
        self.x += v[0]
        self.y += v[1]


class Particle(pyglet.sprite.Sprite):
    def __init__(self, index, *args, **kwargs):
        super(Particle, self).__init__(*args, **kwargs)
        self.index = index
        self.disabled = False
        self.non_water = True
        self.is_dihydrogen = False
        self.is_oxygen = False

    def update_(self, array):
        a_ = array[self.index]
        self.x = a_[0]
        self.y = a_[1]

    def __repr__(self):
        return 'x={}, y={}'.format(self.x, self.y)

#
# class Hydrogen(Particle):
#     def update_(self, array):
#         a_ = array[self.index]
#         a_[3] += 1
#         vv = a_[2:]
#         a_[2:] = vv / sqrt(np.dot(vv, vv)) * 50
#         self.x = a_[0]
#         self.y = a_[1]



class Block:
    def __init__(self, sx, sy, x, y, x2, y2):
        height = (y2 - y) * sy
        width = (x2 - x) * sx
        self.bottom = y * sy
        self.top = y * sy + height
        self.left = x * sx
        self.right = x * sx + width

    def collide(self, point):
        return (self.left < point[0] < self.right) and (self.bottom < point[1] < self.top)


class App(pyglet.window.Window):

    def __init__(self, n, array, fps, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        self.fps = fps
        self.dt = 1. / self.fps

        self.r_height = 900
        self.r_width = 1600

        self.sun = False

        self.scale_x = 2
        self.scale_y = 1.5

        self.batch = pyglet.graphics.Batch()

        self.n = n
        self.entities = np.empty(self.n * 2, dtype=np.object)
        self.enabled_entities = np.zeros(self.n * 2, dtype=np.bool)
        self.enabled_entities[:self.n] = 1

        self.array = array
        self.go = False
        self.draw = False

        self.fps_display = pyglet.clock.ClockDisplay()

        self.entity_size = 8

        self.cobalt = Block(self.scale_x, self.scale_y,
            150 - self.entity_size / self.scale_x,
            100 - self.entity_size / self.scale_y,
            300 - self.entity_size / self.scale_x,
            500 + self.entity_size / self.scale_y)
        self.right_block = Block(self.scale_x, self.scale_y,
            300,
            100 - self.entity_size / self.scale_y,
            650 + self.entity_size / self.scale_x,
            500 + self.entity_size / self.scale_y)
        self.zinc = Block(self.scale_x, self.scale_y, 550, 100, 650, 500)

        self.collision_distance = self.entity_size * 2
        self.squared_cd = self.collision_distance ** 2

        self.bg_image = pyglet.image.load('bg.jpg')
        self.box_image = pyglet.image.load('box3.png')
        bg = pyglet.graphics.OrderedGroup(0)
        self.box_sprite = pyglet.sprite.Sprite(self.box_image,
                                               x=150 * self.scale_x,
                                               y=100 * self.scale_y,
                                               batch=self.batch,
                                               group=bg)
        # self.box_sprite.scale_x = self.scale_x
        # self.box_sprite.scale_y = self.scale_y

        self.blue_image = pyglet.image.load('circle_blue.png')
        self.blue_image.anchor_x = self.blue_image.width // 2
        self.blue_image.anchor_y = self.blue_image.width // 2

        self.red_image = pyglet.image.load('circle_red.png')
        self.red_image.anchor_x = self.red_image.width // 2
        self.red_image.anchor_y = self.red_image.width // 2

        self.white_image = pyglet.image.load('circle_white.png')
        self.white_image.anchor_x = self.white_image.width // 2
        self.white_image.anchor_y = self.white_image.width // 2

        self.plus_image = pyglet.image.load('circle_plus.png')
        self.plus_image.anchor_x = self.plus_image.width // 2
        self.plus_image.anchor_y = self.plus_image.width // 2

        self.minus_image = pyglet.image.load('circle_minus.png')
        self.minus_image.anchor_x = self.minus_image.width // 2
        self.minus_image.anchor_y = self.minus_image.width // 2

        self.red2_image = pyglet.image.load('circle_red2.png')
        self.red2_image.anchor_x = self.red2_image.width // 2
        self.red2_image.anchor_y = self.red2_image.width // 2

        self.fg = pyglet.graphics.OrderedGroup(1)
        self.scale = self.entity_size / (self.blue_image.width / 2)
        self.init_sprites()

        self.entities_for_animation = np.empty((self.n, 4), dtype=np.object)
        self.centers = np.empty((self.n, 4), dtype=np.float)
        self.enabled_entities_for_animation = set()
        self.doing_fusion = dict()

        self.clock = pyglet.clock.Clock()
        pyglet.clock.schedule_interval(self.update, self.dt)

    def create_dioxygen(self, enta, entb):
        contact_point = (self.array[enta, :2] + self.array[entb, :2]) / 2

        self.entities[enta].is_oxygen = False
        self.entities[enta].is_dihydrogen = True
        self.entities[enta].image = self.red2_image

        self.enabled_entities[entb] = False
        self.entities[entb] = None

        self.array[enta, :2] = contact_point

    def add_dihydrogen(self, ani):
        i = ani + self.n
        self.enabled_entities[i] = True

        self.array[i, :2] = self.centers[ani, :2].copy()
        self.array[i, 2:] = 50., 0.
        self.entities[i] = Particle(i, self.white_image,
                                    x=self.array[i, 0],
                                    y=self.array[i, 1],
                                    batch=self.batch,
                                    group=self.fg)
        self.entities[i].non_water = True
        self.entities[i].scale = self.scale
        self.entities[i].is_dihydrogen = True

    def add_entity_for_animation(self, i, center):
        self.centers[i, :2] = center
        if center[1] > self.cobalt.top - 50 * self.scale_y:
            base = (45, -20)
        elif center[1] < self.cobalt.bottom + 50 * self.scale_y:
            base = (45, 20)
        else:
            base = (50, 0)

        self.centers[i, 2:] = base

        v = np.array((base,) * 4, dtype=np.float)
        v += rd.randint(-60, 50, (4, 2)) / 10
        # v = v / sqrt(np.dot(v, v)) * 50

        for n in range(2):
            v[n] = v[n] / sqrt(np.dot(v[n], v[n])) * 50
            self.entities_for_animation[i, n] = Anim(v[n, 0], v[n, 1], self.minus_image,
                                                     x=center[0],
                                                     y=center[1],
                                                     batch=self.batch,
                                                     group=self.fg)
        for n in range(2, 4):
            v[n] = v[n] / sqrt(np.dot(v[n], v[n])) * 50
            self.entities_for_animation[i, n] = Anim(v[n, 0], v[n, 1], self.plus_image,
                                                     x=center[0],
                                                     y=center[1],
                                                     batch=self.batch,
                                                     group=self.fg)

        for entity in self.entities_for_animation[i]:
            entity.scale = self.scale * 0.7
        self.enabled_entities_for_animation.add(i)

    def init_sprites(self):
        for i in range(self.n):
            self.entities[i] = Particle(i, self.blue_image,
                                        x=self.array[i, 0],
                                        y=self.array[i, 1],
                                        batch=self.batch,
                                        group=self.fg)
            self.entities[i].scale = self.scale

    def on_draw(self):

        if self.draw:
            self.bg_image.blit(0, 0)
            #self.box_image.blit(150, 100)
            self.batch.draw()
        # self.clock.tick()
        # try:
        #     self.set_caption(str(self.clock.get_fps()))
        # except ZeroDivisionError:
        #     pass

    def on_key_press(self, symbol, *args, **kwargs):
        super(App, self).on_key_press(symbol, *args, **kwargs)
        if symbol == pyglet.window.key.SPACE:
            if self.width > 500:
                self.go ^= True
                self.draw = self.go
        elif symbol == pyglet.window.key.F2:
            self.go = True
            for _ in range(500):
                self.update()
            self.go = False
            print('\n\nPrêt au démarrage,\nF3 : Plein écran\nSPACE : draw\nF4 : changement de l\'attr "non_water".')
        elif symbol == pyglet.window.key.F1:
            self.set_fullscreen(False, width=200, height=100)
            self.draw = False
            self.go = False
        elif symbol == pyglet.window.key.F4:
            if not self.sun:
                self.sun = True
                for i_, entity in enumerate(self.entities):
                    if self.enabled_entities[i_]:
                        entity.non_water = False
        elif symbol == pyglet.window.key.F3:
            self.set_fullscreen(True, width=1600, height=900)

    def fusion(self, index):
        center_pos = self.centers[index, :2]
        for ent in self.entities_for_animation[index]:
            pvv = np.array((ent.x, ent.y))
            ent.v = center_pos - pvv
        self.doing_fusion[index] = 1

    def update(self, *_, **__):
        if self.go:
            pairs = calculate_new_vectors(self.array, self.collision_distance, self.squared_cd, self.enabled_entities)
            for enta, entb in pairs.items():
                try:
                    if self.entities[enta].is_oxygen and self.entities[entb].is_oxygen:
                        self.create_dioxygen(enta, entb)
                except AttributeError:
                    print(0)
            for i, entity in enumerate(self.entities):
                pos = self.array[i, :2]
                if self.enabled_entities[i]:
                    if entity.is_dihydrogen and not self.zinc.collide(pos):
                        self.array[i, 3] += 1
                        vv = self.array[i, 2:]
                        vv[:] = vv / sqrt(np.dot(vv, vv)) * 50

                    if pos[1] > self.r_height - self.entity_size:
                        if not entity.is_dihydrogen:
                            self.array[i, 3] = -np.abs(self.array[i, 3])
                        elif pos[1] > self.r_height + self.entity_size:
                            self.enabled_entities[i] = False
                            self.entities[i] = None
                    if pos[1] < self.entity_size:
                        self.array[i, 3] = np.abs(self.array[i, 3])
                    if pos[0] > self.r_width - self.entity_size:
                        self.array[i, 2] = -np.abs(self.array[i, 2])
                    if pos[0] < self.entity_size:
                        self.array[i, 2] = np.abs(self.array[i, 2])

                    if self.cobalt.collide(pos):
                        if not entity.non_water:
                            entity.non_water = True
                            entity.image = self.red_image
                            entity.is_oxygen = True
                            self.add_entity_for_animation(i, pos)

                        if pos[1] > self.cobalt.top - self.entity_size:
                            self.array[i, 3] = np.abs(self.array[i, 3])
                        elif pos[1] < self.cobalt.bottom + self.entity_size:
                            self.array[i, 3] = -np.abs(self.array[i, 3])
                        if pos[0] < self.cobalt.left + self.entity_size:
                            self.array[i, 2] = -np.abs(self.array[i, 2])

                    elif self.right_block.collide(pos):
                        if pos[1] > self.right_block.top - self.entity_size:
                            self.array[i, 3] = np.abs(self.array[i, 3])
                        elif pos[1] < self.right_block.bottom + self.entity_size:
                            self.array[i, 3] = -np.abs(self.array[i, 3])
                        if pos[0] > self.right_block.right - self.entity_size:
                            self.array[i, 2] = np.abs(self.array[i, 2])
                        elif pos[0] < self.right_block.left + self.entity_size:
                            self.array[i, 2] = -np.abs(self.array[i, 2])
                    entity.update_(self.array)
                    self.array[i, :2] += self.array[i, 2:] / 30

            toremove = set()
            for ani in self.enabled_entities_for_animation:
                anent = self.entities_for_animation[ani]
                for ent in anent:
                    ent.update_()
                if self.doing_fusion.get(ani, False):
                    self.doing_fusion[ani] += 1
                    if self.doing_fusion[ani] == 30:
                        toremove.add(ani)
                        self.add_dihydrogen(ani)
                elif self.zinc.collide(self.centers[ani, :2]):
                    self.fusion(ani)
                else:
                    self.centers[ani, :2] += self.centers[ani, 2:] / 30
            self.enabled_entities_for_animation ^= toremove
            for index in toremove:
                self.entities_for_animation[index, :] = None


if __name__ == '__main__':
    w = 800
    h = 600
    ax1 = np.arange(0, 100, 8 ** 1.5)
    ax2 = np.arange(1500, 1600, 8 ** 1.5)
    ax = np.concatenate((ax1, ax2))
    ay = np.arange(0, h, 8 ** 1.5)
    a = np.empty((ax.shape[0] * ay.shape[0], 4), dtype=np.float64)
    i = 0
    for x in ax:
        for y in ay:
            vx = randrange(-50, 51)
            a[i] = x, y, vx, sqrt(2500 - vx ** 2)
            i += 1

    n = ax.shape[0] * ay.shape[0]

    arr = np.empty((n * 2, 4), dtype=np.float64)
    arr[:n, :] = a
    #
    # n = 2
    # arr = np.array((
    #     (30, 350, 50, 0),
    #     (45, 500, 50, 0),
    #     (0, 0, 0, 0),
    #     (0, 0, 0, 0)
    #               ), dtype=np.float64)

    # n = 1
    # arr = np.array((
    #     (30, 350, 50, 0),
    #     (0, 0, 0, 0)
    #               ), dtype=np.float64)

    app = App(n, arr, 60, width=200, height=100, fullscreen=False)
    pyglet.app.run()
