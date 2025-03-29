from grafiki import Grafiki
import pygame
class Przycisk:
    def __init__(self, L,niewcisniety, wcisniety,skala):
        self.stan=False
        self.skala = skala
        self.x=L[0]
        self.y=L[1]
        self.niewcisniety = niewcisniety
        self.wcisniety = wcisniety
        self.grafika = Grafiki(niewcisniety,L[0],L[1])
    def sprawdz(self,pozycja):
        if self.grafika.rect.collidepoint(pygame.mouse.get_pos()):
            self.grafika.image = self.wcisniety

            self.stan = True
        elif self.stan == True:
            self.stan = False
            self.grafika.image = self.niewcisniety





