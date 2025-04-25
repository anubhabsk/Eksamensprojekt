import pygame
from bullet import Bullet
from boundary import Boundary
 
PLAYER_SPEED = 300
PLAYER_HP = 3
HEART_SPACING = 60  
 
class Player:
    def __init__(self, image_path, start_x, start_y, controls, direction, boundary):
        self.image_path = image_path
        self.image = pygame.image.load(image_path).convert_alpha()  
        self.rect = self.image.get_rect(center=(start_x, start_y))
        self.speed = PLAYER_SPEED
        self.bullets = []
        self.health = PLAYER_HP
        self.controls = controls
        self.direction = direction  
        self.boundary = boundary
        self.heart_image = pygame.image.load("Sprites/Heart.png").convert_alpha()
        self.heart_image = pygame.transform.scale(self.heart_image, (50, 50))
        self.hitbox_radius = max(self.rect.width, self.rect.height) // 3
        self.hitbox_center = self.rect.center
        self.bullet_image = "Sprites/BulletLeft.png" if "PlayerRed" in image_path else "Sprites/BulletRight.png"
 
    def get_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == self.controls["shoot"]:
            bullet_start = self.rect.midright if self.direction == 1 else self.rect.midleft
            self.bullets.append(Bullet(bullet_start, self.direction, self.bullet_image))
 
    def update(self, keys, dt, opponent, boxes):
        """Updates player movement, bullets, and handles collisions."""
        if keys[self.controls["up"]]:
            self.rect.y -= self.speed * dt
        if keys[self.controls["down"]]:
            self.rect.y += self.speed * dt
        if keys[self.controls["left"]]:
            self.rect.x -= self.speed * dt
        if keys[self.controls["right"]]:
            self.rect.x += self.speed * dt
        self.boundary.enforce(self)
        self.hitbox_center = self.rect.center
        new_bullets = []
        for bullet in self.bullets:
            bullet.update(dt)
            if bullet.is_off_screen(1920):  
                continue  
            if bullet.check_collision(opponent):  
                opponent.take_damage()  
                continue  
            if bullet.check_collision_with_boxes(boxes):
                continue  
            new_bullets.append(bullet)
        self.bullets = new_bullets  
 
    def take_damage(self):
        self.health -= 1
       
    def draw(self, surf):
        for bullet in self.bullets:
            bullet.render(surf)
        surf.blit(self.image, self.rect)
        for i in range(self.health):
            heart_x = self.rect.x + 30 + (i * HEART_SPACING)
            heart_y = self.rect.y - 40  
            surf.blit(self.heart_image, (heart_x, heart_y))
 
    def check_collision(self, bullet):
        return self.rect.colliderect(bullet.rect)