# classes of the game.
import pygame
from constants import ROCKET, BULLET, BOMB, HEIGHT, AY


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