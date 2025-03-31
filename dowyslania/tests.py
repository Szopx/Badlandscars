import unittest
import pygame
import os
from grafiki import Grafiki
from przyciski import Przycisk

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

class PrzyciskiTests(unittest.TestCase):
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

if __name__ == "__main__":
    unittest.main()