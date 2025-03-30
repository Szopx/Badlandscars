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

    def bounce(self):
        self.vel = -self.vel
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
        #print("ok?")
        if self.bomb_limit!=0:
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
        self.x, self.y = (900,520)
        self.img = RED_CAR
        self.START_POS = (900,520)
        self.MASK= RED_CAR_MASK
        self.turbo_counter = 0
    def turbo(self):
        self.turbo_counter=5
        global ilosc_monet
        if ilosc_monet>=5:
            ilosc_monet -=5

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
        self.img = BOMBA
        self.maska = BOMBA_MASKA
        self.x, self.y = pos
        self.czas = 0

class ComputerCar(AbstractCar):
    def __init__(self, max_vel, rotation_vel, IMG, MASK, START_POS,path = [], isaggresive = 0, ismistrzprostej = 1):
        super().__init__(max_vel, rotation_vel)
        self.path = path
        self.current_point = 0
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

    def calculate_angle(self):
        target_x, target_y = self.path[self.current_point]
        x_diff = target_x - self.x
        y_diff = target_y - self.y

        if y_diff == 0:
            desired_radian_angle = math.pi / 2
        else:
            desired_radian_angle = math.atan(x_diff / y_diff)

        if target_y > self.y:
            desired_radian_angle += math.pi

        difference_in_angle = self.angle - math.degrees(desired_radian_angle)
        if difference_in_angle >= 180:
            difference_in_angle -= 360

        if difference_in_angle > 0:
            self.angle -= min(self.rotation_vel, abs(difference_in_angle))
        else:
            self.angle += min(self.rotation_vel, abs(difference_in_angle))

    def update_path_point(self):
        target = self.path[self.current_point]
        rect = pygame.Rect(
            self.x, self.y, self.img.get_width(), self.img.get_height())
        if rect.collidepoint(*target):
            self.current_point += 1

    def move(self):
        if self.current_point >= len(self.path):
            return
        self.calculate_angle()
        self.update_path_point()
        super().move()

    def next_level(self, level):
        self.reset()
        self.vel = self.max_vel + (level - 1) * 0.2
        self.current_point = 0

def draw(win, images, player_car, computer_cars, game_info):
    global ilosc_monet
    for img, pos in images:
        win.blit(img, pos)

    level_text = MAIN_FONT.render(
        f"My Laps {player_car.laps}", 1, (255, 255, 255))
    win.blit(level_text, (10, HEIGHT - level_text.get_height() - 70))

    time_text = MAIN_FONT.render(
        f"Rest Laps: 1 - {computer_cars[0].laps}; 2 - {computer_cars[1].laps}"
        f"3 - {computer_cars[2].laps}4 -{computer_cars[3].laps}", 1, (255, 255, 255))
    win.blit(time_text, (10, HEIGHT - time_text.get_height() - 40))

    forsa= MAIN_FONT.render(
    f"MONEY {ilosc_monet}", 1, (255, 255, 255))
    win.blit(forsa, (10, HEIGHT - level_text.get_height() - 90))

    for computer_car in computer_cars+[player_car]:
        computer_car.draw(win)
        win.blit(BOMBA, (player_car.bomb.x, player_car.bomb.y))
    pygame.display.update()

def deklaruj(tekst, n):
    global TRACK, GRASS, BUDYNKI, TRACK_BORDER, TRACK_BORDER_MASK, FINISH, FINISH_MASK, PATH1, PATH2, monety
    fact = 0.7
    TRACK = scale_image(pygame.image.load(f'imgs/{tekst}-trasa.png').convert_alpha(), fact)
    GRASS = scale_image(pygame.image.load(f'imgs/{tekst}-tlo.png').convert_alpha(), fact)
    BUDYNKI = scale_image(pygame.image.load(f'imgs/{tekst}-infrastruktura.png').convert_alpha(), fact)
    TRACK_BORDER = scale_image(pygame.image.load(f'imgs/{tekst}-trasa-outline.png'), fact)
    TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
    FINISH = scale_image(pygame.image.load(f'imgs/{tekst}-meta.png'), fact)
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
    if keys[pygame.K_r]:
        player_car.przerzut()
    if keys[pygame.K_q]:
        print(pygame.mouse.get_pos())
    if keys[pygame.K_x]:
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
        if x.collide(OLEJ_MASKA) != None and tryb == "mars":
            x.rotate(right=True)
    for m in computercars:
        computer_finish_poi_collide = m.collide(
            FINISH_MASK, *FINISH_POSITION)
        if computer_finish_poi_collide != None:
            if computer_finish_poi_collide[0]!=943:
                m.laps+=1
                m.reset()
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

def deklaruj(tekst, n):
    global TRACK, GRASS, BUDYNKI, TRACK_BORDER, TRACK_BORDER_MASK, FINISH, FINISH_MASK, PATH1, PATH2, monety
    fact = 0.7
    TRACK = scale_image(pygame.image.load(f'imgs/{tekst}-trasa.png').convert_alpha(), fact)
    GRASS = scale_image(pygame.image.load(f'imgs/{tekst}-tlo.png').convert_alpha(), fact)
    BUDYNKI = scale_image(pygame.image.load(f'imgs/{tekst}-infrastruktura.png').convert_alpha(), fact)
    TRACK_BORDER = scale_image(pygame.image.load(f'imgs/{tekst}-trasa-outline.png'), fact)
    TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
    FINISH = scale_image(pygame.image.load(f'imgs/{tekst}-meta.png'), fact)
    FINISH_MASK = pygame.mask.from_surface(FINISH)
    PATH1 = PATHS[2 * n - 2]
    PATH2 = PATHS[2 * n - 1]
    monety = MONETS[n - 1]




if __name__ == "__main__":


    pygame.font.init()
    fact = 0.7

    TRACK = scale_image(pygame.image.load("imgs/mars-trasa.png"), 0.7)
    WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Rewolucyjne Autka")

    FINISH_POSITION = (0, 0)
    BOMBA = scale_image(pygame.image.load("imgs/bomb.png"), 2)
    BOMBA_MASKA = pygame.mask.from_surface(BOMBA)
    MONETA = scale_image(pygame.image.load("imgs/monetka.png"), 0.05)
    MONETA_MASKA = pygame.mask.from_surface(MONETA)
    RED_CAR = scale_image(pygame.image.load("imgs/red-car0.png").convert_alpha(), 0.4)
    RED_CAR_MASK = pygame.mask.from_surface(RED_CAR)
    GREEN_CAR = scale_image(pygame.image.load("imgs/green-car.png"), 0.4)
    GREEN_CAR_MASK = pygame.mask.from_surface(GREEN_CAR)
    PURPLE_CAR = scale_image(pygame.image.load("imgs/purple-car.png"), 0.4)
    PURPLE_CAR_MASK = pygame.mask.from_surface(GREEN_CAR)
    WHITE_CAR = scale_image(pygame.image.load("imgs/white-car.png"), 0.4)
    WHITE_CAR_MASK = pygame.mask.from_surface(GREEN_CAR)
    GREY_CAR = scale_image(pygame.image.load("imgs/grey-car.png"), 0.4)
    GREY_CAR_MASK = pygame.mask.from_surface(GREEN_CAR)
    OLEJ = scale_image(pygame.image.load("imgs/olej.png"), 0.7)
    OLEJ_MASKA = pygame.mask.from_surface(OLEJ)

    MAIN_FONT = pygame.font.SysFont("comicsans", 44)

    (TRACK, GRASS, BUDYNKI, TRACK_BORDER, TRACK_BORDER_MASK,
     FINISH, FINISH_MASK, PATH1, PATH2,monety) = (0 for i in range(10))







    PATHS = [[(778, 551), (733, 469), (604, 432), (449, 431),
              (266, 442), (170, 406), (111, 337), (142, 264),
              (205, 226), (237, 202), (358, 193), (421, 194),
              (521, 199), (941, 190), (1042, 215), (1134, 216),
              (1202, 225), (1236, 257), (1236, 310), (1199, 365),
              (1149, 428), (1123, 485), (1040, 559), (930, 571)], [(778, 551), (604, 432), (449, 431),
                                                                   (266, 442), (170, 406), (111, 337), (142, 264),
                                                                   (205, 226), (237, 202), (358, 193), (421, 194),
                                                                   (521, 199), (941, 190), (1042, 215), (1134, 216),
                                                                   (1202, 225), (1236, 257), (1236, 310), (1199, 365),
                                                                   (1149, 428), (1123, 485), (1040, 559), (930, 571)]]*3
    MONETS = [[Monetka((200, 200)), Monetka((800, 200)), Monetka((500, 450))]]*3




    #inicjalizacja zmiennych
    p=1
    #inizjalizacja okna


    #stworzenie gracza i przeciwników

    #stworzenie wszystkich przycisków z jakich będziemy korzystać
    przyciski = []
    przyciski.append(Przycisk((WIN.get_width() / 2, WIN.get_height() / 2-100),
                              pygame.image.load("naciski\\start0.png").convert_alpha(),
                              pygame.image.load("naciski\\start1.png").convert_alpha(),0.5))
    przyciski.append(Przycisk((WIN.get_width() / 2-200, WIN.get_height() / 2-10),
                              pygame.image.load("naciski\\credits0.png").convert_alpha(),
                              pygame.image.load("naciski\\credits1.png").convert_alpha(),0.5))

    przyciski.append(Przycisk((WIN.get_width()-50, WIN.get_height() -50),
                              pygame.image.load(f"naciski\\exit0.png").convert_alpha(),
                              pygame.image.load(f"naciski\\exit1.png").convert_alpha(),0.5))
    przyciski.append(Przycisk((WIN.get_width() / 2, WIN.get_height() / 2+83),
                              pygame.image.load("naciski\\sklep0.png").convert_alpha(),
                              pygame.image.load("naciski\\sklep1.png").convert_alpha(), 0.5))
    przyciski.append(Przycisk((WIN.get_width() / 2, WIN.get_height() / 2+83),
                              pygame.image.load("naciski\\lvlpierwszy0.png").convert_alpha(),
                              pygame.image.load("naciski\\lvlpierwszy1.png").convert_alpha(), 0.5))
    przyciski.append(Przycisk((WIN.get_width() / 2-100, WIN.get_height() / 2+83),
                              pygame.image.load("naciski\\lvldrugi0.png").convert_alpha(),
                              pygame.image.load("naciski\\lvldrugi1.png").convert_alpha(), 0.5))
    przyciski.append(Przycisk((WIN.get_width() / 2+100, WIN.get_height() / 2+83),
                              pygame.image.load("naciski\\lvltrzeci0.png").convert_alpha(),
                              pygame.image.load("naciski\\lvltrzeci1.png").convert_alpha(), 0.5))



    #inicjalizacja zmiennych praktycznie ważnych dla gry
    licznik = 5
    tryb = "Gra-menu"
    FPS = 60
    run = True
    clock = pygame.time.Clock()

    base_font = pygame.font.Font(None, 32)
    user_text = ''
    input_rect = pygame.Rect(200, 200, 140, 32)
    color_active = pygame.Color('lightskyblue3')
    color_passive = pygame.Color('chartreuse4')
    color = color_passive
    active = False

    game_info = GameInfo()
    c = 0
    #tablica wynikow = [["blank"],["blank"],["blank"]]


    deklaruj("mars",1)

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

            #rysowanie obiektów
            WIN.fill((0, 0, 0))
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

            if przyciski[0].stan == True and (pygame.mouse.get_pressed()[0] == True or keys[pygame.K_RETURN]):
                tryb = "Gra-menu"
            if przyciski[3].stan == True and (pygame.mouse.get_pressed()[0] == True or keys[pygame.K_RETURN]):
                tryb = "Sklep"






            WIN.fill((0, 0, 0))
            for i in przyciski[0:2]+[przyciski[3]]:
                i.grafika.draw(WIN)
            font = pygame.font.SysFont('sylfaen', 30)
            lo = font.render("^twój statek wygląda tak^", 10, (200,200,200))
            l4 = font.render("twoje gwiazdki: ", 10, (255, 255, 255))
            WIN.blit(l4, (WIN.get_width()/2-120,WIN.get_height()-40))
            WIN.blit(lo, (WIN.get_width() / 2 - 160, WIN.get_height() - 80))
            pygame.display.update()
        elif tryb == "Gra-menu":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            keys = pygame.key.get_pressed()

            for i in przyciski:
                i.sprawdz(pygame.mouse.get_pos())

            if przyciski[4].stan == True and (pygame.mouse.get_pressed()[0] == True or keys[pygame.K_RETURN]):
                tryb = "mars"
                deklaruj("mars",1)
                ilosc_monet = 0
                images = [(GRASS, (0, 0)), (TRACK, (0, 0)),
                          (FINISH, FINISH_POSITION), (BUDYNKI, (0, 0))]
                player_car = PlayerCar(4, 8)
                computercars = [ComputerCar(1, 4, GREEN_CAR, GREEN_CAR_MASK, (900, 590), PATH1 * 3,0,0),
                                ComputerCar(2, 4, WHITE_CAR, WHITE_CAR_MASK, (880, 560), PATH1 * 3,0,1),
                                ComputerCar(1, 4, GREY_CAR, GREY_CAR_MASK, (830, 530), PATH2 * 3,1,0),
                                ComputerCar(1, 4, PURPLE_CAR, PURPLE_CAR_MASK, (800, 510), PATH2 * 3,1,1)]

            if przyciski[5].stan == True and (pygame.mouse.get_pressed()[0] == True or keys[pygame.K_RETURN]):
                tryb = "wenus"
                deklaruj("wenus",2)

                ilosc_monet = 0
                images = [(GRASS, (0, 0)), (TRACK, (0, 0)),
                          (FINISH, FINISH_POSITION), (BUDYNKI, (0, 0))]
                player_car = PlayerCar(4, 8)
                computercars = [ComputerCar(2, 4, GREEN_CAR, GREEN_CAR_MASK, (870, 590), PATH1 * 3),
                                ComputerCar(2, 4, WHITE_CAR, WHITE_CAR_MASK, (880, 560), PATH1 * 3),
                                ComputerCar(2, 4, GREY_CAR, GREY_CAR_MASK, (850, 530), PATH2 * 3),
                                ComputerCar(2, 4, PURPLE_CAR, PURPLE_CAR_MASK, (840, 510), PATH2 * 3)]
            if przyciski[6].stan == True and (pygame.mouse.get_pressed()[0] == True or keys[pygame.K_RETURN]):
                tryb = "merkury"
                deklaruj("merkury",3)

                ilosc_monet = 0
                images = [(GRASS, (0, 0)), (TRACK, (0, 0)),
                          (FINISH, FINISH_POSITION), (BUDYNKI, (0, 0))]
                player_car = PlayerCar(4, 8)
                computercars = [ComputerCar(2, 4, GREEN_CAR, GREEN_CAR_MASK, (870, 590), PATH1 * 3),
                                ComputerCar(2, 4, WHITE_CAR, WHITE_CAR_MASK, (880, 560), PATH1 * 3),
                                ComputerCar(2, 4, GREY_CAR, GREY_CAR_MASK, (850, 530), PATH2 * 3),
                                ComputerCar(2, 4, PURPLE_CAR, PURPLE_CAR_MASK, (840, 510), PATH2 * 3)]

            WIN.fill((0, 0, 0))
            for i in przyciski[4:7]:
                i.grafika.draw(WIN)
            pygame.display.update()
        elif tryb == "Sklep":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
        elif tryb == "mars":
            for car in computercars:
                if car.isaggresive == 1 and (car.x - player_car.x) ** 2 + (car.y - player_car.y) ** 2 <= 400:
                    pass  #nie mam pojęcia jak zrobić


            #print(tryb)
            listamonet = []
            for i in monety:
                listamonet.append((i.img, (i.x, i.y)))
            draw(WIN, images + listamonet+[(OLEJ,(0,0))], player_car, computercars, game_info)
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
            c %= 10

            if c == 0:
                for i in [player_car] + computercars:
                    i.bombaminusczas()
                player_car.turbo_counter -= 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
            if player_car.turbo_counter > 0:
                player_car.max_vel = 12
            else:
                player_car.max_vel = 8


            move_player(player_car)
            for car in computercars:
                car.move_forward()
            # kolizje

            for auto in [player_car] + computercars:
                for bomba in [player_car] + computercars:
                    if auto.collide(BOMBA_MASKA, *(bomba.bomb.x, bomba.bomb.y)) != None and bomba.bomb.czas < 9:
                        bomba.wyrzućbombe()
                        auto.reset()
            for moneta in monety:
                if player_car.collide(MONETA_MASKA, *(moneta.x, moneta.y)) != None:
                    moneta.odrzuć()

            handle_collision(player_car, computercars, game_info)
            for car in computercars:
                if car.laps >=3:
                    print("Lamus")
                    tryb = "Main"
            if player_car.laps>=3:
                print("Essa")
                tryb = "Tabelka"
        elif tryb == "wenus":
            listamonet = []
            for i in monety:
                listamonet.append((i.img, (i.x, i.y)))
            draw(WIN, images + listamonet, player_car, computercars, game_info)
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
            c %= 10

            if c == 0:
                for i in [player_car] + computercars:
                    i.bombaminusczas()
                player_car.turbo_counter -= 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
            if player_car.turbo_counter > 0:
                player_car.max_vel = 12
            else:
                player_car.max_vel = 8
            move_player(player_car)
            for car in computercars:
                car.move()
            # kolizje

            for auto in [player_car] + computercars:
                for bomba in [player_car] + computercars:
                    if auto.collide(BOMBA_MASKA, *(bomba.bomb.x, bomba.bomb.y)) != None and bomba.bomb.czas < 9:
                        bomba.wyrzućbombe()
                        auto.reset()
            for moneta in monety:
                if player_car.collide(MONETA_MASKA, *(moneta.x, moneta.y)) != None:
                    moneta.odrzuć()

            handle_collision(player_car, computercars, game_info)
            for car in computercars:
                if car.laps >= 3:
                    print("Lamus")
                    tryb = "Main"
            if player_car.laps >= 3:
                print("Essa")
                tryb = "Tabelka"
        elif tryb == "merkury":
            listamonet = []
            for i in monety:
                listamonet.append((i.img, (i.x, i.y)))
            draw(WIN, images + listamonet, player_car, computercars, game_info)
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
            c %= 10

            if c == 0:
                for i in [player_car] + computercars:
                    i.bombaminusczas()
                player_car.turbo_counter -= 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
            if player_car.turbo_counter > 0:
                player_car.max_vel = 12
            else:
                player_car.max_vel = 8
            move_player(player_car)
            for car in computercars:
                car.move()
            # kolizje

            for auto in [player_car] + computercars:
                for bomba in [player_car] + computercars:
                    if auto.collide(BOMBA_MASKA, *(bomba.bomb.x, bomba.bomb.y)) != None and bomba.bomb.czas < 9:
                        bomba.wyrzućbombe()
                        auto.reset()
            for moneta in monety:
                if player_car.collide(MONETA_MASKA, *(moneta.x, moneta.y)) != None:
                    moneta.odrzuć()

            handle_collision(player_car, computercars, game_info)
            for car in computercars:
                if car.laps >= 3:
                    print("Lamus")
                    tryb = "Main"
            if player_car.laps >= 3:
                print("Essa")
                tryb = "Tabelka"
        elif tryb == "Tabelka":
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
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode
            WIN.fill((255, 255, 255))
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
                tryb = "Main"
                print(user_text)

            przyciski[2].grafika.draw(WIN)
            pygame.display.flip()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
        clock.tick(FPS)