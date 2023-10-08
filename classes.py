# classes of the game.
import pygame
from constants import ROCKET, BULLET, BOMB, HEIGHT, AY, WIDTH, JET, HELICOPTER
from random import randint, randrange


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
        else:
            return False
        

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