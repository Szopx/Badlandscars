import pygame
import math
import random
from przyciski import Przycisk
import pygame
import time
from utils import scale_image, blit_rotate_center, blit_text_center

#Definicja klasy
class GameInfo:
    LEVELS = 10

    def __init__(self, level=1):
        self.level = level
        self.started = False
        self.level_start_time = 0

    def next_level(self):
        self.level += 1
        self.started = False

    def reset(self):
        self.level = 1
        self.started = False
        self.level_start_time = 0

    def game_finished(self):
        return self.level > self.LEVELS

    def start_level(self):
        self.started = True
        self.level_start_time = time.time()

    def get_level_time(self):
        if not self.started:
            return 0
        return round(time.time() - self.level_start_time)

class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 90
        self.laps = 0
        self.acceleration = 0.1
        self.bomb_limit = 1
        self.bomb = Bomb((-10000,-1000))
        self.didbounce = 0
        self.countdowntornada=0
    def bounce(self):
        self.vel = -1.5*self.vel
        self.didbounce=1
        self.move()
    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()
    def rotate(self, left=False, right=False, m=1):
        if left:
            self.angle += self.rotation_vel*m
        elif right:
            self.angle -= self.rotation_vel*m
    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)
    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()
    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()
    def move(self,m=1):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel*m
        horizontal = math.sin(radians) * self.vel*m

        self.y -= vertical
        self.x -= horizontal
    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi
    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 90
        #self.vel = 0
    def przerzut(self):
        self.x, self.y = (self.START_POS[0]+200,self.START_POS[1])
        self.angle = 90
        #self.vel = 0
    def dodajbombe(self):
        if self.bomb_limit!=0:
            pygame.mixer.Sound.play(v_czarna_dziura)
            self.bomb_limit -=1
            self.bomb.czas = 13
            self.bomb.x= self.x
            self.bomb.y =self.y
            #print('ok')
    def wyrzućbombe(self):
        self.bomb.x,self.bomb.y = (-100,-100)
        self.bomb_limit=1
    def bombaminusczas(self):
        if self.bomb.czas>0:
            self.bomb.czas-=1
            if self.bomb.czas==0:
                self.wyrzućbombe()
class PlayerCar(AbstractCar):
    def __init__(self, max_vel, rotation_vel):
        super().__init__(max_vel, rotation_vel)
        self.x, self.y = (885, 514)
        self.img = RED_CAR
        self.START_POS = (885, 514)
        self.MASK= RED_CAR_MASK
        self.turbo_counter = 0
    def turbo(self):

        global ilosc_monet
        if ilosc_monet>=5:
            ilosc_monet -=5
            self.turbo_counter = 5
class Monetka:
    def __init__(self, pos):
        self.x, self.y = pos
        self.pos = pos
        self.img = MONETA
        self.maska = MONETA_MASKA

    def odrzuć(self):
        global ilosc_monet
        ilosc_monet += 1
        self.x, self.y = (-1000, -1000)

    def przywróć(self):
        self.x, self.y = self.pos
class Bomb:
    def __init__(self, pos):
        self.img = scale_image(pygame.image.load("_internal/imgs/boomba1.png"), 0.2)
        self.maska = pygame.mask.from_surface(self.img)
        self.x, self.y = pos
        self.czas = 0
class Ufoludek:
    def __init__(self):
        self.Grafiki = [scale_image(pygame.image.load("_internal/imgs/ufo/ufols1.png").convert_alpha(), 0.5),
         scale_image(pygame.image.load("_internal/imgs/ufo/ufols2.png").convert_alpha(), 0.5),
        scale_image(pygame.image.load("_internal/imgs/ufo/ufols3.png").convert_alpha(), 0.5),
         scale_image(pygame.image.load("_internal/imgs/ufo/ufolo.png").convert_alpha(), 0.5)]
        self.grafika=1
        self.Maska= pygame.mask.from_surface(self.Grafiki[0])
        self.pozycje = [(253, 200),(77, 314),(600,120),(1103, 528),(1103, 224)]
        self.pos = (-1000,-1000)
        self.czyobudzony = False
        self.countdown = 0
    def losujpozycje(self):
        m = random.randint(0, len(self.pozycje) - 1)
        if self.pozycje[m] != self.pos:
            self.pos = self.pozycje[m]
        else:
            self.pos = self.pozycje[(m+1)%len(self.pozycje)]
    def zmiengrafike(self):
        if self.czyobudzony==False:
            self.grafika+=1
            self.grafika %=3
    def odlicz(self):
        self.countdown = max(0,self.countdown -1)
        if self.countdown == 0:
            self.czyobudzony = False
class Pajak:
    def __init__(self):
        self.Grafiki = [scale_image(pygame.image.load("_internal/imgs/pajak1.png").convert_alpha(), 0.5),
         scale_image(pygame.image.load("_internal/imgs/pajak2.png").convert_alpha(), 0.5),
        scale_image(pygame.image.load("_internal/imgs/pajak3.png").convert_alpha(), 0.5)]
        self.grafika=1
        self.Maska= pygame.mask.from_surface(self.Grafiki[0])
        self.granice = [115,246]
        self.goradol=0
        self.pos = (921,115)
        self.countdown = 0
    def idz(self):
        if self.goradol ==1:
            self.pos=(921, self.pos[1]-5)
        else:
            self.pos=(921, self.pos[1]+5)
        if self.pos[1]<115:
            self.goradol=0
        elif self.pos[1]>246:
            self.goradol=1
    def zmiengrafike(self):
        self.grafika+=1
        self.grafika %=3


class ComputerCar(AbstractCar):
    def __init__(self, max_vel, rotation_vel, IMG, MASK, START_POS,path = [], isaggresive = 0, ismistrzprostej = 1):
        super().__init__(max_vel, rotation_vel)
        self.path = path
        self.current_point = 0
        self.point_before = -1
        self.vel = max_vel
        self.x, self.y = START_POS
        self.img = IMG
        self.START_POS= START_POS
        self.MASK = MASK
        self.isaggresive = isaggresive
        self.ismistrzprostej = ismistrzprostej
    def draw_points(self, win):
        for point in self.path:
            pygame.draw.circle(win, (255, 0, 0), point, 5)

    def draw(self, win):
        super().draw(win)
        # self.draw_points(win)

    def calculate_angle(self, czypokazuj=1):
        target_x, target_y = self.path[self.current_point]
        x_diff = target_x - self.x
        y_diff = target_y - self.y

        if y_diff == 0:
            desired_radian_angle = math.pi / 2
        else:
            desired_radian_angle = math.atan(x_diff/y_diff)

        if target_y > self.y:
            desired_radian_angle += math.pi

        difference_in_angle = self.angle - math.degrees(desired_radian_angle)
        if difference_in_angle > 180:
            difference_in_angle -= 360
        if abs(difference_in_angle)%360>30 and (self.x-target_x)**2+(self.y-target_y)**2>25:
            if self.ismistrzprostej == 1:
                self.vel = self.vel / 2

        if difference_in_angle > 0:
            self.angle -= min(self.rotation_vel, abs(difference_in_angle))
            self.angle %= 360
        else:
            self.angle += min(self.rotation_vel, abs(difference_in_angle))
            self.angle %=360

    def update_path_point(self):
        target = self.path[self.current_point]
        rect = pygame.Rect(
            self.x-5, self.y-5, self.img.get_width(), self.img.get_height())
        if rect.collidepoint(*target):
            self.current_point += 1

    def move(self):
        if self.current_point >= len(self.path):
            return
        self.calculate_angle()
        self.update_path_point()
        super().move()
    def bounce(self):
        if random.randint(0,30)==3:
            self.dodajbombe()
        super().bounce()

    def next_level(self, level):
        self.reset()
        self.vel = self.max_vel + (level - 1) * 0.2
        self.current_point = 0

    def idzdogracza(self,x,y):
        x_diff = x - self.x
        y_diff = y - self.y

        if y_diff == 0:
            desired_radian_angle = math.pi / 2
        else:
            desired_radian_angle = math.atan(x_diff / y_diff)

        if y > self.y:
            desired_radian_angle += math.pi

        difference_in_angle = self.angle - math.degrees(desired_radian_angle)
        if difference_in_angle > 180:
            difference_in_angle -= 360

        if difference_in_angle > 0:
            self.angle -= min(self.rotation_vel, abs(difference_in_angle))
            self.angle %= 360
        else:
            self.angle += min(self.rotation_vel, abs(difference_in_angle))
            self.angle %=360
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel* 1.5
        horizontal = math.sin(radians) * self.vel *1.5

        self.y -= vertical
        self.x -= horizontal
    def reset(self):
        self.current_point = 0
        super().reset()
def draw(win, images, player_car, computer_cars,game_info):
    global ilosc_monet, tryb, obecnysnieg, czysniezy
    global PATH1,PATH2
    for img, pos in images:
        win.blit(img, pos)

    level_text = MAIN_FONT.render(
        f"Moje okrążenia {player_car.laps}", 1, (255, 255, 255))
    win.blit(level_text, (10, 120 - level_text.get_height()))

    c_laps = MAIN_FONT.render(
        f"Pozostałe okrążenia: 1 - {computer_cars[0].laps} ; 2 - {computer_cars[1].laps}"
        f"; 3 - {computer_cars[2].laps}; 4 -{computer_cars[3].laps}", 1, (255, 255, 255))
    win.blit(c_laps, (10, 60 - c_laps.get_height()))

    time_text = MAIN_FONT.render(
        f"Czas: {game_info.get_level_time()}s", 1, (255, 255, 255))
    win.blit(time_text, (WIDTH - 400, 10))

    forsa= MAIN_FONT.render(
    f"Money {ilosc_monet}", 1, (255, 255, 255))
    win.blit(forsa, (WIDTH - 400, 60))

    for computer_car in computer_cars+[player_car]:
        computer_car.draw(win)
        win.blit(computer_car.bomb.img, (computer_car.bomb.x, computer_car.bomb.y))

    for punkt in PATH1:
        pygame.draw.circle(WIN,(0,255,0), punkt, 5)
    for punkt in PATH2:
        pygame.draw.circle(WIN,(0,0,255), punkt, 5)
    if tryb == "merkury" and czysniezy == True:
        win.blit(SNIEG[obecnysnieg], (0,0))

    pygame.display.update()
def deklaruj(tekst, n):
    global TRACK, GRASS, BUDYNKI, TRACK_BORDER, TRACK_BORDER_MASK, FINISH, FINISH_MASK, PATH1, PATH2, monety
    fact = 0.7
    TRACK = scale_image(pygame.image.load(f'_internal/imgs/tekstury/{tekst}-trasa.png').convert_alpha(), fact)
    GRASS = scale_image(pygame.image.load(f'_internal/imgs/tekstury/{tekst}-tlo.png').convert_alpha(), fact)
    BUDYNKI = scale_image(pygame.image.load(f'_internal/imgs/tekstury/{tekst}-infrastruktura.png').convert_alpha(), fact)
    TRACK_BORDER = scale_image(pygame.image.load(f'_internal/imgs/tekstury/{tekst}-trasa-outline.png'), fact)
    TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
    FINISH = scale_image(pygame.image.load(f'_internal/imgs/tekstury/{tekst}-meta.png'), fact)
    FINISH_MASK = pygame.mask.from_surface(FINISH)
    PATH1 = PATHS[2 * n - 2]
    PATH2 = PATHS[2 * n - 1]
    monety = MONETS[n - 1]
def move_player(player_car, m=1):
    global c
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True, m=1)
    if keys[pygame.K_w]:
        moved = True
        player_car.move_forward()
    if keys[pygame.K_s]:
        moved = True
        player_car.move_backward()
    if keys[pygame.K_SPACE]:
        player_car.dodajbombe()
    if keys[pygame.K_x]:
        player_car.przerzut()
    if keys[pygame.K_BACKSPACE]:
        global tryb
        tryb = "Main"
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        pygame.mixer.music.load('_internal\dzwieki\\menu.mp3')
        pygame.mixer.music.play(loops=-1, start=0.0, fade_ms=750)
    if keys[pygame.K_q]:
        print(pygame.mouse.get_pos())
    if keys[pygame.K_r]:
        if c % 5 == 0:
            player_car.turbo()
    if keys[pygame.K_z]:
        global ilosc_monet
        if c%5==0:
            ilosc_monet+=5
    if not moved:
        player_car.reduce_speed()
def handle_collision(player_car, computercars, game_info):
    global tryb
    for x in [player_car]+computercars:
        if x.collide(TRACK_BORDER_MASK) != None:
            x.bounce()
        for y in [player_car]+computercars:
            if x!=y and x.collide(y.MASK, *(y.x,y.y))!= None:
                x.bounce()
        '''if x.collide(OLEJ_MASKA) != None and tryb == "mars":
            x.rotate(right=True)'''
    for m in computercars:
        computer_finish_poi_collide = m.collide(
            FINISH_MASK, *FINISH_POSITION)
        if computer_finish_poi_collide != None:
            if computer_finish_poi_collide[0]!=943:
                m.laps+=1
                m.x+=-110
            else:
                m.bounce()

    player_finish_poi_collide = player_car.collide(
        FINISH_MASK, *FINISH_POSITION)
    if player_finish_poi_collide != None:
        if player_finish_poi_collide[0] == 943:
            player_car.bounce()
        else:
            player_car.laps +=1
            player_car.reset()

            global monety
            for moneta in monety:
                moneta.przywróć()

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    fact = 0.7
    obecneauto=0
    TRACK = scale_image(pygame.image.load("_internal/imgs/tekstury/mars-trasa.png"), 0.7)
    WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Rewolucyjne Autka")

    FINISH_POSITION = (0, 0)

    pygame.mixer.music.load(r'_internal\dzwieki\menu.mp3')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    v_przycisk = pygame.mixer.Sound("_internal\dzwieki\\najazd-na-przycisk.wav")
    v_auta = pygame.mixer.Sound("_internal\dzwieki\\Autka_same.mp3")
    v_czarna_dziura = pygame.mixer.Sound("_internal\dzwieki\\czarna_dziura.mp3")
    v_gra = pygame.mixer.Sound("_internal\dzwieki\\gra.mp3")
    v_menu = pygame.mixer.Sound("_internal\dzwieki\\menu.mp3")
    v_pajak = pygame.mixer.Sound("_internal\dzwieki\\pajak.mp3")
    v_poslizg = pygame.mixer.Sound("_internal\dzwieki\\poslizg.mp3")
    v_snieg = pygame.mixer.Sound("_internal\dzwieki\\snieg.mp3 ")
    v_ufo = pygame.mixer.Sound("_internal\dzwieki\\UFOLUDEK.wav")
    v_wygrana = pygame.mixer.Sound("_internal\dzwieki\\wygrana.mp3")
    v_tornado = pygame.mixer.Sound("_internal\dzwieki\\tornado.wav")

    TLO = pygame.image.load("_internal/imgs/tlo.png").convert_alpha()
    MONETA = scale_image(pygame.image.load("_internal/imgs/moneta.png"), 0.2)
    MONETA_MASKA = pygame.mask.from_surface(MONETA)
    RED_CAR = scale_image(pygame.image.load("_internal/imgs/auta/pl1.png").convert_alpha(), 1.2)
    RED_CAR_MASK = pygame.mask.from_surface(RED_CAR)
    GREEN_CAR = scale_image(pygame.image.load("_internal/imgs/auta/en1.png"), 0.9)
    GREEN_CAR_MASK = pygame.mask.from_surface(GREEN_CAR)
    PURPLE_CAR = scale_image(pygame.image.load("_internal/imgs/auta/en2.png"), 1.0)
    PURPLE_CAR_MASK = pygame.mask.from_surface(GREEN_CAR)
    WHITE_CAR = scale_image(pygame.image.load("_internal/imgs/auta/en3.png"), 1.0)
    WHITE_CAR_MASK = pygame.mask.from_surface(GREEN_CAR)
    GREY_CAR = scale_image(pygame.image.load("_internal/imgs/auta/en4.png"), 1.0)
    GREY_CAR_MASK = pygame.mask.from_surface(GREEN_CAR)
    BOMBA1 = scale_image(pygame.image.load("_internal/imgs/boomba1.png"), 0.2)
    BOMBA2 = scale_image(pygame.image.load("_internal/imgs/boomba2.png"), 0.2)
    creditsy = scale_image(pygame.image.load("_internal/imgs/creditsy.png").convert_alpha(), 0.65)
    h2play = scale_image(pygame.image.load("_internal/imgs/h2play.png").convert_alpha(),0.7)
    SNIEG = [scale_image(pygame.image.load("_internal/imgs/snieg1.png"), 0.7),
             scale_image(pygame.image.load("_internal/imgs/snieg2.png"), 0.7),
             scale_image(pygame.image.load("_internal/imgs/snieg3.png"), 0.7),
             scale_image(pygame.image.load("_internal/imgs/snieg4.png"), 0.7),
             scale_image(pygame.image.load("_internal/imgs/snieg5.png"), 0.7)]
    obecnysnieg=0

    MAIN_FONT = pygame.font.SysFont("comicsans", 44)

    (TRACK, GRASS, BUDYNKI, TRACK_BORDER, TRACK_BORDER_MASK,
     FINISH, FINISH_MASK, PATH1, PATH2,monety) = (0 for i in range(10))

    PATHS = [[(748, 500),(722, 438),(347, 450),(74+10, 366),(203, 202),
            (405, 170),(1125, 197),(1194+20, 302-20),(1126, 402),(1096, 553),(873, 566)],

            [(764, 498), (708, 444), (606, 408), (562, 403), (458, 403),
            (410, 427), (323, 428), (261, 430), (182, 412), (124, 371), (115, 315),
            (151, 246), (230, 206), (315, 193), (337, 191), (442, 183), (540, 190),
            (586, 191), (632, 191), (713, 191), (788, 199), (873, 202), (901, 200), (1022, 202), (1138, 224), (1210, 236), (1246, 296), (1226, 337), (1165, 391), (1127, 438), (1143, 490), (1182, 542),(867, 570)],

             [(802, 480),
(548, 479),
(481, 567),
(182, 558),
(145, 423),
(166, 247),
(218, 173+20),
(444, 223),
(646, 181),
(754, 186+30),
(790, 312),
(900, 317),
(940, 229-10),
(1040, 194-10),(1154, 210),(1171, 358),(1154, 533),
(903, 578),], [(798, 483), (606, 466), (531, 506), (477, 551), (417, 557),
               (322, 554), (283, 554), (249, 554), (189, 545), (154, 431), (161, 392),
               (161, 392), (161, 389), (154, 326), (150, 258), (188, 202), (243, 181), (309, 191),
               (373, 222), (426, 233), (482, 230), (550, 218), (577, 212), (631, 195), (703, 182),
               (742, 204), (756, 257), (786, 327), (840, 357), (906, 315), (938, 234), (1025, 178),
               (1028, 182), (1086, 182), (1150, 216), (1186, 281), (1187, 331), (1182, 413), (1182, 413),
               (1182, 413), (1186, 461), (1170, 528), (1118, 550), (1046, 547), (896, 558+10)],
             [(663, 565), (610, 562), (550, 550), (530, 506), (514, 427), (490, 387), (458, 360),
              (414, 357), (382, 371), (363, 414), (364, 420), (360, 496), (337, 545), (298, 560),
              (228, 564), (223, 564), (175, 572), (118, 553), (99, 529), (90, 505), (119, 489),
              (175, 485), (216, 467), (244, 445), (247, 423), (246, 368), (229, 322), (212, 291),
              (154, 253), (122, 239), (119, 228), (119, 222), (135, 183), (200, 158), (266, 157),
              (334, 154), (451, 152), (516, 154), (576, 166), (591, 170), (613, 200), (628, 272),
              (630, 366), (654, 408), (731, 367), (738, 310), (742, 245), (787, 205), (820, 194),
              (859, 176), (930, 156), (1001, 150), (1046, 150), (1087, 156), (1146, 166), (1198, 186),
              (1226, 226), (1205, 276), (1133, 310), (1047, 310), (987, 323), (952, 383), (1021, 432),
              (1090, 434), (1181, 473), (1158, 530), (1045, 546)],[(554, 533), (498, 354), (451, 327), (382, 363),
              (362, 532), (297, 577), (148, 569), (251, 470),
              (262, 304), (154, 247), (109, 191),
              (326, 154), (515, 173), (594, 186), (642, 329),
              (713, 419), (767, 262), (824, 177), (1182, 194),
              (1226, 229), (1046, 312), (974, 333), (950, 382), (1014, 421),
              (1130, 432), (1221, 454), (1152, 554)]]
    MONETS = [[Monetka((200, 200)), Monetka((800, 200)), Monetka((500, 450))],[Monetka((812, 525)),
Monetka((561, 489)),
Monetka((370, 566)),
Monetka((195, 195)),
Monetka((650, 194)),
Monetka((1056, 180)),
Monetka((1182, 354))],[Monetka((0,0))]]





    #inicjalizacja zmiennych
    p=1
    #inizjalizacja okna


    #stworzenie gracza i przeciwników

    #stworzenie wszystkich przycisków z jakich będziemy korzystać
    przyciski = []
    przyciski.append(Przycisk((WIN.get_width() / 2, WIN.get_height() / 2-100),
                              pygame.image.load("_internal/naciski\\prz_play.png").convert_alpha(),
                              pygame.image.load("_internal/naciski\\prz_play_akt.png").convert_alpha(),0.7))
    przyciski.append(Przycisk((WIN.get_width() / 2, WIN.get_height() / 2),
                              pygame.image.load("_internal/naciski\\prz_credits.png").convert_alpha(),
                              pygame.image.load("_internal/naciski\\prz_credits_akt.png").convert_alpha(),0.7))
    przyciski.append(Przycisk((WIN.get_width()-170, WIN.get_height() -40),
                              pygame.image.load(f"_internal/naciski\\prz_exit.png").convert_alpha(),
                              pygame.image.load(f"_internal/naciski\\prz_exit_akt.png").convert_alpha(),0.5))
    przyciski.append(Przycisk((WIN.get_width() / 2, WIN.get_height() / 2+250),
                              pygame.image.load("_internal/naciski\\prz_ustaw.png").convert_alpha(),
                              pygame.image.load("_internal/naciski\\prz_ustaw_akt.png").convert_alpha(), 0.7))
    przyciski.append(Przycisk((WIN.get_width() / 2-350, WIN.get_height() /2 -250),
                              pygame.image.load("_internal/naciski\\prz_lvl1.png").convert_alpha(),
                              pygame.image.load("_internal/naciski\\prz_lvl1_akt.png").convert_alpha(), 0.5))
    przyciski.append(Przycisk((WIN.get_width() / 2+350, WIN.get_height() / 2-250),
                              pygame.image.load("_internal/naciski\\prz_lvl2.png").convert_alpha(),
                              pygame.image.load("_internal/naciski\\prz_lvl2_akt.png").convert_alpha(), 0.5))
    przyciski.append(Przycisk((WIN.get_width() / 2, WIN.get_height() / 2-250),
                              pygame.image.load("_internal/naciski\\prz_lvl3.png").convert_alpha(),
                              pygame.image.load("_internal/naciski\\prz_lvl3_akt.png").convert_alpha(), 0.5))
    przyciski.append(Przycisk((WIN.get_width() / 2+300, WIN.get_height() / 2),
                              pygame.image.load("_internal/naciski\\prz_lewo.png").convert_alpha(),
                              pygame.image.load("_internal/naciski\\prz_lewo_akt.png").convert_alpha(), 0.5))
    przyciski.append(Przycisk((WIN.get_width() / 2-300, WIN.get_height() / 2),
                              pygame.image.load("_internal/naciski\\prz_prawo.png").convert_alpha(),
                              pygame.image.load("_internal/naciski\\prz_prawo_akt.png").convert_alpha(), 0.5))
    przyciski.append(Przycisk((WIN.get_width() / 2 , WIN.get_height() / 2+100),
                              pygame.image.load("_internal/naciski\\prz_tabela.png").convert_alpha(),
                              pygame.image.load("_internal/naciski\\prz_tabela_akt.png").convert_alpha(), 0.7))




    #inicjalizacja zmiennych praktycznie ważnych dla gry
    licznik = 5
    tryb = "Main"
    FPS = 40
    run = True
    clock = pygame.time.Clock()

    base_font = pygame.font.Font(None, 60)
    user_text = ''
    input_rect = pygame.Rect(200, 200, 200, 60)
    color_active = pygame.Color('lightskyblue3')
    color_passive = pygame.Color('chartreuse4')
    color = color_passive
    active = False
    countdown = 0

    c = 0
    tablica_wynikow = [["brak",10000,"--"],["brak",10000,"--"],["brak",10000,"--"],["brak",10000,"--"],
                       ["brak",10000,"--"],["brak",10000,"--"],["brak",10000,"--"],["brak",10000,"--"],
                       ["brak",10000,"--"],["brak",10000,"--"]]

    while run:
        #działa ale trch grafiki trzymają

        if tryb == "Credits":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            keys = pygame.key.get_pressed()
            przyciski[2].sprawdz(pygame.mouse.get_pos())
            if przyciski[2].stan == True and (pygame.mouse.get_pressed()[0] == True or keys[pygame.K_RETURN]):
                tryb = "Main"
                pygame.mixer.Sound.play(v_przycisk)

            #rysowanie obiektów
            WIN.blit(creditsy,(0,0))
            przyciski[2].grafika.draw(WIN)
            pygame.display.update()#
        elif tryb == "Main":

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            keys = pygame.key.get_pressed()

            for i in przyciski:
                i.sprawdz(pygame.mouse.get_pos())

            if przyciski[1].stan == True and (pygame.mouse.get_pressed()[0] == True or keys[pygame.K_RETURN]):
                tryb = "Credits"
                pygame.mixer.Sound.play(v_przycisk)

            if przyciski[0].stan == True and (pygame.mouse.get_pressed()[0] == True or keys[pygame.K_RETURN]):
                tryb = "Gra-menu"
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                pygame.mixer.music.load('_internal/dzwieki\\gra.mp3')
                pygame.mixer.music.play(loops=-1, start=0.0, fade_ms=750)

                pygame.mixer.Sound.play(v_przycisk)
            if przyciski[3].stan == True and (pygame.mouse.get_pressed()[0] == True or keys[pygame.K_RETURN]):
                tryb = "Sklep"
                pygame.mixer.Sound.play(v_przycisk)
                RED_CAR = scale_image(pygame.image.load(f"_internal/imgs/auta/pl{obecneauto}.png").convert_alpha(), 3)
            if przyciski[9].stan == True and (pygame.mouse.get_pressed()[0] == True or keys[pygame.K_RETURN]):
                tryb = "Tabela"
                pygame.mixer.Sound.play(v_przycisk)






            WIN.blit(TLO,(0,0))
            for i in przyciski[0:2]+[przyciski[3]]+[przyciski[9]]:
                i.grafika.draw(WIN)
            pygame.display.update()
        elif tryb == "Gra-menu":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            keys = pygame.key.get_pressed()

            for i in przyciski:
                i.sprawdz(pygame.mouse.get_pos())

            if przyciski[4].stan == True and (pygame.mouse.get_pressed()[0] == True )or keys[pygame.K_1]:
                pygame.mixer.Sound.play(v_przycisk)
                game_info = GameInfo()
                tryb = "mars"
                deklaruj("mars",1)
                ilosc_monet = 0
                images = [(GRASS, (0, 0)), (TRACK, (0, 0)),
                          (FINISH, FINISH_POSITION), (BUDYNKI, (0, 0))]
                player_car = PlayerCar(4, 8)
                computercars = [ComputerCar(2, 2, GREEN_CAR, GREEN_CAR_MASK,(888, 599), PATH1 * 3,0, 1 ),
                                ComputerCar(3.3, 6, WHITE_CAR, WHITE_CAR_MASK, (816-10, 578), PATH2 * 3,0,0),
                                ComputerCar(2.5, 3, GREY_CAR, GREY_CAR_MASK,(877, 563), PATH1 * 3,1,1),
                                ComputerCar(4.1, 6, PURPLE_CAR, PURPLE_CAR_MASK,(782, 521), PATH2 * 3,1,0)]
                ufoludek = Ufoludek()
                ufoludek.losujpozycje()
            if przyciski[5].stan == True and (pygame.mouse.get_pressed()[0] == True) or keys[pygame.K_2]:
                pygame.mixer.Sound.play(v_przycisk)
                game_info = GameInfo()
                tryb = "wenus"
                deklaruj("wenus", 2)
                ilosc_monet = 0
                OLEJ = scale_image(pygame.image.load("_internal/imgs/lvl2_plamy.png").convert_alpha(), 0.7)
                OLEJ_MASKA = pygame.mask.from_surface(OLEJ)
                NAWIERZCHNIA = scale_image(pygame.image.load("_internal/imgs/lvl2_nawierzchnie.png").convert_alpha(), 0.7)
                NAWIERZCHNIA_MASKA = pygame.mask.from_surface(NAWIERZCHNIA)
                obecnetornado=0
                TORNADO = [scale_image(pygame.image.load("_internal/imgs/tornada/tornada1.png").convert_alpha(), 0.7),
                           scale_image(pygame.image.load("_internal/imgs/tornada/tornada2.png").convert_alpha(), 0.7),
                           scale_image(pygame.image.load("_internal/imgs/tornada/tornada3.png").convert_alpha(), 0.7)]

                TORNADO_MASKA = pygame.mask.from_surface(TORNADO[0])

                images = [(GRASS, (0, 0)), (TRACK, (0, 0)),
                          (FINISH, FINISH_POSITION), (NAWIERZCHNIA,(0,0)), (OLEJ, (0,0)), (BUDYNKI, (0, 0))]
                player_car = PlayerCar(4, 8)
                computercars = [ComputerCar(2.6, 4, GREEN_CAR, GREEN_CAR_MASK, (903, 582), PATH1 * 3,0,1),
                                ComputerCar(2.9, 4, WHITE_CAR, WHITE_CAR_MASK, (845, 576), PATH1 * 3,1,1),
                                ComputerCar(3.9, 5.5, GREY_CAR, GREY_CAR_MASK, (811, 542), PATH2 * 3,0,0),
                                ComputerCar(4.2, 6, PURPLE_CAR, PURPLE_CAR_MASK, (810, 495), PATH2 * 3,1,0)]
            if przyciski[6].stan == True and (pygame.mouse.get_pressed()[0] == True) or keys[pygame.K_3]:
                pygame.mixer.Sound.play(v_przycisk)
                game_info = GameInfo()
                czysniezy = False
                tryb = "merkury"
                deklaruj("merkury",3)
                OLEJ = scale_image(pygame.image.load("_internal/imgs/lvl3_plamy.png").convert_alpha(), 0.7)
                OLEJ_MASKA = pygame.mask.from_surface(OLEJ)
                NAWIERZCHNIA = scale_image(pygame.image.load("_internal/imgs/lvl3_nawierzchnie.png").convert_alpha(), 0.7)
                NAWIERZCHNIA_MASKA = pygame.mask.from_surface(NAWIERZCHNIA)

                Pajaczek = Pajak()
                ilosc_monet = 0
                images = [(GRASS, (0, 0)), (TRACK, (0, 0)),
                          (FINISH, FINISH_POSITION), (NAWIERZCHNIA, (0, 0)), (OLEJ, (0, 0)), (BUDYNKI, (0, 0))]
                player_car = PlayerCar(4, 8)
                computercars = [ComputerCar(1, 4, GREEN_CAR, GREEN_CAR_MASK, (883, 588-20), PATH1 * 3,1,1),
                                ComputerCar(2.8, 5, WHITE_CAR, WHITE_CAR_MASK, (767, 593-20), PATH2 * 3,0,0),
                                ComputerCar(3, 4, GREY_CAR, GREY_CAR_MASK, (824, 590-20), PATH1 * 3,1,1),
                                ComputerCar(3.5, 6, PURPLE_CAR, PURPLE_CAR_MASK, (714, 590-20), PATH2 * 3,0,0)]

            WIN.blit(h2play,(0,0))
            for i in przyciski[4:7]:
                i.grafika.draw(WIN)
            pygame.display.update()
        elif tryb == "Sklep":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            keys = pygame.key.get_pressed()
            countdown = max(countdown-1,0)
            for i in [2,7,8]:
                przyciski[i].sprawdz(pygame.mouse.get_pos())
            if przyciski[2].stan == True and (pygame.mouse.get_pressed()[0] == True or keys[pygame.K_RETURN]):
                pygame.mixer.Sound.play(v_przycisk)
                tryb = "Main"
                RED_CAR = scale_image(pygame.image.load(f'_internal/imgs/auta/pl{obecneauto}.png').convert_alpha(), 1.2)

            if przyciski[7].stan == True and (pygame.mouse.get_pressed()[0] == True and countdown ==0):
                pygame.mixer.Sound.play(v_przycisk)
                obecneauto+=1
                obecneauto%=9
                countdown = 30
                RED_CAR = scale_image(pygame.image.load(f'_internal/imgs/auta/pl{obecneauto}.png').convert_alpha(), 3)
            if przyciski[8].stan == True and (pygame.mouse.get_pressed()[0] == True and countdown == 0):
                pygame.mixer.Sound.play(v_przycisk)
                obecneauto -= 1
                obecneauto %= 9
                countdown = 30
                RED_CAR = scale_image(pygame.image.load(f'_internal/imgs/auta/pl{obecneauto}.png').convert_alpha(), 3)

            # rysowanie obiektów
            WIN.blit(TLO,(0,0))
            WIN.blit(RED_CAR, (WIN.get_width() / 2, WIN.get_height()/2))
            for i in [2, 7, 8]:
                przyciski[i].grafika.draw(WIN)
            pygame.display.update()

            #RED_CAR = scale_image(pygame.image.load("imgs/auta/pl1.png").convert_alpha(), 1.2)
        elif tryb == "mars":
            #print(computercars[3].x, computercars[3].y,"target:",computercars[3].path[computercars[3].current_point], "kąt", computercars[3].angle, "vel", computercars[3].vel)
            for car in computercars:
                if (car.isaggresive == 1 and (car.x - player_car.x) ** 2 + (car.y - player_car.y) ** 2 <= 4000 and
                    (car.x - player_car.x) ** 2 + (car.y - player_car.y) ** 2 >= 10):
                    car.idzdogracza(player_car.x, player_car.y)
                '''if c%150 == 0:
                    if car.point_before == car.current_point:
                        print("changepoint")
                    else:
                        car.point_before = car.current_point'''

            #print(tryb)
            listamonet = []
            for i in monety:
                listamonet.append((i.img, (i.x, i.y)))
            draw(WIN, images + listamonet+[(ufoludek.Grafiki[ufoludek.grafika], ufoludek.pos)], player_car, computercars, game_info)
            while not game_info.started:
                blit_text_center(
                    WIN, MAIN_FONT, f"Press any key to start level {game_info.level}!")
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        break

                    if event.type == pygame.KEYDOWN:
                        game_info.start_level()

            # print(player_car.bomb.x, player_car.bomb.y)
            c += 1
            c %= 1000

            if c%10 == 0:
                for i in [player_car] + computercars:
                    i.bombaminusczas()
                player_car.turbo_counter -= 1
                ufoludek.zmiengrafike()
                ufoludek.odlicz()
            '''
            if c%100==0:
                pygame.mixer.Sound.play(v_auta)
            '''


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
            if player_car.turbo_counter > 0:
                player_car.max_vel = 10
            else:
                player_car.max_vel = 6


            move_player(player_car)
            for car in computercars:
                car.move_forward()
            # kolizje
            handle_collision(player_car, computercars, game_info)


            for auto in [player_car] + computercars:
                for bomba in [player_car] + computercars:
                    if auto.collide(bomba.bomb.maska, *(bomba.bomb.x, bomba.bomb.y)) != None and bomba.bomb.czas < 9:
                        bomba.wyrzućbombe()
                        auto.reset()
                if auto.collide(ufoludek.Maska, *ufoludek.pos) != None:
                    auto.bounce()
                    ufoludek.czyobudzony=True
                    ufoludek.grafika =3
                    ufoludek.losujpozycje()
                    ufoludek.countdown = 5
                    pygame.mixer.Sound.play(v_ufo)
                if c%20==0:
                    auto.bomb.img= BOMBA1
                elif c%20 == 10:
                    auto.bomb.img = BOMBA2
            for moneta in monety:
                if player_car.collide(MONETA_MASKA, *(moneta.x, moneta.y)) != None:
                    moneta.odrzuć()


            for car in computercars:
                if car.laps >=3:
                    tryb = "Main"
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                    pygame.mixer.music.load('_internal/dzwieki\\menu.mp3')
                    pygame.mixer.music.play(loops=-1, start=0.0, fade_ms=750)
                car.didbounce = 0
            if player_car.laps>=3:
                tablica_wynikow.append(["", game_info.get_level_time(), "I"])
                tryb = ("wpiszTabelka")
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                pygame.mixer.music.load('_internal/dzwieki\\wygrana.mp3')
                pygame.mixer.music.play(loops=-1, start=0.0, fade_ms=750)
        elif tryb == "wenus":
            #print(computercars[3].x, computercars[3].y,"target:",computercars[3].path[computercars[3].current_point], "kąt", computercars[3].angle)
            for car in computercars:
                if (car.isaggresive == 1 and (car.x - player_car.x) ** 2 + (car.y - player_car.y) ** 2 <= 4000 and
                        (car.x - player_car.x) ** 2 + (car.y - player_car.y) ** 2 >= 10):
                    car.idzdogracza(player_car.x, player_car.y)


            #print(tryb)
            listamonet = []
            for i in monety:
                listamonet.append((i.img, (i.x, i.y)))
            draw(WIN, images + listamonet+[(TORNADO[obecnetornado],(0,0))], player_car, computercars, game_info)
            while not game_info.started:
                blit_text_center(
                    WIN, MAIN_FONT, f"Press any key to start level {game_info.level}!")
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        break

                    if event.type == pygame.KEYDOWN:
                        game_info.start_level()

            # print(player_car.bomb.x, player_car.bomb.y)
            c += 1
            c %= 100

            if c%10 == 0:
                for i in [player_car] + computercars:
                    i.bombaminusczas()
                player_car.turbo_counter -= 1
                player_car.countdowntornada = max(player_car.countdowntornada-1, -5)
                obecnetornado+=1
                obecnetornado%=3
                if c%40 ==0 and random.randint(0,4)==3:
                    computercars[random.randint(0,3)].dodajbombe()



            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
            if player_car.turbo_counter > 0:
                player_car.max_vel = 10
            else:
                player_car.max_vel = 6

            handle_collision(player_car, computercars, game_info)
            if player_car.countdowntornada <=0:
                move_player(player_car)
            else:
                player_car.angle+=5
            for car in computercars:
                car.move_forward()
            # kolizje

            for auto in [player_car] + computercars:
                for bomba in [player_car] + computercars:
                    if auto.collide(bomba.bomb.maska, *(bomba.bomb.x, bomba.bomb.y)) != None and bomba.bomb.czas < 9:
                        bomba.wyrzućbombe()
                        auto.reset()
                if auto.collide(OLEJ_MASKA, *(0,0)) != None:
                    auto.angle+=7
                    auto.angle %=360
                    if c%50 ==0:
                        pygame.mixer.Sound.play(v_poslizg)
                if auto.collide(NAWIERZCHNIA_MASKA, *(0,0)) != None:
                    auto.angle+=7*((-1)**random.randint(1,5))
                    auto.angle %=360
                if auto.collide(TORNADO_MASKA, *(0,0)) != None and auto.countdowntornada<=-5:
                    pygame.mixer.Sound.play(v_tornado)
                    auto.countdowntornada=5
                if c%20==0:
                    auto.bomb.img= BOMBA1
                elif c%20 == 10:
                    auto.bomb.img = BOMBA2
            for moneta in monety:
                if player_car.collide(MONETA_MASKA, *(moneta.x, moneta.y)) != None:
                    moneta.odrzuć()


            for car in computercars:
                if car.laps >=3:
                    tryb = "Main"
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                    pygame.mixer.music.load('_internal/dzwieki\\menu.mp3')
                    pygame.mixer.music.play(loops=-1, start=0.0, fade_ms=750)
                    car.didbounce = 0
            if player_car.laps>=3:
                tablica_wynikow.append(["", game_info.get_level_time(), "II"])
                tryb = ("wpiszTabelka")
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                pygame.mixer.music.load('_internal/dzwieki\\wygrana.mp3')
                pygame.mixer.music.play(loops=-1, start=0.0, fade_ms=750)
        elif tryb == "merkury":
            #print(computercars[3].x, computercars[3].y,"target:",computercars[3].path[computercars[3].current_point], "kąt", computercars[3].angle)
            for car in computercars:
                if (car.isaggresive == 1 and (car.x - player_car.x) ** 2 + (car.y - player_car.y) ** 2 <= 4000 and
                        (car.x - player_car.x) ** 2 + (car.y - player_car.y) ** 2 >= 10):
                    car.idzdogracza(player_car.x, player_car.y)
            if c % 40 == 0 and random.randint(0, 4) == 3:
                computercars[random.randint(0, 3)].dodajbombe()


            #print(tryb)
            listamonet = []
            for i in monety:
                listamonet.append((i.img, (i.x, i.y)))
            draw(WIN, images + listamonet+[(Pajaczek.Grafiki[Pajaczek.grafika],Pajaczek.pos)], player_car, computercars, game_info)
            while not game_info.started:
                blit_text_center(
                    WIN, MAIN_FONT, f"Press any key to start level {game_info.level}!")
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        break

                    if event.type == pygame.KEYDOWN:
                        game_info.start_level()

            # print(player_car.bomb.x, player_car.bomb.y)
            c += 1
            c %= 10000

            if c%10 == 0:
                for i in [player_car] + computercars:
                    i.bombaminusczas()
                player_car.turbo_counter -= 1
            if c%5==0:
                obecnysnieg+=1
                obecnysnieg%=5
            if c%3==0:
                Pajaczek.zmiengrafike()
                Pajaczek.idz()
            if c%40 == 0:
                if random.randint(0,30)%6==0:
                    pygame.mixer.Sound.play(v_snieg)
                    czysniezy=True
                else:
                    czysniezy = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
            if player_car.turbo_counter > 0:
                player_car.max_vel = 20
            else:
                player_car.max_vel = 6

            handle_collision(player_car, computercars, game_info)

            move_player(player_car)
            for car in computercars:
                car.move_forward()
            # kolizje

            for auto in [player_car] + computercars:
                for bomba in [player_car] + computercars:
                    if auto.collide(bomba.bomb.maska, *(bomba.bomb.x, bomba.bomb.y)) != None and bomba.bomb.czas < 9:
                        bomba.wyrzućbombe()
                        auto.reset()
                if auto.collide(OLEJ_MASKA, *(0,0)) != None:
                    auto.angle+=7
                    auto.angle %=360
                    if c%50 ==0:
                        pygame.mixer.Sound.play(v_poslizg)
                if auto.collide(NAWIERZCHNIA_MASKA, *(0,0)) != None:
                    auto.move_forward()
                if c%20==0:
                    auto.bomb.img= BOMBA1
                elif c%20 == 10:
                    auto.bomb.img = BOMBA2
                if auto.collide(Pajaczek.Maska, *Pajaczek.pos) != None:
                    pygame.mixer.Sound.play(v_pajak)
                    auto.reset()


            for moneta in monety:
                if player_car.collide(MONETA_MASKA, *(moneta.x, moneta.y)) != None:
                    moneta.odrzuć()


            for car in computercars:

                if car.laps >=3:
                    tryb = "Main"
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                    pygame.mixer.music.load('_internal/dzwieki\\menu.mp3')
                    pygame.mixer.music.play(loops=-1, start=0.0, fade_ms=750)
                    car.didbounce = 0

            if player_car.laps>=3:
                tablica_wynikow.append(["",game_info.get_level_time(), "III"])
                tryb = ("wpiszTabelka")
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                pygame.mixer.music.load('_internal/dzwieki\\wygrana.mp3')
                pygame.mixer.music.play(loops=-1, start=0.0, fade_ms=750)
        elif tryb == ("wpiszTabelka"):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_rect.collidepoint(event.pos):
                        active = True
                    else:
                        active = False
                if event.type == pygame.KEYDOWN:
                    pygame.mixer.Sound.play(v_przycisk)
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode
            WIN.blit(TLO,(0,0))
            if active:
                color = color_active
            else:
                color = color_passive
            pygame.draw.rect(WIN, color, input_rect)
            text_surface = base_font.render(user_text, True, (255, 255, 255))
            WIN.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
            input_rect.w = max(100, text_surface.get_width() + 10)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            keys = pygame.key.get_pressed()
            przyciski[2].sprawdz(pygame.mouse.get_pos())
            if przyciski[2].stan == True and (pygame.mouse.get_pressed()[0] == True or keys[pygame.K_RETURN]):
                tryb = "Tabela"
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                pygame.mixer.music.load('_internal/dzwieki\\menu.mp3')
                pygame.mixer.music.play(loops=-1, start=0.0, fade_ms=750)
                tablica_wynikow[-1][0]=user_text
                tablica_wynikow = sorted(tablica_wynikow, key=lambda a_entry: a_entry[1])[::-1][-10:]

            przyciski[2].grafika.draw(WIN)
            pygame.display.flip()
        elif tryb == "Tabela":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            keys = pygame.key.get_pressed()
            przyciski[2].sprawdz(pygame.mouse.get_pos())
            if przyciski[2].stan == True and (pygame.mouse.get_pressed()[0] == True or keys[pygame.K_RETURN]):
                tryb = "Main"


            # rysowanie obiektów
            WIN.blit(TLO,(0,0))
            delta = 80
            for i in tablica_wynikow:

                level_text = MAIN_FONT.render(f'NAZWA: {i[0]} CZAS: {i[1]}, POZIOM: {i[2]}', 1, (255, 255, 255))
                WIN.blit(level_text, (10, HEIGHT-delta))
                delta +=60

            przyciski[2].grafika.draw(WIN)
            pygame.display.update()  #
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
        clock.tick(FPS)