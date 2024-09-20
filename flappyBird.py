import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Bird
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 4, HEIGHT // 2)
        self.velocity = 0
        self.gravity = 0.5

    def update(self):
        self.velocity += self.gravity
        self.rect.y += self.velocity
        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity = 0

    def jump(self):
        self.velocity = -10

# Pipe
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, is_top):
        super().__init__()
        self.image = pygame.Surface((60, y))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        if is_top:
            self.rect.bottomleft = (x, y)
        else:
            self.rect.topleft = (x, y)
        self.speed = -4

    def update(self):
        self.rect.x += self.speed
        if self.rect.right < 0:
            self.kill()

# Game class
class Game:
    def __init__(self):
        self.bird = Bird()
        self.all_sprites = pygame.sprite.Group(self.bird)
        self.pipes = pygame.sprite.Group()
        self.score = 0
        self.font = pygame.font.Font(None, 36)

    def create_pipes(self):
        height = random.randint(150, 400)
        gap = 200
        top_pipe = Pipe(WIDTH, height, True)
        bottom_pipe = Pipe(WIDTH, height + gap, False)
        self.pipes.add(top_pipe, bottom_pipe)
        self.all_sprites.add(top_pipe, bottom_pipe)

    def run(self):
        clock = pygame.time.Clock()
        pipe_timer = 0
        running = True

        while running:
            dt = clock.tick(60) / 1000  # Delta time in seconds

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.bird.jump()

            # Create new pipes
            pipe_timer += dt
            if pipe_timer > 1.5:  # Create new pipes every 1.5 seconds
                self.create_pipes()
                pipe_timer = 0

            self.all_sprites.update()

            # Check for collisions
            if pygame.sprite.spritecollide(self.bird, self.pipes, False) or self.bird.rect.bottom > HEIGHT:
                running = False

            # Update score
            for pipe in self.pipes:
                if pipe.rect.right < self.bird.rect.left and not hasattr(pipe, 'scored'):
                    self.score += 0.5  # Increment by 0.5 for each pipe (top and bottom) to get 1 point per pair
                    pipe.scored = True

            # Draw everything
            screen.fill(WHITE)
            self.all_sprites.draw(screen)

            # Draw score
            score_text = self.font.render(f"Score: {int(self.score)}", True, BLACK)
            screen.blit(score_text, (10, 10))

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()