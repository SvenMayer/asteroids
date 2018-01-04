#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Sven Mayer
"""
from space_fighters import GamePiece


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

    def ship_turn(self, direction):
        self._ship.turn = direction

    def ship_accelerate(self, value):
        if value:
            self._ship.thrust = 1
        else:
            self._ship.thrust = 0

#
#    def ship_fire(self):
#        ship_pos = self._ship.position
