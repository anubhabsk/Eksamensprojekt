import pygame
from player import Player
from pygame.locals import *
from boundary import Boundary

pygame.init()
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT), SCALED | FULLSCREEN)
pygame.display.set_caption("Blast Buddies")

# Load baggrundsbillede
background = pygame.image.load("Sprites/Background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
# Create boundary instance
boundary = Boundary(WIDTH, HEIGHT)

# FPS
FPS = 30
clock = pygame.time.Clock()

# Spillere
player1 = Player("Sprites/PlayerRed.png", 100, HEIGHT // 2, {
    "up": pygame.K_w, "down": pygame.K_s, "left": pygame.K_a, "right": pygame.K_d, "shoot": pygame.K_e
}, direction = 1, boundary = boundary)

player2 = Player("Sprites/PlayerBlue.png", WIDTH - 150, HEIGHT // 2, {
    "up": pygame.K_UP, "down": pygame.K_DOWN, "left": pygame.K_LEFT, "right": pygame.K_RIGHT, "shoot": pygame.K_SPACE
}, direction = -1, boundary = boundary)

# Game loop
running = True
while running:
    delta_time = clock.tick(60) / 1000.0  # 60 FPS, konverteret til sekunder

    # Tegn baggrund
    screen.blit(background, (0, 0))

    # Event håndtering
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            player1.get_event(event)
            player2.get_event(event)

    # Opdater spillere
    keys = pygame.key.get_pressed()
    player1.update(keys, delta_time, player2)
    player2.update(keys, delta_time, player1)

    # Tegn spillere
    player1.draw(screen)
    player2.draw(screen)

    pygame.display.flip()  # Opdater skærmen

pygame.quit()