#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Sven Mayer
"""
import numpy as np


class PhysicsEngine():
    def __init__(self, position=(0., 0., 0.), acceleration=1.5,
                 angular_velocity=0.1*np.pi, start_velocity=(0., 0.)):
        if not (isinstance(position, tuple) and (len(position) == 3)):
            raise ValueError("argument 'position' takes tuple of size three")
        self._position = position
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

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        if isinstance(value, tuple) and len(value) == 3:
            self._position = value
        elif isinstance(value, list) and len(value) == 3:
            self._position = (value[0], value[1], value[2])
        else:
            raise TypeError("Only tuples or lists with three elements can " +
                            "be assigned to position.")

    def step(self, dt):
        new_angle = self.position[2]
        if self._turn != 0:
            new_angle += self._turn * self._angular_velocity * dt
            new_angle %= 2. * np.pi
            self._sin_angle = np.sin(new_angle)
            self._cos_angle = np.cos(new_angle)

        if self._thrust != 0:
            self.velocity = (
                self.velocity[0] +
                self._thrust * self._acceleration * self._cos_angle * dt,
                self.velocity[1] +
                self._thrust * self._acceleration * self._sin_angle * dt)

        new_x = self.position[0] + self.velocity[0] * dt
        new_y = self.position[1] + self.velocity[1] * dt

        self.position = (new_x, new_y, new_angle)


class ConvexPolygon(object):
    def __init__(self, xy):
        self.xy = xy

        # Calculate the unity vector for each side.
        self.side = []
        for i in range(-1, len(self.xy) - 1):
            side_vector = (self.xy[i+1][0] - self.xy[i][0],
                           self.xy[i+1][1] - self.xy[i][1])
            len_side = np.sqrt(side_vector[0]**2. + side_vector[1]**2.)
            self.side.append((side_vector[0] / len_side,
                              side_vector[1] / len_side))
        self.side = self.side[1:] + self.side[:1]

        # Calculate the normal for each side.
        self.side_normal = []
        for side in self.side:
            self.side_normal.append((-1.*side[1], side[0]))

    def projection(self, proj_vec):
        return [xy[0] * proj_vec[0] + xy[1] * proj_vec[1] for
                xy in self.xy]

    def collides(self, other):
        # Find out which polygon has less sides to minimize the number
        # of projections needed to check for collision.
        if len(self.xy) < len(other.xy):
            normals = self.side_normal
        else:
            normals = other.side_normal

        collides = True
        for normal in normals:
            my_points = self.projection(normal)
            other_points = other.projection(normal)
            my_range = min(my_points), max(my_points)
            other_range = min(other_points), max(other_points)
            if not (my_range[1] > other_range[0] and
                    my_range[0] < other_range[1]):
                collides = False
                break

        return collides

    def rotate(self, angle=0.0):
        sina = np.sin(angle)
        cosa = np.cos(angle)
        self.xy = [(x*cosa-y*sina, x*sina+y*sina) for (x, y) in self.xy]
        self.side = [(x*cosa-y*sina, x*sina+y*sina) for (x, y) in self.side]
        self.side_normal = [(x*cosa-y*sina, x*sina+y*sina) for (x, y)
                            in self.side_normal]


class GamePiece(PhysicsEngine):
    def __init__(self, size, type, position=(0., 0., 0.), acceleration=1.5,
                 angular_velocity=0.1*np.pi, start_velocity=(0., 0.), **kwargs):
        super(GamePiece, self).__init__(
            position=position, acceleration=acceleration,
            angular_velocity=angular_velocity, start_velocity=start_velocity)
        self.size = size
        if type == "polygon":
            if 'xy' not in kwargs:
                raise TypeError("Argument 'xy' required for GamePiece type " +
                                "'polygon'")
            self._gb_repr = ConvexPolygon(xy=kwargs['xy'])
        elif type == "point":
            # TODO: Implement Point
            pass
        else:
            raise TypeError("Unknown type '{0:s}'".format(str(type)))


class Ship(GamePiece):
    def __init__(self, size, position=(0., 0., 0.), acceleration=1.5,
                 angular_velocity=0.1*np.pi):
        super(Ship, self).__init__(
            size=size, xy=[(-0.2679491924311227*size, -1./3.*size),
                           (0.2679491924311227*size, -1./3.*size),
                           (0., 2./3.*size)], type="polygon",
            position=position, acceleration=acceleration,
            angular_velocity=angular_velocity, start_velocity=(0., 0.))

    @property
    def gunposition(self):
        two_thirds_size = 2. / 3. * self.size
        return (
            self.position[0] + self._cos_angle * two_thirds_size,
            self.position[1] + self._sin_angle * two_thirds_size,
            self.position[2])


class AsteroidBase(GamePiece):
    def __init__(self, size, position, start_velocity, angular_velocity):
        # AsteroidBase cannot be instantiated.
        if type(self) is AsteroidBase:
            raise TypeError("AsteroidBase cannot be instantiated")
        super(AsteroidBase, self).__init__(
            size=size, type="polygon",
            xy=[(size * x, size * y) for (x, y) in self._xy],
            position=position, angular_velocity=np.abs(angular_velocity))
        if angular_velocity > 0.:
            self.turn = 1
        elif angular_velocity < 0.:
            self.turn = -1
        self.velocity = start_velocity


class Asteroid1(AsteroidBase):
    _xy = [(0.2, 0.4), (-0.08, 0.5), (-0.4, -0.4), (-0.5, -0.04),
           (-0.2, -0.4), (0.3, -0.3), (0.5, 0.1)]

    def __init__(self, size, position, start_velocity, angular_velocity):
        super(Asteroid1, self).__init__(size=size, position=position,
                                        start_velocity=start_velocity,
                                        angular_velocity=angular_velocity)
#
# TODO: Add more asteroid shapes.

class Projectile(GamePiece):
    def __init__(self, size, position, velocity):
        super(Projectile, self).__init__(
            size, type="point", position=position, start_velocity=velocity)
