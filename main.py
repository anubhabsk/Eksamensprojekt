import pygame
from player import Player
from pygame.locals import *
from boundary import Boundary
from box import Box
import random

pygame.init()
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT), SCALED | FULLSCREEN)
pygame.display.set_caption("Blast Buddies")

background = pygame.image.load("Sprites/Background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
boundary = Boundary(WIDTH, HEIGHT)
FPS = 30
clock = pygame.time.Clock()

player1 = Player("Sprites/PlayerRed.png", 100, HEIGHT // 2, {
    "up": pygame.K_w, "down": pygame.K_s, "left": pygame.K_a, "right": pygame.K_d, "shoot": pygame.K_e
}, direction=1, boundary=boundary)

player2 = Player("Sprites/PlayerBlue.png", WIDTH - 150, HEIGHT // 2, {
    "up": pygame.K_UP, "down": pygame.K_DOWN, "left": pygame.K_LEFT, "right": pygame.K_RIGHT, "shoot": pygame.K_SPACE
}, direction=-1, boundary=boundary)

def generate_boxes():
    boxes = []
    for _ in range(3):
        x = random.randint(100, WIDTH // 2 - 100)
        y = random.randint(100, HEIGHT - 100)
        boxes.append(Box(x, y))

    for _ in range(3):
        x = random.randint(WIDTH // 2 + 100, WIDTH - 100)
        y = random.randint(100, HEIGHT - 100)
        boxes.append(Box(x, y))

    return boxes

boxes = generate_boxes()

running = True
while running:
    delta_time = clock.tick(60) / 1000.0  
    screen.blit(background, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            player1.get_event(event)
            player2.get_event(event)

    keys = pygame.key.get_pressed()
    
    player1.update(keys, delta_time, player2, boxes)  
    player2.update(keys, delta_time, player1, boxes)  

    for box in boxes:
        box.update()
        box.draw(screen)

    player1.draw(screen)
    player2.draw(screen)

    pygame.display.flip()

pygame.quit()
