import pygame
import random

pygame.init()

width = 1200
height = 800

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong")

paddle_width = 30
paddle_height = 100
paddle_colour = (200, 200, 200)

ball_len = 20

screen_colour = (80, 80, 80)

font = pygame.font.Font(None, 62)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.score = 0
    
    def update(self):
        player_box = pygame.Rect(self.x, self.y, paddle_width, paddle_height)
        
        pygame.draw.rect(window, paddle_colour, (player_box))

class Ball:
    def __init__(self, x, y, x_vel, y_vel):
        self.x = x
        self.y = y
        self.original_x_vel = x_vel
        self.original_y_vel = y_vel
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.colour = (random.randint(80, 250), random.randint(80, 250), random.randint(80, 250))
        
    def update(self):
        self.x += self.x_vel
        self.y += self.y_vel
        
        pygame.draw.rect(window, self.colour, (self.x, self.y, ball_len, ball_len))

    def check_collision(self):
        ball_box = pygame.Rect(self.x, self.y, ball_len, ball_len)
        
        player1 = pygame.Rect(player_1.x, player_1.y, paddle_width, paddle_height)
        player2 = pygame.Rect(player_2.x, player_2.y, paddle_width, paddle_height)
        
        resolving_collision = False
        
        if (ball_box.colliderect(player1) or ball_box.colliderect(player2)) and not resolving_collision:
            self.x_vel *= -1.2
            self.colour = (random.randint(80, 250), random.randint(80, 250), random.randint(80, 250))
        
        # check with screen border
        if (self.y < 0) or (self.y + ball_len > height):
            self.y_vel *= -1.1
        if (self.x < 0) or (self.x + ball_len > width):
            if self.x < 0:
                player_2.score += 1
            else:
                player_1.score += 1
                
            self.x = 580
            self.y = 380
            self.x_vel = self.original_x_vel * -1
            self.y_vel = self.original_y_vel * -1
            
                

running = True
clock = pygame.time.Clock()
FPS = 60

player_1 = Player(80, 300)
player_2 = Player(1090, 300)
ball = Ball(580, 380, 2, 2)

while running:
    deltaTime = clock.tick(FPS) / 1000
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    window.fill(screen_colour)
    
    buttons = pygame.key.get_pressed()
    
    if buttons[pygame.K_w] and player_1.y > 0:
        player_1.y -= 5
    elif buttons[pygame.K_s] and player_1.y < 800 - paddle_height:
        player_1.y += 5
        
    if buttons[pygame.K_UP] and player_2.y > 0:
        player_2.y -= 5
    elif buttons[pygame.K_DOWN] and player_2.y < 800 - paddle_height:
        player_2.y += 5
        
    # Score
    player_1_score_text = font.render(str(player_1.score), True, ball.colour)
    player_2_score_text = font.render(str(player_2.score), True, ball.colour)
    
    window.blit(player_1_score_text, (540, 30))
    window.blit(player_2_score_text, (640, 30))
    
    ball.update()
    ball.check_collision()
    
    player_1.update()
    player_2.update()
    
    pygame.display.flip()

            
pygame.quit()