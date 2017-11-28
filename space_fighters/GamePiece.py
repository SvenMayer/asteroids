#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Sven Mayer
"""
import numpy as np

class GamePiece():
    def __init__(self, position=(0., 0., 0.), acceleration=1.5,
                 angular_velocity=0.1*np.pi, start_velocity=(0., 0.)):
        if not (isinstance(position, tuple) and len(position)==3):
            raise ValueError("argument 'position' takes tuple of size three")
        self.position = position
        self.velocity = start_velocity
        self._acceleration = acceleration
        self._angular_velocity = angular_velocity
        self._sin_angle = np.sin(self.position[2])
        self._cos_angle = np.cos(self.position[2])
        self._thrust = False
        self._turn = 0

    @property
    def thrust(self):
        return self._thrust

    @thrust.setter
    def thrust(self, value):
        if not (isinstance(value, int) and value in [-1, 0, 1]):
            raise ValueError("thrust has to be of type 'bool'")
        self._thrust = value

    @property
    def turn(self):
        return self._turn

    @turn.setter
    def turn(self, value):
        if not (isinstance(value, int) and value in [-1, 0, 1]):
            raise ValueError("'turn' has to be integer -1, 0, or 1")
        self._turn = value

    def step(self, dt):
        new_angle = self.position[2]
        if self._turn != 0:
            new_angle += self._turn * self._angular_velocity * dt
            new_angle %= 2. * np.pi
            self._sin_angle = np.sin(new_angle)
            self._cos_angle = np.cos(new_angle)

        if self._thrust != 0:
            self.velocity =(
                self.velocity[0] +
                self._thrust * self._acceleration * self._cos_angle * dt,
                self.velocity[1] +
                self._thrust * self._acceleration * self._sin_angle * dt)

        new_x = self.position[0] + self.velocity[0] * dt
        new_y = self.position[1] + self.velocity[1] * dt

        self.position = (new_x, new_y, new_angle)
