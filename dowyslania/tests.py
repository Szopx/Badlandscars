import unittest
import pygame
import os
from grafiki import *

img = os.path.join("imgs", "bomb.png")

# grafiki


class GrafikiTests(unittest.TestCase):
    def setUp(self):
        self.g = Grafiki(img, 3, 14)

    def test_init(self):
        """checks that __init__ sets values properly"""
        self.assertEqual(self.g.pion_image, img)
        self.assertEqual(self.g.rem, img)
        self.assertEqual(self.g.image, img)
        self.assertIsInstance(self.g.rect, pygame.Rect)
        self.assertEqual(self.g.angle, 0)
        self.assertEqual(self.g.x, 3)
        self.assertEqual(self.g.y, 14)

    def test_hardskale(self):
        pass

    def test_kat(self):
        pass

    def test_rotoi(self):
        pass

    def test_skale(self):
        pass

    def test_zmienxy(self):
        pass

    def test_draw(self):
        pass
