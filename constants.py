import pygame

# screen color

WHITE = 0xFFFFFF

# images of game
ROCKET = pygame.image.load('images/rocket.png')
ROCKET.set_colorkey(WHITE)

BULLET = pygame.image.load('images/bullet.png')
BULLET.set_colorkey(WHITE)

BOMB = pygame.image.load('images/bomb.png')
BOMB.set_colorkey(WHITE)

TANK = pygame.image.load('images/tank.png')
TANK.set_colorkey(WHITE)

JET = pygame.image.load('images/jet.png')
JET.set_colorkey(WHITE)

HELICOPTER = pygame.image.load('images/helicopter.png')
HELICOPTER.set_colorkey(WHITE)