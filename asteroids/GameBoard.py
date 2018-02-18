#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Sven Mayer
"""
from asteroids import GamePiece
import numpy as np


DEFAULT_PROJECTILE_SIZE = 10.
DEFAULT_PROJECTILE_VELO = 10.


class GameBoard(object):
    def __init__(self, size, no_asteroids):
        if not isinstance(size, tuple) and not isinstance(size, list):
            raise AttributeError("Argument 'size' has to be of type list or tuple")
        if len(size) != 2:
            raise AttributeError("Argument 'size' has to be of length 2")
        self.size = (size[0], size[1])

        if not isinstance(no_asteroids, int):
            raise AttributeError("Argument 'no_asteroids' has to be of type 'int'")
        self.no_asteroids = no_asteroids

        self._asteroids = []
        self._projectiles = []
        self._ship = None
        self.moving_objects = []
        self.gameover = False

    def _add_asteroid(self, obj):
        if not isinstance(obj, GamePiece.AsteroidBase):
            raise AttributeError("Added object has to be of type 'AsteroidBase'")
        self._asteroids.append(obj)
        self.moving_objects.append(obj)

    def _add_ship(self, obj):
        if not isinstance(obj, GamePiece.Ship):
            raise AttributeError("Added object has to be of type 'Ship'")
        if self._ship is not None:
            raise RuntimeError("Cannot add multiple ships")
        self._ship = obj
        self.moving_objects.append(obj)

    def _add_projectile(self, obj):
        if not isinstance(obj, GamePiece.Projectile):
            raise AttributeError("Added object has to be of type 'Projectile'")
        self._projectiles.append(obj)
        self.moving_objects.append(obj)

    def _asteroids_out_of_bounds(self):
        for asteroid in self._asteroids:
            pos = asteroid.position
            if (pos[0] < 0. or pos[0] > self.size[0] or
                    pos[1] < 0. or pos[1] > self.size[1]):
                asteroid.position = (pos[0] % self.size[0],
                                     pos[1] % self.size[1],
                                     pos[2])

    def _projectiles_out_of_bounds(self):
        for idx, projectile in enumerate(self._projectiles[::-1]):
            pos = projectile.position
            if (pos[0] < 0. or pos[0] > self.size[0] or
                    pos[1] < 0. or pos[1] > self.size[1]):
                self._projectiles.pop(idx)
                self.moving_objects.pop(self.moving_objects.index(projectile))

    def _ship_out_of_bounds(self):
        pos = self._ship.position
        if (pos[0] < 0. or pos[0] > self.size[0] or
                pos[1] < 0. or pos[1] > self.size[1]):
            self._ship.position = (
                pos[0] % self.size[0],
                pos[1] % self.size[1],
                pos[2])

    def _calculate_new_position(self, dt):
        for itm in self.moving_objects:
            self.moving_objects.step(dt)

    def _resolve_collision(self):
        # Check if the ship collides with any asteroid.
        for asteroid in self._asteroids:
            if self._ship is not None and self._ship.collides(asteroid):
                self.gameover = True
                break
        for i in range(len(self._asteroids)-1, -1, -1):
            for j in range(len(self._projectiles)-1, -1, -1):
                if self._asteroids[i].collides(self._projectiles[j]):
                    self._asteroids.pop(i)
                    self._projectiles.pop(j)
                    break

    def step(self, dt):
        self._calculate_new_position(dt)
        self._asteroids_out_of_bounds()
        self._projectiles_out_of_bounds()
        self._ship_out_of_bounds()
        # TODO: Check if anything collides.
        # Ship destroyed.
        # Asteroids destroyed.

    def ship_turn(self, direction):
        self._ship.turn = direction

    def ship_accelerate(self, value):
        if value:
            self._ship.thrust = 1
        else:
            self._ship.thrust = 0

    def ship_fire(self):
        gunpos = self._ship.gunposition
        velo = (
            DEFAULT_PROJECTILE_VELO * np.cos(gunpos[2]),
            DEFAULT_PROJECTILE_VELO * np.sin(gunpos[2]))

        projectile = GamePiece.Projectile(size=DEFAULT_PROJECTILE_SIZE,
                                          position=gunpos, velocity=velo)

        self._projectiles.append(projectile)
        self.moving_objects.append(projectile)
