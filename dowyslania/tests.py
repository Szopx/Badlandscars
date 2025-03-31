import unittest
import pygame
import os
import time
from grafiki import Grafiki
from przyciski import Przycisk
from obywyszlo import *

img = os.path.join("imgs", "bomb.png")

class GrafikiTests(unittest.TestCase):
    def setUp(self):
        self.g = Grafiki(img, 3, 14)

    def test_init(self):
        """checks that __init__ sets values properly"""
        self.assertEqual(self.g.pion_image, img)
        self.assertEqual(self.g.rem, img)
        self.assertIsInstance(self.g.image, pygame.Surface)
        self.assertIsInstance(self.g.rect, pygame.Rect)
        self.assertEqual(self.g.angle, 0)
        self.assertEqual(self.g.x, 3)
        self.assertEqual(self.g.y, 14)

    def test_kat(self):
        self.g.kat(30)
        self.assertEqual(self.g.angle, 30)

    def test_zmienxy(self):
        self.g.zmienxy(15,92)
        self.assertEqual(self.g.x, 15)
        self.assertEqual(self.g.y, 92)

class PrzyciskTests(unittest.TestCase):
    def setUp(self):
        self.p = Przycisk([0,1], img, img, 1)

    def test_init(self):
        """checks that __init__ sets values properly"""
        self.assertEqual(self.p.stan, False)
        self.assertEqual(self.p.skala, 1)
        self.assertEqual(self.p.x,0)
        self.assertEqual(self.p.y,1)
        self.assertEqual(self.p.niewcisniety, img)
        self.assertEqual(self.p.wcisniety, img)
        self.assertIsInstance(self.p.grafika, Grafiki)

class GameInfoTests(unittest.TestCase):
    def setUp(self):
        self.me = GameInfo()

    def test_init(self):
        """checks that __init__ sets values properly"""
        self.assertEqual(self.me.level, 1)
        self.assertEqual(self.me.started, False)
        self.assertEqual(self.me.level_start_time, 0)

    def test_next_level(self):
        tmp = self.me.level + 1
        self.me.next_level()
        self.assertEqual(self.me.level, tmp)
        self.assertEqual(self.me.started, False)

    def test_reset(self):
        self.me.next_level()
        self.me.start_level()
        self.me.reset()
        self.assertEqual(self.me.level, 1)
        self.assertEqual(self.me.started, False)
        self.assertEqual(self.me.level_start_time, 0)

    def test_game_finished(self):
        self.me.level = self.me.LEVELS
        self.assertEqual(self.me.game_finished(), False)
        self.me.level = self.me.LEVELS+1
        self.assertEqual(self.me.game_finished(), True)

    def test_start_level(self):
        self.me.start_level()
        self.assertEqual(self.me.started, True)
        self.assertTrue(self.me.level_start_time > 0)

    def test_get_level_time(self):
        self.me.reset()
        self.assertEqual(self.me.get_level_time(), 0)
        self.me.start_level()
        time.sleep(1)
        self.assertTrue(self.me.get_level_time() > 0)


if __name__ == "__main__":
    unittest.main()