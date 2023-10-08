import math
from random import randint, randrange
from classes import Rocket, Bullet, Shell
from constants import WHITE, WIDTH, HEIGHT, FPS, BOMB, AY
import pygame


TANK = pygame.image.load('images/tank.png')
TANK.set_colorkey(WHITE)

JET = pygame.image.load('images/jet.png')
JET.set_colorkey(WHITE)

HELICOPTER = pygame.image.load('images/helicopter.png')
HELICOPTER.set_colorkey(WHITE)

class Bomb(Shell):  # class for shells attacks from air weapon
    def __init__(self, x, y, live=1, side_x=50, side_y=50):
        super().__init__(x, y, live, side_x, side_y)

    def draw(self, screen):
        screen.blit(BOMB, (self.x, self.y))

    def move(self):
        if self.y + self.side_y < HEIGHT:
            self.y += AY
        else:
            bombs.remove(self)

class Target:
    def __init__(self, side_x, side_y, vx, vy, points=0, live=1):
        self.side_x = side_x
        self.side_y = side_y
        self.vx = vx
        self.vy = vy
        self.points = points
        self.live = live

    def hit(self, points=1):
        """Missing shell into the goal."""
        self.points += points


class Jet(Target):
    def __init__(self, side_x=90, side_y=90, vx=5, vy=5):
        super().__init__(side_x, side_y, vx, vy, points=0, live=1)
        self.x = randrange(0, WIDTH - self.side_x, 50)
        self.y = 10 + self.side_y

    def draw(self):
        screen.blit(JET, (self.x, self.y))

    def toss_bomb(self):
        if self.x % 300 == 0:
            global mike
            mike += 1
            new_bomb = Bomb(self.x, self.y)
            bombs.append(new_bomb)

    def move(self):
        self.x += self.vx
        if self.x + self.side_x > WIDTH or self.x < 0:
            self.vx *= -1

    def new_jet(self):  # Initialization of new target
        self.live = 1
        self.points = 0
        self.x = randrange(0, WIDTH - self.side_x, 50)
        self.y = 10 + self.side_y


class Helicopter(Target):
    def __init__(self, side_x=90, side_y=90, vx=3, vy=3):
        super().__init__(side_x, side_y, vx, vy, points=0, live=1)
        self.x = randrange(0, WIDTH - self.side_x, 90)
        self.y = randint(0 + self.side_y, 2 * self.side_y)

    def draw(self):
        screen.blit(HELICOPTER, (self.x, self.y))

    def toss_bomb(self):
        if self.x % 300 == 0:
            global mike
            mike += 1
            new_bomb = Bomb(self.x, self.y)
            bombs.append(new_bomb)

    def move(self):
        self.x += self.vx
        self.y += self.vy
        if self.x + self.side_x > WIDTH or self.x < 0:
            self.vx *= -1
        if self.y + self.side_y > HEIGHT / 2 or self.y < 0:
            self.vy *= -1

    def new_helicopter(self):  # Initialization of new helicopter
        self.live = 1
        self.points = 0
        self.x = randrange(0, WIDTH - self.side_x, 90)
        self.y = randint(0 + self.side_y, 2 * self.side_y)


class Tank(Target):
    def __init__(self, side_x=128, side_y=128, vx=5, vy=0):
        super().__init__(side_x, side_y, vx, vy, points=0, live=5)
        self.x = WIDTH - self.side_x
        self.y = HEIGHT - self.side_y
        self.an = 1
        self.f2_power = 10
        self.f2_on = 0
        self.f1_power = 15
        self.f1_on = 0

    def fire1_start(self, eve):
        if eve:
            self.f1_on = 1

    def fire2_start(self, eve):
        if eve:
            self.f2_on = 1

    def fire1_end(self, eve):
        """
        Shooting from Tank
        """
        global rockets, mike
        new_rocket = Rocket(self.x, self.y)
        new_rocket.side_x += 5
        self.an = math.atan2((eve.pos[1] - new_rocket.y), (eve.pos[0] - new_rocket.x))
        new_rocket.vx = self.f1_power * math.cos(self.an)
        new_rocket.vy = - self.f1_power * math.sin(self.an)
        rockets.append(new_rocket)

        self.f1_on = 0
        self.f1_power = 15

    def fire2_end(self, eve):
        """
        Shooting from Tank
        """
        global bullets, mike
        mike += 1
        new_bullet = Bullet(self.x, self.y)
        self.an = math.atan2((eve.pos[1] - new_bullet.y), (eve.pos[0] - new_bullet.x))
        new_bullet.vx = self.f2_power * math.cos(self.an)
        new_bullet.vy = - self.f2_power * math.sin(self.an)
        bullets.append(new_bullet)
        self.f2_on = 0
        self.f2_power = 10

    def targeting(self, eve):
        """Aiming. Depends on mouse position."""
        if eve:
            try:
                self.an = math.atan((event.pos[1] - 450) / (event.pos[0] - 20))
            except ZeroDivisionError:
                pass

    def power_up(self):
        if self.f2_on or self.f1_on:
            if self.f2_power < 100 or self.f1_on < 100:
                self.f2_power += 1
                self.f1_power += 1

    def draw(self):
        screen.blit(TANK, (self.x, self.y))

    def move(self):
        self.x += self.vx
        if self.x + self.side_x > WIDTH or self.x < 0:
            self.vx *= -1

    def new_tank(self):
        self.y = HEIGHT - self.side_y
        self.x = randint(0, WIDTH - self.side_x)
        self.live = 5


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
mike = 0
bullets = []
rockets = []
bombs = []

clock = pygame.time.Clock()
tank1 = Tank()
tank2 = Tank()
target1 = Helicopter()
target2 = Helicopter()
target3 = Jet()
target4 = Jet()
finished = False

while not finished:
    screen.fill(WHITE)
    helicopters = [target1, target2]
    jets = [target3, target4]
    tanks = [tank1, tank2]
    tank1.draw(), tank1.move()
    tank2.draw()
    target1.draw(), target1.move(), target1.toss_bomb()
    target2.draw(), target2.move(), target2.toss_bomb()
    target3.draw(), target3.move(), target3.toss_bomb()
    target4.draw(), target4.move(), target4.toss_bomb()

    for b in bullets:
        if b.live == 0 or b.x > WIDTH or b.x < 0 or b.y < 0 or b.y > HEIGHT:
            bullets.remove(b)
        else:
            b.draw(screen)
    for r in rockets:
        if r.live == 0 or r.x > WIDTH or r.x < 0 or r.y < 0 or r.y > HEIGHT:
            rockets.remove(r)
        else:
            r.draw(screen)
    for bomb in bombs:
        if bomb.live == 0 or bomb.x > WIDTH or bomb.x < 0 or bomb.y < 0 or bomb.y > HEIGHT:
            bombs.remove(bomb)
        else:
            bomb.draw(screen)
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                tank1.fire2_start(event)
            if event.button == 3:
                tank2.fire1_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                tank1.fire2_end(event)
            if event.button == 3:
                tank2.fire1_end(event)
        elif event.type == pygame.MOUSEMOTION:
            tank1.targeting(event)
            tank2.targeting(event)

    for bullet in bullets:
        bullet.move()
        for helicopter in helicopters:
            if bullet.hitting(helicopter) and helicopter.live:
                helicopter.live = 0
                helicopter.hit()
                helicopter.new_helicopter()
        for jet in jets:
            if bullet.hitting(jet) and jet.live:
                jet.live = 0
                jet.hit()
                jet.new_jet()

    for rocket in rockets:
        rocket.move()
        for helicopter in helicopters:
            if rocket.hitting(helicopter) and helicopter.live:
                helicopter.live = 0
                helicopter.hit()
                helicopter.new_helicopter()
        for jet in jets:
            if rocket.hitting(jet) and jet.live:
                jet.live = 0
                jet.hit()
                jet.new_jet()

    for bomb in bombs:
        bomb.move()
        for tank in tanks:
            if bomb.hitting(tank) and tank.live:
                tank.live -= 1
                tank.hit()
                if tank.live == 0:
                    tank.new_tank()

    tank1.power_up()
    tank2.power_up()


pygame.quit()
