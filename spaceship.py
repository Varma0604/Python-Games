import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        return Bullet(self.rect.centerx, self.rect.top)

# Alien
class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 1

    def update(self):
        self.rect.y += self.speed

# Bullet
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# Power-up
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.type = random.choice(['speed', 'multishot'])

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

# Game class
class Game:
    def __init__(self):
        self.player = Player()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.aliens = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.score = 0
        self.level = 1
        self.create_aliens()

    def create_aliens(self):
        for row in range(5):
            for column in range(10):
                alien = Alien(column * 60 + 50, row * 50 + 30)
                self.aliens.add(alien)
                self.all_sprites.add(alien)

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bullet = self.player.shoot()
                        self.bullets.add(bullet)
                        self.all_sprites.add(bullet)

            self.all_sprites.update()

            # Check for collisions
            hits = pygame.sprite.groupcollide(self.aliens, self.bullets, True, True)
            for hit in hits:
                self.score += 10
                if random.random() < 0.1:  # 10% chance to spawn a power-up
                    powerup = PowerUp(hit.rect.x, hit.rect.y)
                    self.powerups.add(powerup)
                    self.all_sprites.add(powerup)

            # Check for power-up collection
            powerup_hits = pygame.sprite.spritecollide(self.player, self.powerups, True)
            for powerup in powerup_hits:
                if powerup.type == 'speed':
                    self.player.speed += 1
                elif powerup.type == 'multishot':
                    for i in range(-1, 2):
                        bullet = Bullet(self.player.rect.centerx + i * 10, self.player.rect.top)
                        self.bullets.add(bullet)
                        self.all_sprites.add(bullet)

            # Check if aliens reached the bottom
            if any(alien.rect.bottom >= HEIGHT for alien in self.aliens):
                running = False

            # Next level
            if not self.aliens:
                self.level += 1
                self.create_aliens()
                for alien in self.aliens:
                    alien.speed = 1 + self.level * 0.5

            # Draw everything
            screen.fill(BLACK)
            self.all_sprites.draw(screen)

            # Draw score and level
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {self.score}", True, WHITE)
            level_text = font.render(f"Level: {self.level}", True, WHITE)
            screen.blit(score_text, (10, 10))
            screen.blit(level_text, (WIDTH - 100, 10))

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()