#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Sven Mayer
"""
import unittest
from space_fighters import GamePiece


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


if __name__ == u"__main__":
    unittest.main()
