import pygame

pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
BALL_RADIUS = 25
BALL_COLOR = (255, 0, 0)
BG_COLOR = (255, 255, 255)
STEP = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("moving ball")


ball_x = WIDTH // 2
ball_y = HEIGHT // 2

run = True
while run:
    screen.fill(BG_COLOR)
    pygame.draw.circle(screen, BALL_COLOR, (ball_x, ball_y), BALL_RADIUS)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and ball_y - BALL_RADIUS - STEP >= 0:
                ball_y -= STEP
            elif event.key == pygame.K_DOWN and ball_y + BALL_RADIUS + STEP <= HEIGHT:
                ball_y += STEP
            elif event.key == pygame.K_LEFT and ball_x - BALL_RADIUS - STEP >= 0:
                ball_x -= STEP
            elif event.key == pygame.K_RIGHT and ball_x + BALL_RADIUS + STEP <= WIDTH:
                ball_x += STEP

pygame.quit()
