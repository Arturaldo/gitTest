import pygame
import random

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60

BIRD_WIDTH = 34
BIRD_HEIGHT = 24
PIPE_WIDTH = 52
PIPE_GAP = 150

GRAVITY = 0.5
FLAP_STRENGTH = -10

# Initialize Pygame
pygame.init()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
CLOCK = pygame.time.Clock()
pygame.display.set_caption("Mini Flappy Bird")

# Bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(50, SCREEN_HEIGHT // 2))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += int(self.velocity)
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity = 0

    def flap(self):
        self.velocity = FLAP_STRENGTH

# Pipe class
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position='top'):
        super().__init__()
        self.image = pygame.Surface((PIPE_WIDTH, SCREEN_HEIGHT))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        if position == 'top':
            self.rect.bottomleft = (x, y - PIPE_GAP // 2)
        else:
            self.rect.topleft = (x, y + PIPE_GAP // 2)

    def update(self):
        self.rect.x -= 3
        if self.rect.right < 0:
            self.kill()

# Function to create pipe pairs

def create_pipe_pair(x):
    gap_y = random.randint(100, SCREEN_HEIGHT - 100)
    top_pipe = Pipe(x, gap_y, 'top')
    bottom_pipe = Pipe(x, gap_y, 'bottom')
    return top_pipe, bottom_pipe

# Main game loop

def main():
    running = True
    bird = Bird()
    pipes = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(bird)
    SPAWNPIPE = pygame.USEREVENT
    pygame.time.set_timer(SPAWNPIPE, 1500)

    score = 0
    font = pygame.font.SysFont(None, 36)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    bird.flap()
            if event.type == SPAWNPIPE:
                top_pipe, bottom_pipe = create_pipe_pair(SCREEN_WIDTH + PIPE_WIDTH)
                pipes.add(top_pipe, bottom_pipe)
                all_sprites.add(top_pipe, bottom_pipe)

        all_sprites.update()

        # Check collisions
        if pygame.sprite.spritecollideany(bird, pipes):
            running = False

        # Update score based on pipes passed
        for pipe in pipes:
            if pipe.rect.right < bird.rect.left and not hasattr(pipe, 'scored'):
                pipe.scored = True
                if pipe.rect.bottom < SCREEN_HEIGHT:  # count only one pipe of pair
                    score += 1

        SCREEN.fill((135, 206, 235))
        all_sprites.draw(SCREEN)

        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        SCREEN.blit(score_text, (10, 10))

        pygame.display.flip()
        CLOCK.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()
