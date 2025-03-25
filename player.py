import pygame as pg

pg.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PLAYER_SPEED = 300
LASER_SPEED = 5
PLAYER_HP = 3

# Colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# Initialize screen
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_rect = screen.get_rect()


class Laser:
    def __init__(self, loc, direction, color):
        self.image = pg.Surface((5, 40)).convert()
        self.image.fill(color)
        self.rect = self.image.get_rect(center=loc)
        self.speed = LASER_SPEED * direction  # Direction: -1 (up), 1 (down)

    def update(self):
        self.rect.y += self.speed

    def render(self, surf):
        surf.blit(self.image, self.rect)

    def is_off_screen(self):
        return self.rect.top > SCREEN_HEIGHT or self.rect.bottom < 0


class Player:
    def __init__(self, screen_rect, color, start_x, start_y, controls, direction):
        self.screen_rect = screen_rect
        self.color = color
        self.image = pg.Surface((50, 50)).convert()
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(start_x, start_y))
        self.dx = PLAYER_SPEED
        self.lasers = []
        self.health = PLAYER_HP
        self.controls = controls
        self.direction = direction  # -1 for Player 1 (shooting up), 1 for Player 2 (shooting down)

    def get_event(self, event):
        if event.type == pg.KEYDOWN and event.key == self.controls["shoot"]:
            self.lasers.append(Laser(self.rect.center, self.direction, YELLOW))

    def update(self, keys, dt):
        if keys[self.controls["left"]]:
            self.rect.x -= self.dx * dt
        if keys[self.controls["right"]]:
            self.rect.x += self.dx * dt

        self.rect.clamp_ip(self.screen_rect)

        # Update lasers and remove off-screen ones
        self.lasers = [laser for laser in self.lasers if not laser.is_off_screen()]
        for laser in self.lasers:
            laser.update()

    def draw(self, surf):
        for laser in self.lasers:
            laser.render(surf)
        surf.blit(self.image, self.rect)

    def check_collision(self, opponent):
        for laser in self.lasers:
            if laser.rect.colliderect(opponent.rect):
                opponent.health -= 1
                self.lasers.remove(laser)


# Controls for each player
p1_controls = {"left": pg.K_a, "right": pg.K_d, "shoot": pg.K_w}
p2_controls = {"left": pg.K_LEFT, "right": pg.K_RIGHT, "shoot": pg.K_UP}

# Create players
player1 = Player(screen_rect, BLUE, SCREEN_WIDTH // 4, SCREEN_HEIGHT - 100, p1_controls, -1)
player2 = Player(screen_rect, RED, 3 * SCREEN_WIDTH // 4, 100, p2_controls, 1)

clock = pg.time.Clock()
done = False

# Game loop
while not done:
    keys = pg.key.get_pressed()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        player1.get_event(event)
        player2.get_event(event)

    # Update game state
    delta_time = clock.tick(60) / 1000.0
    player1.update(keys, delta_time)
    player2.update(keys, delta_time)

    # Check for collisions
    player1.check_collision(player2)
    player2.check_collision(player1)

    # Draw everything
    screen.fill(BLACK)
    player1.draw(screen)
    player2.draw(screen)

    # Display Health
    font = pg.font.Font(None, 36)
    hp_text = font.render(f"P1 HP: {player1.health}   P2 HP: {player2.health}", True, (255, 255, 255))
    screen.blit(hp_text, (SCREEN_WIDTH // 2 - 100, 10))

    # Check if a player lost
    if player1.health <= 0:
        print("Player 2 Wins!")
        done = True
    elif player2.health <= 0:
        print("Player 1 Wins!")
        done = True

    pg.display.update()

pg.quit()
