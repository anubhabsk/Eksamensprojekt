import pygame
import random
 
BOX_WIDTH, BOX_HEIGHT = 159.589041, 150  # Box size
RESPAWN_TIME = 3000  
 
class Box:
    def __init__(self, x, y):
        self.image = pygame.image.load("Sprites/Box.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (BOX_WIDTH, BOX_HEIGHT))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = 3
        self.active = True
        self.respawn_time = 0  
 
    def take_damage(self):
        """ Reduce HP and despawn if necessary. """
        if self.active:
            self.health -= 1
            if self.health <= 0:
                self.active = False
                self.respawn_time = pygame.time.get_ticks()  
 
    def update(self):
        """ Respawn after a set time if inactive. """
        if not self.active:
            current_time = pygame.time.get_ticks()
            if current_time - self.respawn_time >= RESPAWN_TIME:
                self.respawn()
 
    def respawn(self):
        """ Reset health and make the box visible again. """
        self.health = 3
        self.active = True
 
    def draw(self, surf):
        """ Draw the box if it's active. """
        if self.active:
            surf.blit(self.image, self.rect)
 
 
def generate_boxes(screen_width, screen_height, num_per_side):
    """ Generate boxes in random positions on each side. """
    boxes = []
    middle_x = screen_width // 2
    margin = 100  
 
    for _ in range(num_per_side):
        x = random.randint(margin, middle_x - BOX_WIDTH - margin)
        y = random.randint(margin, screen_height - BOX_HEIGHT - margin)
        boxes.append(Box(x, y))
 
    for _ in range(num_per_side):
        x = random.randint(middle_x + margin, screen_width - BOX_WIDTH - margin)
        y = random.randint(margin, screen_height - BOX_HEIGHT - margin)
        boxes.append(Box(x, y))
 
    return boxes