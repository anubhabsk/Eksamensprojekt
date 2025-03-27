import pygame
from bullet import Bullet
from boundary import Boundary
import math


PLAYER_SPEED = 300
PLAYER_HP = 3
HEART_SPACING = 60  #Mellemrum mellem hjerter .png

class Player:
    def __init__(self, image_path, start_x, start_y, controls, direction, boundary):
        self.image = pygame.image.load(image_path).convert_alpha()  
        self.rect = self.image.get_rect(center=(start_x, start_y))
        
        self.image_path = image_path  #Gem billedsti til grænsekontrol
        self.speed = PLAYER_SPEED
        self.bullets = []
        self.health = PLAYER_HP
        self.controls = controls
        self.direction = direction  
        self.boundary = boundary
        
        #Indlæs og tilpas hjertebillede til HP skærm
        self.heart_image = pygame.image.load("Sprites/Heart.png").convert_alpha()
        self.heart_image = pygame.transform.scale(self.heart_image, (50, 50))
        
        #Definer Circular Hitbox
        self.hitbox_radius = max(self.rect.width, self.rect.height) // 3
        self.hitbox_center = self.rect.center

        #Bestem bullet billede baseret på spillerbillede
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
        
        #Anvend grænsebegrænsninger
        self.boundary.enforce(self)

        #Opdater hitbox position
        self.hitbox_center = self.rect.center
        
        #Fjern kugler, der rammer modstanderen, eller går væk fra skærmen
        new_bullets = []
        for bullet in self.bullets:
            bullet.update(dt)
            if bullet.is_off_screen(1920):
                continue  #Fjern kuglen, hvis den er væk fra skærmen
            if bullet.check_collision(opponent):  
                opponent.take_damage()  #Brug den nye funktion til at reducere HP
                continue  #Fjern kuglen ved kollision
            new_bullets.append(bullet)

        
        self.bullets = new_bullets #Opdater bullets list

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            pygame.quit()  #Afslut spillet, hvis HP når 0
            quit()
        
    def check_collision(self, bullet):
        #Tjek om kuglen er inde i den cirkulære hitbox
        bullet_x, bullet_y = bullet.rect.center
        dist_x = bullet_x - self.hitbox_center[0]
        dist_y = bullet_y - self.hitbox_center[1]
        distance = math.sqrt(dist_x**2 + dist_y**2)
        return distance <= self.hitbox_radius

    def draw(self, surf):
        for bullet in self.bullets:
            bullet.render(surf)
        surf.blit(self.image, self.rect)

        # Draw circular hitbox for debugging (remove this in final version)
        # pygame.draw.circle(surf, (255, 0, 0), self.hitbox_center, self.hitbox_radius, 2)  

        for i in range(self.health):
            heart_x = self.rect.x + 30 + (i * HEART_SPACING)
            heart_y = self.rect.y - 40  
            surf.blit(self.heart_image, (heart_x, heart_y))