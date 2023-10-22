# classes of the game.
import pygame
import math
from random import randint, randrange
from constants import ROCKET, BULLET, BOMB, HEIGHT, AY, WIDTH, JET, HELICOPTER, TANK


class Shell():

    def __init__(self, x, y, live, side_x, side_y):
        """ class Shell - the parent clas for all types of a shells.
        """
        self.screen =pygame.Surface
        self.x = x
        self.y = y
        self.live = live
        self.side_x = side_x
        self.side_y = side_y
        self.vx = 10
        self.vy = 10


    def hitting(self, obj):
        """The function checks if the given object collides with the target described in the object. obj.

        Args:
            obj: The object to check for collision.
        Returns:
            Returns True if the ball and the target collide. Otherwise, returns False.
        """
        if (self.x + self.side_x >= obj.x and self.x <= obj.x + obj.side_x
                and self.y <= obj.y + obj.side_y and self.y + self.side_y >= obj.y):
            self.live = 0
            return True
        else:
            return False
        

class Rocket(Shell):
    def __init__(self, x, y, live=1, side_x=32, side_y=32):
        """ class Rocket - the parent clas for tanks weapon
        """
        super().__init__(x, y, live, side_x, side_y)

    def draw(self, screen):
        """
        Self-drawning of the Rocket
        """
        screen.blit(ROCKET, (self.x, self.y))
        
    
    def move(self):
        """
        Moving the TanksRocket with speed vx and vy
        """
        self.x += self.vx
        self.y -= self.vy


class Bullet(Shell):
    def __init__(self, x, y, live=1, side_x=32, side_y=32):
        super().__init__(x, y, live, side_x, side_y)

    def draw(self, screen):
        screen.blit(BULLET, (self.x, self.y))
    
    def move(self):
        """
        Moving the TanksBullet with speed vx and vy
        """
        self.x += self.vx
        self.y -= self.vy


class Bomb(Shell):  # class for shells attacks from air weapon

    def __init__(self, x, y, live=1, side_x=50, side_y=50):
        super().__init__(x, y, live, side_x, side_y)

    def draw(self, screen):
        screen.blit(BOMB, (self.x, self.y))

    def move(self):
        if self.y + self.side_y < HEIGHT:
            self.y += AY
        

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

    def draw(self, screen):
        screen.blit(JET, (self.x, self.y))

    def toss_bomb(self, score, bombs):
        if self.x % 300 == 0:
            score += 1
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

    def draw(self, screen):
        screen.blit(HELICOPTER, (self.x, self.y))

    def toss_bomb(self, score, bombs):
        if self.x % 300 == 0:
            score += 1
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

    def fire1_end(self, eve, rockets, score):
        """
        Shooting from Tank
        """

        new_rocket = Rocket(self.x, self.y)
        new_rocket.side_x += 5
        self.an = math.atan2((eve.pos[1] - new_rocket.y), (eve.pos[0] - new_rocket.x))
        new_rocket.vx = self.f1_power * math.cos(self.an)
        new_rocket.vy = - self.f1_power * math.sin(self.an)
        rockets.append(new_rocket)

        self.f1_on = 0
        self.f1_power = 15

    def fire2_end(self, eve, bullets, score):
        """
        Shooting from Tank
        """
        score += 1
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
                self.an = math.atan((eve.pos[1] - 450) / (eve.pos[0] - 20))
            except ZeroDivisionError:
                pass

    def power_up(self):
        if self.f2_on or self.f1_on:
            if self.f2_power < 100 or self.f1_on < 100:
                self.f2_power += 1
                self.f1_power += 1

    def draw(self, screen):
        screen.blit(TANK, (self.x, self.y))

    def move(self):
        self.x += self.vx
        if self.x + self.side_x > WIDTH or self.x < 0:
            self.vx *= -1

    def new_tank(self):
        self.y = HEIGHT - self.side_y
        self.x = randint(0, WIDTH - self.side_x)
        self.live = 5
