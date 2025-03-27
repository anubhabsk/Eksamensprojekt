import pygame
from pygame.locals import *

pygame.init()
#screen = pygame.display.set_mode((1920, 1080))
screen = pygame.display.set_mode((200, 100), SCALED | FULLSCREEN)
pygame.display.set_caption("Shooting Sim 2D")

FPS = 30
clock = pygame.time.Clock()

BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 251, 0)

lazerGroup = pygame.sprite.Group()
players = pygame.sprite.Group()


class Lazer(pygame.sprite.Sprite):
    def __init__(self, dir, window, speed=10, sender=None):
        super().__init__()
        self.image = pygame.Surface((10, 2))
        self.image.fill(YELLOW)

        self.rect = self.image.get_rect()
        self.vel = pygame.math.Vector2(speed, 0) * dir
        self.window = window
        self.sender = sender

    def update(self):
        self.rect.center += self.vel
        if self.rect.x < 0 or self.rect.midright[0] > self.window.get_width():
            self.kill()
        if p := pygame.sprite.spritecollide(self, players, False):
            for sprite in p:
                if sprite != self.sender:
                    self.kill()
        """
        if not (0 > self.rect.centerx + self.rect.width//2 > self.window.get_width()):
            self.kill()
        if not (0 > self.rect.centery + self.rect.height//2 > self.window.get_height()):
            self.kill()
        """

class Player(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface, color, size, keys, initPos=(0, 0)):
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.center = initPos
        self.window = screen
        self.keys = keys
        self.min = 0
        self.max = self.window.get_width()

    def update(self, fireGroup, dt=1):
        k = pygame.key.get_pressed()
        if k[self.keys["down"]]:
            if self.rect.midbottom[1] < self.window.get_height():
                self.rect.y += dt
        if k[self.keys["up"]]:
            if self.rect.midtop[1] > 0:
                self.rect.y -= dt

        if k[self.keys["left"]]:
            if self.rect.x > self.min:
                self.rect.x -= dt
        if k[self.keys["right"]]:
            if self.rect.midright[0] < self.max:
                self.rect.x += dt
        if k[self.keys["fire"]]:
            if self.rect.centerx > self.window.get_rect().centerx:
                dir = -1

            else:
                dir = 1

            tmp = Lazer(dir, self.window, sender=self)
            tmp.rect.center = self.rect.center

            lazerGroup.add(tmp)



def main():
    p1 = Player(screen, BLUE, (20, 20), dict(up=pygame.K_w, down=pygame.K_s, left=pygame.K_a, right=pygame.K_d, fire=pygame.K_q))
    p2 = Player(screen, RED, (20, 20), dict(up=pygame.K_UP, down=pygame.K_DOWN, left=pygame.K_LEFT, right=pygame.K_RIGHT, fire=pygame.K_p))

    p1.min = 0
    p1.max = screen.get_width()//2

    p2.min = p1.max
    p2.max = screen.get_width()

    p1.rect.center = (screen.get_width()//4, screen.get_height()//2)
    p2.rect.center = (screen.get_width() * 3//4, screen.get_height()//2)

    players.add(p1, p2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()


        players.update(lazerGroup, 3)
        lazerGroup.update()
        print(len(lazerGroup.sprites()))

        screen.fill(GREEN)
        players.draw(screen)
        lazerGroup.draw(screen)

        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    main()