import pygame
import sys
import random  # Required for randomization 

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong - No Images")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Frame rate
FPS = 60
CLOCK = pygame.time.Clock()

# Paddle settings
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
PADDLE_SPEED = 7

# Ball settings
BALL_SIZE = 20
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# Font (use default system font to avoid errors)
FONT = pygame.font.Font(None, 30)  # Replaced "Arial" with default font [[8]]

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
    
    def draw(self):
        pygame.draw.rect(SCREEN, WHITE, self.rect)
    
    def move(self, direction):
        if direction == "UP" and self.rect.top > 0:
            self.rect.y -= PADDLE_SPEED
        elif direction == "DOWN" and self.rect.bottom < HEIGHT:
            self.rect.y += PADDLE_SPEED

class Ball:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.rect = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)
        # Use random.random() instead of random() to avoid TypeError [[9]]
        self.speed_x = BALL_SPEED_X * (-1 if random.random() < 0.5 else 1)
        self.speed_y = BALL_SPEED_Y * (-1 if random.random() < 0.5 else 1)
    
    def draw(self):
        pygame.draw.rect(SCREEN, WHITE, self.rect)
    
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        # Wall collisions
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1
        
        # Score check
        if self.rect.left <= 0:
            return "RIGHT"
        elif self.rect.right >= WIDTH:
            return "LEFT"
        return None

# Create paddles and ball
left_paddle = Paddle(20, HEIGHT//2 - PADDLE_HEIGHT//2)
right_paddle = Paddle(WIDTH - 30, HEIGHT//2 - PADDLE_HEIGHT//2)
ball = Ball()

# Scores
left_score = 0
right_score = 0

def reset_ball():
    ball.reset()

while True:
    SCREEN.fill(BLACK)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Key states
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        left_paddle.move("UP")
    if keys[pygame.K_s]:
        left_paddle.move("DOWN")
    if keys[pygame.K_UP]:
        right_paddle.move("UP")
    if keys[pygame.K_DOWN]:
        right_paddle.move("DOWN")
    
    # Ball logic
    winner = ball.update()
    if winner == "LEFT":
        left_score += 1
        reset_ball()
    elif winner == "RIGHT":
        right_score += 1
        reset_ball()
    
    # Paddle collision
    if ball.rect.colliderect(left_paddle.rect) or ball.rect.colliderect(right_paddle.rect):
        ball.speed_x *= -1
    
    # Draw everything
    left_paddle.draw()
    right_paddle.draw()
    ball.draw()
    
    # Display scores
    left_text = FONT.render(str(left_score), True, WHITE)
    right_text = FONT.render(str(right_score), True, WHITE)
    SCREEN.blit(left_text, (WIDTH//4, 20))
    SCREEN.blit(right_text, (WIDTH * 3//4, 20))
    
    # Update display
    pygame.display.flip()
    CLOCK.tick(FPS)  # Limit to 60 FPS
