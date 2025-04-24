import pygame

BULLET_SPEED = 1100

class Bullet:
    def __init__(self, loc, direction, image_path):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=loc)
        self.speed = BULLET_SPEED * direction  

    def update(self, dt):
        self.rect.x += self.speed * dt  

    def render(self, surf):
        surf.blit(self.image, self.rect)

    def is_off_screen(self, screen_width):
        return self.rect.right < 0 or self.rect.left > screen_width  
    
    def check_collision(self, player):
        return player.check_collision(self)
    
    def check_collision_with_boxes(self, boxes):
        """ Check if bullet collides with any active box """
        for box in boxes:
            if box.active and self.rect.colliderect(box.rect):
                box.take_damage()
                return True
        return False
    
