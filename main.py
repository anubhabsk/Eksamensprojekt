import pygame
from player import Player

# Initialiser pygame
pygame.init()

# Skærmstørrelse (matcher baggrundsbilledet)
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D PvP Shooter")

# Load baggrundsbillede
background = pygame.image.load("Sprites/Background.png")

# FPS
clock = pygame.time.Clock()

# Spillere
player1 = Player(100, HEIGHT // 2, (0, 0, 255))  # Blå spiller
player2 = Player(WIDTH - 150, HEIGHT // 2, (255, 0, 0))  # Rød spiller

# Game loop
running = True
while running:
    clock.tick(60)  # 60 FPS
    
    # Tegn baggrund
    screen.blit(background, (0, 0))

    # Event håndtering
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Opdater spillere
    keys = pygame.key.get_pressed()
    player1.update(keys, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d)
    player2.update(keys, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)

    # Tegn spillere
    player1.draw(screen)
    player2.draw(screen)

    pygame.display.flip()  # Opdater skærmen

pygame.quit()
