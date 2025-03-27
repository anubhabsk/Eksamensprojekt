import pygame
from bullet import Bullet
from boundary import Boundary


PLAYER_SPEED = 300
PLAYER_HP = 3
HEART_SPACING = 60  # Space between hearts

class Player:
    def __init__(self, image_path, start_x, start_y, controls, direction, boundary):
        self.image = pygame.image.load(image_path).convert_alpha()  
        self.rect = self.image.get_rect(center=(start_x, start_y))
        
        self.image_path = image_path  # Store image path for boundary checks
        self.speed = PLAYER_SPEED
        self.bullets = []
        self.health = PLAYER_HP # Players start with 3 HP
        self.controls = controls
        self.direction = direction  
        self.boundary = boundary  # Assign boundary instance
        
        # Load and resize heart image for HP display
        self.heart_image = pygame.image.load("Sprites/Heart.png").convert_alpha()
        self.heart_image = pygame.transform.scale(self.heart_image, (50, 50))  # Justér størrelsen her


        # Determine bullet image based on player image
        if "PlayerRed" in image_path:
            self.bullet_image = "Sprites/BulletLeft.png"
        else:
            self.bullet_image = "Sprites/BulletRight.png"

    def get_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == self.controls["shoot"]:
            bullet_start = self.rect.midright if self.direction == 1 else self.rect.midleft
            self.bullets.append(Bullet(bullet_start, self.direction, self.bullet_image))

    def update(self, keys, dt, opponent):
        if keys[self.controls["up"]]:
            self.rect.y -= self.speed * dt
        if keys[self.controls["down"]]:
            self.rect.y += self.speed * dt
        if keys[self.controls["left"]]:
            self.rect.x -= self.speed * dt
        if keys[self.controls["right"]]:
            self.rect.x += self.speed * dt
            
        # Apply boundary restrictions
        self.boundary.enforce(self)
        
        # Remove bullets that hit opponent or go off-screen
        new_bullets = []
        for bullet in self.bullets:
            bullet.update(dt)
            if bullet.is_off_screen(1920):
                continue  # Remove bullet if it goes off screen
            if bullet.check_collision(opponent):  
                opponent.health -= 1  # Reduce opponent's health
                if opponent.health <= 0:
                    pygame.quit()  # End game if HP reaches 0
                    quit()
                continue  # Remove bullet upon collision
            new_bullets.append(bullet)

        # Update bullets
        self.bullets = new_bullets # Update bullets list

    def draw(self, surf):
        for bullet in self.bullets:
            bullet.render(surf)
        # Draw player sprite
        surf.blit(self.image, self.rect)
        
        # Draw hearts
        for i in range(self.health):
            heart_x = self.rect.x + (i * HEART_SPACING)
            heart_y = self.rect.y - 40  # Position above player
            surf.blit(self.heart_image, (heart_x, heart_y))
