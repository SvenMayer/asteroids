#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Sven Mayer
"""
import unittest
from asteroids import GamePiece


import numpy as np


class TestGamePiece(unittest.TestCase):
    def test_initialize_empty(self):
        gamePiece = GamePiece.GamePiece()
        self.assertIsInstance(gamePiece, GamePiece.GamePiece)

    def test_initialize_wrong_position_parameters(self):
        with self.assertRaises(ValueError):
            GamePiece.GamePiece((1., 2.))

    def test_initialize(self):
        pos = (1., 2., 0.)
        gamePiece = GamePiece.GamePiece(position=pos)
        self.assertEqual(gamePiece.position, pos)

    def test_increase_velo(self):
        gamePiece = GamePiece.GamePiece((0., 0., 0.), acceleration=10.)
        gamePiece.thrust = 1
        gamePiece.step(0.1)
        self.assertAlmostEqual(gamePiece.velocity, (1., 0.))

    def test_turn(self):
        dt_step = 0.1
        angular_velocity = 0.1 * np.pi
        gamePiece = GamePiece.GamePiece((0., 0., 0.),
                                        angular_velocity=angular_velocity)
        gamePiece.turn = 1
        gamePiece.step(dt_step)
        self.assertAlmostEqual(gamePiece.position[2],
                               dt_step*angular_velocity)

    def test_new_position(self):
        pos = (1., 2., np.pi/2.)
        angular_velocity = 0.1*np.pi
        acceleration = 1.5
        gamePiece = GamePiece.GamePiece(
            pos, acceleration=acceleration, angular_velocity=angular_velocity)
        gamePiece.thrust = 1
        gamePiece.step(1.0)
        new_velo_y = 1.5*1.0
        new_pos = 1., 2.+new_velo_y*1.0, np.pi/2.
        gamePiece.thrust = 0
        gamePiece.turn = 1
        gamePiece.step(3.0)
        new2_angle = pos[2] + angular_velocity*3.0
        new2_pos = new_pos[0], new_pos[1]+new_velo_y*3.0, new2_angle
        gamePiece.turn = 0
        gamePiece.thrust = 1
        gamePiece.step(1.0)
        new3_velo_x = 0. + acceleration * 1.0 * np.cos(new2_angle)
        new3_velo_y = new_velo_y + acceleration * 1.0 * np.sin(new2_angle)
        new3_pos = (new2_pos[0] + new3_velo_x * 1.0,
                    new2_pos[1] + new3_velo_y * 1.0,
                    new2_angle)
        self.assertAlmostEqual(gamePiece.position[0]+gamePiece.position[1]+gamePiece.position[2],
                               new3_pos[0]+new3_pos[1]+new3_pos[2])

    def test_set_position_wrong_type(self):
        gamePiece = GamePiece.GamePiece(position=(0., 0., 0.),
                                        start_velocity=(1., 1.),
                                        angular_velocity=1.5)
        with self.assertRaises(TypeError):
            gamePiece.position = (1., 2., 3., 4.)

    def test_spin_and_start_velo(self):
        position = (0., 0., 0.)
        start_velocity = 1., 2.
        angular_velocity = np.pi/4.
        gamePiece = GamePiece.GamePiece(position=position,
                              start_velocity=start_velocity,
                              angular_velocity=angular_velocity)
        turnDir = -1
        gamePiece.turn = turnDir
        dt = 1.5
        gamePiece.step(dt)
        new_position = (
            position[0] + start_velocity[0] * dt,
            position[1] + start_velocity[1] * dt,
            (position[2] + angular_velocity * dt * turnDir) % (2. * np.pi))
        self.assertAlmostEqual(new_position[0]+new_position[1]+
                               new_position[2],
                               gamePiece.position[0]+gamePiece.position[1]+
                               gamePiece.position[2])


class TestConvexPolygon(unittest.TestCase):
    def test_init(self):
        xy = (0., 0.), (1., 2.), (-2., 1.), (-1., -1.)
        con_pol = GamePiece.ConvexPolygon(xy)
        self.assertIsInstance(con_pol, GamePiece.ConvexPolygon)

    def test_side_vectors(self):
        xy = (0., 0.), (1., 2.), (-2., 1.)
        side = []
        len_side = []
        unity_side = []
        for i in range(-1, len(xy)-1):
            side.append((xy[i+1][0]-xy[i][0], xy[i+1][1]-xy[i][1]))
            len_side.append(np.sqrt(side[-1][0]**2. + side[-1][1]**2.))
            unity_side.append((side[-1][0]/len_side[-1], side[-1][1]/len_side[-1]))
        unity_side = unity_side[1:] + unity_side[:1]

        con_pol = GamePiece.ConvexPolygon(xy)
        self.assertAlmostEqual(unity_side[0][0]+unity_side[1][0]+
                               unity_side[2][0]+unity_side[0][1]+
                               unity_side[1][1]+unity_side[2][1],
                               con_pol.side[0][0]+con_pol.side[1][0]+
                               con_pol.side[2][0]+con_pol.side[0][1]+
                               con_pol.side[1][1]+con_pol.side[2][1])

    def test_side_normal_vector(self):
        xy = (0., 0.), (0., 1.), (1., 1.)
        con_pol = GamePiece.ConvexPolygon(xy)
        self.assertAlmostEqual(np.abs(con_pol.side_normal[0][0]+
                               con_pol.side_normal[0][1])+
                               np.abs(con_pol.side_normal[1][0]+
                               con_pol.side_normal[1][1])+
                               np.abs(con_pol.side_normal[2][0]+
                               con_pol.side_normal[2][1]),
                               1. + 0. + 1. )

    def test_projection(self):
        xy = [(0., 0.), (1., 1.), (-1., 1.)]
        poly = GamePiece.ConvexPolygon(xy)
        proj = poly.projection((1./np.sqrt(2.), 1./np.sqrt(2.)))
        self.assertAlmostEqual(proj[0] + proj[1] + proj[2], np.sqrt(2.))

    def test_collision(self):
        poly1 = GamePiece.ConvexPolygon([(0., 0.), (1., 1.), (0., 1.)])
        poly2 = GamePiece.ConvexPolygon([(1., 0.), (0.8, 1.), (2., 1.)])
        self.assertTrue(poly1.collides(poly2))

    def test_nocollision(self):
        poly1 = GamePiece.ConvexPolygon([(0., 0.), (1., 1.), (0., 1.)])
        poly2 = GamePiece.ConvexPolygon([(1., 0.), (1., 1.), (2., 1.)])
        self.assertFalse(poly1.collides(poly2))

    def test_rotate(self):
        poly = GamePiece.ConvexPolygon([(0., 0.), (0., 1.), (1., 0.)])
        poly.rotate(np.pi/2.)
        self.assertAlmostEqual(poly.xy[1][0], -1.)


class TestShip(unittest.TestCase):
    def test_init(self):
        ship = GamePiece.Ship(size=2.4)
        self.assertAlmostEqual(ship.size, 2.4)

    def test_gun_position(self):
        ship = GamePiece.Ship(size=10., position=(0., 0., 0.))
        self.assertAlmostEqual(ship.gunposition[0], 2.*10./3.)
        self.assertAlmostEqual(ship.gunposition[1], 0.)
        self.assertAlmostEqual(ship.gunposition[2], 0.)


class TestAsteroidBase(unittest.TestCase):
    def test_init(self):
        with self.assertRaises(TypeError):
            GamePiece.AsteroidBase(position=(0., 0., 0.), size=1.0,
                                   angular_velocity=0., start_velocity=(0., 0.))

class TestAsteroids(unittest.TestCase):
    def test_init_(self):
        asteroid = GamePiece.Asteroid1(size=3.6, position=(0., 0., 0.),
                                       angular_velocity=10.,
                                       start_velocity=(1.2, 2.1))
        self.assertAlmostEqual(asteroid.size+asteroid.velocity[0]+
                               asteroid.position[0]+asteroid._angular_velocity,
                               3.6+1.2+0.+10.)


class TestProjectile(unittest.TestCase):
    def test_init_(self):
        projectile = GamePiece.Projectile(size=1., position=(2., 3., 4.),
                                          velocity=(4.2, 5.3))
        self.assertAlmostEqual(projectile.size+projectile.position[1]+
                               projectile.velocity[1], 1.+3.+5.3)


if __name__ == u"__main__":
    unittest.main()