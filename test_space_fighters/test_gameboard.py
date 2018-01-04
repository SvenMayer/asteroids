#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Sven Mayer
"""
import unittest
from space_fighters import GameBoard
from space_fighters import GamePiece


class TestGameBoardInit(unittest.TestCase):
    def test_init_arguments(self):
        gameboard = GameBoard.GameBoard(size=(200., 150.),
                                        no_asteroids=12)
        self.assertAlmostEqual(gameboard.size[0], 200.)
        self.assertAlmostEqual(gameboard.size[1], 150.)
        self.assertEqual(gameboard.no_asteroids, 12)

    def test_init(self):
        gameboard = GameBoard.GameBoard(size=(200., 150.),
                                        no_asteroids=12)
        self.assertTrue(hasattr(gameboard, '_asteroids'))
        self.assertTrue(hasattr(gameboard, 'moving_objects'))
        self.assertTrue(hasattr(gameboard, '_ship'))
        self.assertTrue(hasattr(gameboard, '_projectiles'))

    def test_init_wrong_size_argument(self):
        with self.assertRaises(AttributeError):
            gameboard = GameBoard.GameBoard(size=(200., 150., 300.),
                                            no_asteroids=10)

    def test_init_wrong_no_asteroids_arguemnts(self):
        with self.assertRaises(AttributeError):
            gameboard = GameBoard.GameBoard(size=(100., 120.),
                                            no_asteroids=10.2)

    def test_init_wrong_size_argument2(self):
        with self.assertRaises(AttributeError):
            gameboard = GameBoard.GameBoard(size="Sven", no_asteroids=10)


class TestGameBoardHiddenMethods(unittest.TestCase):
    def setUp(self):
        self.gameboard = GameBoard.GameBoard(size=(100., 100.), no_asteroids=2)

    def test_add_asteroid_wrong_type(self):
        with self.assertRaises(AttributeError):
            self.gameboard._add_asteroid(10)

    def test_add_asteroid(self):
        asteroid = GamePiece.Asteroid1(1., (0., 0., 0.), (1., 1.), 1.)
        self.gameboard._add_asteroid(asteroid)
        self.assertEqual(self.gameboard._asteroids[-1], asteroid)
        self.assertEqual(self.gameboard.moving_objects[-1], asteroid)

    def test_add_ship_wrong_type(self):
        with self.assertRaises(AttributeError):
            self.gameboard._add_ship(10)

    def test_add_ship(self):
        ship = GamePiece.Ship(1.)
        self.gameboard._add_ship(ship)
        self.assertEqual(self.gameboard._ship, ship)
        self.assertEqual(self.gameboard.moving_objects[-1], ship)

    def test_add_multiple_ships(self):
        ship1 = GamePiece.Ship(1.)
        ship2 = GamePiece.Ship(1.)
        self.gameboard._add_ship(ship1)
        with self.assertRaises(RuntimeError):
            self.gameboard._add_ship(ship2)

    def test_add_projectile_wrong_type(self):
        with self.assertRaises(AttributeError):
            self.gameboard._add_projectile(10)

    def test_add_projectile(self):
        proj = GamePiece.Projectile(1., (0., 0., 0.), (1., 1.))
        self.gameboard._add_projectile(proj)
        self.assertEqual(self.gameboard._projectiles[-1], proj)
        self.assertEqual(self.gameboard.moving_objects[-1], proj)


class TestGameBoardUserMethods(unittest.TestCase):
    def setUp(self):
        self.gameboard = GameBoard.GameBoard(size=(100., 100.), no_asteroids=2)
        self.ship = GamePiece.Ship(1., (10., 10., 0.))
        self.Asteroid = GamePiece.Asteroid1(1., (20., 10., 0), (0., 0.), 1.)

    def test_turn_ship(self):
        self.gameboard._add_ship(self.ship)
        self.gameboard.ship_turn(1)
        self.assertEqual(self.ship.turn, 1)

    def test_accelerate_ship(self):
        self.gameboard._add_ship(self.ship)
        self.gameboard.ship_accelerate(True)
        self.assertEqual(self.ship.thrust, 1)
        self.gameboard.ship_accelerate(False)
        self.assertEqual(self.ship.thrust, 0)

#    def test_fire_ship(self):
#        self.gameboard._add_ship(self.ship)
#        self.gameboard.ship_fire()
#        self.assertEqual(len(self.gameboard._projectiles), 1)
