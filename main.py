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

def start_screen():
    front_screen = pygame.image.load("Sprites/FrontScreen.png")
    front_screen = pygame.transform.scale(front_screen, (WIDTH, HEIGHT))
    font = pygame.font.SysFont("Arial", 60)
    play_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 50, 300, 100)
    quit_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 200, 300, 100)

    while True:
        screen.blit(front_screen, (0, 0))
        pygame.draw.rect(screen, (0, 0, 0), play_button) 
        pygame.draw.rect(screen, (200, 0, 0), quit_button)
        play_text = font.render("Play", True, (255, 255, 255))
        quit_text = font.render("Quit", True, (255, 255, 255))
        screen.blit(play_text, (play_button.x + 100, play_button.y + 10))
        screen.blit(quit_text, (quit_button.x + 100, quit_button.y + 10))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    return
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    quit()

start_screen()

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

def game_over_screen(winner_text):
    font = pygame.font.SysFont(None, 120)
    small_font = pygame.font.SysFont(None, 60)
    play_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 50, 300, 100)
    quit_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 180, 300, 100)
    while True:
        screen.fill((0, 0, 0))
        text_surface = font.render(winner_text, True, (255, 255, 255))
        screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2 - 100))
        pygame.draw.rect(screen, (255, 255, 255), play_button)
        pygame.draw.rect(screen, (255, 0, 0), quit_button)
        play_text = small_font.render("Play Again", True, (0, 0, 0))
        quit_text = small_font.render("Quit", True, (255, 255, 255))
        screen.blit(play_text, (play_button.x + 50, play_button.y + 30))
        screen.blit(quit_text, (quit_button.x + 100, quit_button.y + 30))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    return True
                elif quit_button.collidepoint(event.pos):
                    return False
        pygame.display.flip()

running = True

while running:
    delta_time = clock.tick(60) / 1000.0
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        player1.get_event(event) 
        player2.get_event(event)
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
    keys = pygame.key.get_pressed()
    player1.update(keys, delta_time, player2, boxes)
    player2.update(keys, delta_time, player1, boxes)
    for box in boxes:
        box.update()
        box.draw(screen)
    player1.draw(screen)
    player2.draw(screen)
    if player1.health <= 0:
        if not game_over_screen("Player Blue has won!"):
            running = False
        else:
            player1 = Player("Sprites/PlayerRed.png", 100, HEIGHT // 2, {
                "up": pygame.K_w, "down": pygame.K_s, "left": pygame.K_a, "right": pygame.K_d, "shoot": pygame.K_e
            }, direction=1, boundary=boundary)

            player2 = Player("Sprites/PlayerBlue.png", WIDTH - 150, HEIGHT // 2, {
                "up": pygame.K_UP, "down": pygame.K_DOWN, "left": pygame.K_LEFT, "right": pygame.K_RIGHT, "shoot": pygame.K_SPACE
            }, direction=-1, boundary=boundary)
            boxes = generate_boxes()

    if player2.health <= 0:
        if not game_over_screen("Player Red has won!"):
            running = False
        else:
            player1 = Player("Sprites/PlayerRed.png", 100, HEIGHT // 2, {
                "up": pygame.K_w, "down": pygame.K_s, "left": pygame.K_a, "right": pygame.K_d, "shoot": pygame.K_e
            }, direction=1, boundary=boundary)
            player2 = Player("Sprites/PlayerBlue.png", WIDTH - 150, HEIGHT // 2, {
                "up": pygame.K_UP, "down": pygame.K_DOWN, "left": pygame.K_LEFT, "right": pygame.K_RIGHT, "shoot": pygame.K_SPACE
            }, direction=-1, boundary=boundary)
            boxes = generate_boxes()
    pygame.display.flip()
    
pygame.quit()