import pygame
from bullet import Bullet

PLAYER_SPEED = 300
PLAYER_HP = 3

class Player:
    def __init__(self, image_path, start_x, start_y, controls, direction):
        self.image = pygame.image.load(image_path).convert_alpha()  
        self.rect = self.image.get_rect(center=(start_x, start_y))
        
        self.speed = PLAYER_SPEED
        self.bullets = []
        self.health = PLAYER_HP
        self.controls = controls
        self.direction = direction  

    def get_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == self.controls["shoot"]:
            bullet_start = self.rect.midright if self.direction == 1 else self.rect.midleft
            self.bullets.append(Bullet(bullet_start, self.direction))

    def update(self, keys, dt):

        if keys[self.controls["up"]]:
            self.rect.y -= self.speed * dt
        if keys[self.controls["down"]]:
            self.rect.y += self.speed * dt
        if keys[self.controls["left"]]:
            self.rect.x -= self.speed * dt
        if keys[self.controls["right"]]:
            self.rect.x += self.speed * dt

        self.bullets = [bullet for bullet in self.bullets if not bullet.is_off_screen(1920)]
        for laser in self.bullets:
            laser.update(dt)
        
    def draw(self, surf):
        for bullet in self.bullets:
            bullet.render(surf)
        surf.blit(self.image, self.rect)