from classes import Jet, Helicopter, Tank
from constants import WHITE
import pygame


WIDTH = 800
HEIGHT = 600
FPS = 30 #velosity of screen updating

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
score = 0
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
    tank1.draw(screen), tank1.move()
    tank2.draw(screen)
    target1.draw(screen), target1.move(), target1.toss_bomb(score, bombs)
    target2.draw(screen), target2.move(), target2.toss_bomb(score, bombs)
    target3.draw(screen), target3.move(), target3.toss_bomb(score, bombs)
    target4.draw(screen), target4.move(), target4.toss_bomb(score, bombs)

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
                tank1.fire2_end(event, bullets, score)
            if event.button == 3:
                tank2.fire1_end(event, rockets, score)
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
        if bomb.move() == False:
             bombs.remove(bomb)
        for tank in tanks:
            if bomb.hitting(tank) and tank.live:
                tank.live -= 1
                tank.hit()
                if tank.live == 0:
                    tank.new_tank()

    tank1.power_up()
    tank2.power_up()


pygame.quit()
