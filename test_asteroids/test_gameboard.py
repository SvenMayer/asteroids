#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Sven Mayer
"""
import unittest
from asteroids import GameBoard
from asteroids import GamePiece


class TestGameBoardInit(unittest.TestCase):
    def test_init_arguments(self):
        gameboard = GameBoard.GameBoard(size=(200., 150.),
                                        no_asteroids=12)
        self.assertSequenceEqual(gameboard.size, (200., 150.))
        self.assertEqual(gameboard.no_asteroids, 12)

    def test_init(self):
        gameboard = GameBoard.GameBoard(size=(200., 150.),
                                        no_asteroids=12)
        self.assertTrue(hasattr(gameboard, '_asteroids'))
        self.assertTrue(hasattr(gameboard, 'moving_objects'))
        self.assertTrue(hasattr(gameboard, '_ship'))
        self.assertTrue(hasattr(gameboard, '_projectiles'))
        self.assertTrue(hasattr(gameboard, 'gameover'))

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

    def test_asteroid_out_of_bounds(self):
        asteroid = GamePiece.Asteroid1(1., (120., 40., 2.), (1., 1.), 1.)
        self.gameboard._add_asteroid(asteroid)
        self.gameboard._asteroids_out_of_bounds()
        self.assertSequenceEqual(asteroid.position, (20., 40., 2.))

    def test_projectile_out_of_bounds(self):
        projectile = GamePiece.Projectile(size=4., position=(30., -10, 2.),
                                          velocity=(0., 0.))
        self.gameboard._add_projectile(projectile)
        self.gameboard._projectiles_out_of_bounds()
        self.assertNotIn(projectile, self.gameboard._projectiles)
        self.assertNotIn(projectile, self.gameboard.moving_objects)

    def test_ship_out_of_bounds(self):
        ship = GamePiece.Ship(size=10., position=(-30., 20., 1.))
        self.gameboard._add_ship(ship)
        self.gameboard._ship_out_of_bounds()
        self.assertSequenceEqual(ship.position, (70., 20., 1.))

    def test_collision_asteroid_collides_ship(self):
        ship = GamePiece.Ship(size=1.,position=(0., 0., 2.))
        asteroid = GamePiece.Asteroid1(size=1., position=(0., 0., 4.),
                                       start_velocity=(1., 1.),
                                       angular_velocity=-10.)
        self.gameboard._add_ship(ship)
        self.gameboard._add_asteroid(asteroid)
        self.gameboard._resolve_collision()
        self.assertTrue(self.gameboard.gameover)

    def test_collision_asteroid_collides_projectile(self):
        projectile = GamePiece.Projectile(1.0, (0., 0., 0.), (1., 0.))
        asteroid = GamePiece.Asteroid1(size=1., position=(0., 0., 4.),
                                       start_velocity=(1., 1.),
                                       angular_velocity=-10.)
        self.gameboard._add_asteroid(asteroid)
        self.gameboard._add_projectile(projectile)
        self.gameboard._resolve_collision()
        self.assertNotIn(asteroid, self.gameboard._asteroids)
        self.assertNotIn(projectile, self.gameboard._projectiles)


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

    def test_fire_ship(self):
        self.gameboard._add_ship(self.ship)
        self.gameboard.ship_fire()
        self.assertSequenceEqual(self.gameboard._projectiles[-1].position,
                                 self.ship.gunposition)
        self.assertSequenceEqual(self.gameboard.moving_objects[-1].position,
                                 self.ship.gunposition)

if __name__ == u"__main__":
    unittest.main()