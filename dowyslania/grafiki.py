import pygame

class Grafiki(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.pion_image = image
        self.rem = self.pion_image
        self.image = self.pion_image
        self.rect = self.image.get_rect(center = (x, y))
        self.angle = 0
        self.x=x
        self.y=y
    def hardskale(self, n):
        self.pion_image = pygame.transform.scale(self.rem, (self.rem.get_width() * n, self.rem.get_height() * n))
        self.rem = self.pion_image
        self.rect = self.pion_image.get_rect()
        self.image = self.pion_image
        self.zmienxy(self.x, self.y)
    def kat(self,kot):
        self.image = pygame.transform.rotate(self.pion_image, kot)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.angle = kot
    def rotoi(self,k): #rotate only image
        self.image = pygame.transform.rotate(self.pion_image, self.angle+k)
        self.rect = self.image.get_rect(center=self.rect.center)
    def skale(self, n):
        self.pion_image = pygame.transform.scale(self.rem, (self.rem.get_width()*n, self.rem.get_height()*n))
        self.rect = self.pion_image.get_rect()
        self.image=self.pion_image
        self.zmienxy(self.x, self.y)
    def zmienxy(self,x1,y1):
        self.x=x1
        self.y=y1
        self.rect = self.image.get_rect(center = (x1, y1))
    def draw(self, scrn):
        scrn.blit(self.image,self.rect)
