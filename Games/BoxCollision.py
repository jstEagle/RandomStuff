import pygame
import random
from enum import Enum

pygame.init()

width = 1200
height = 800

window = pygame.display.set_mode((width, height))

# Colours
WHITE = (250, 250, 250)
BLACK = (0, 0, 0)
BLUE = (87, 180, 242)
GRAY = (100, 100, 100)

class Box:
    def __init__(self, x, y, x_vel, y_vel, colour, dimension):
        self.x = x
        self.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.colour = colour
        self.dimension = dimension
        
    def update(self):
        self.x += self.x_vel
        self.y += self.y_vel

        pygame.draw.rect(window, self.colour, (self.x, self.y, self.dimension, self.dimension))
        
    def check_collision(self):
        # Calculate the position of the player's box
        player_rect = pygame.Rect(self.x, self.y, self.dimension, self.dimension)
        
        # Flag to indicate whether collision resolution is in progress
        resolving_collision = False
        
        # Loop through each wall box
        for box in boxes:
            if box.colour == wall_color:
                # Create a rectangle for the current wall box
                wall_rect = pygame.Rect(box.x, box.y, box.dimension, box.dimension)
                
                # Check for collision between player's box and wall
                if player_rect.colliderect(wall_rect) and not resolving_collision:
                    # Determine the side of collision (left/right or top/bottom)
                    dx = self.x + self.dimension / 2 - box.x - box.dimension / 2
                    dy = self.y + self.dimension / 2 - box.y - box.dimension / 2
                    
                    # Adjust position to resolve collision
                    if abs(dx) > abs(dy):
                        # If collision is on the horizontal axis, adjust x position
                        if dx > 0: #Left
                            self.x = box.x + box.dimension
                            self.collision_effect(Direction.LEFT)
                        else: #Right
                            self.x = box.x - self.dimension
                            self.collision_effect(Direction.RIGHT)
                            
                        # Flip x velocity
                        self.x_vel *= -1
                    else:
                        # If collision is on the vertical axis, adjust y position
                        if dy > 0: #Above
                            self.y = box.y + box.dimension
                            self.collision_effect(Direction.UP)
                        else: #Below
                            self.y = box.y - self.dimension
                            self.collision_effect(Direction.DOWN)
                            
                        # Flip y velocity
                        self.y_vel *= -1
                    
                    # Set flag to indicate collision resolution is in progress
                    resolving_collision = True
                    
                    self.colour = (random.randint(0, 250), random.randint(0, 250), random.randint(0, 250))
        
        # Reset flag after checking all collisions
        resolving_collision = False
    
    def collision_effect(self, direction):
        for i in range(random.randint(5, 15)):
            effects.append(Effect(self.x, self.y, self.x_vel, self.y_vel, self.dimension - 5, direction))

class Direction(Enum):
        LEFT = 1
        RIGHT = 2
        UP = 3
        DOWN = 4
    
class Effect:
    def __init__(self, x, y, x_vel, y_vel, size, direction):
        self.x = x
        self.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.size = random.randint(2, size)
        self.colour = (250, 250, 250)
        self.count = 0;
    
        self.direction = direction

        if direction == Direction.UP:
            self.x += random.randint(-10, 10)
            self.y += random.randint(-10, 0)
            self.x_vel = random.randint(-3, 3)
            self.y_vel = random.randint(-3, -1)
        elif direction == Direction.DOWN:
            self.x += random.randint(-10, 10)
            self.y += random.randint(0, 10)
            self.x_vel = random.randint(-3, 3)
            self.y_vel = random.randint(1, 3)
        elif direction == Direction.LEFT:
            self.x += random.randint(-10, 0)
            self.y += random.randint(-10, 10)
            self.x_vel = random.randint(-3, -1)
            self.y_vel = random.randint(-3, 3)
        else:
            self.x += random.randint(0, 10)
            self.y += random.randint(-10, 10)
            self.x_vel = random.randint(1, 3)
            self.y_vel = random.randint(-3, 3)
        
    def update(self):
        pygame.draw.rect(window, self.colour, (self.x, self.y, self.size, self.size))
        
        self.x += self.x_vel
        self.y += self.y_vel
        
        self.count += 1;
        
        if random.randint(0, 20) == 1:
            self.colour = (random.randint(50, 220), random.randint(50, 220), random.randint(50, 220))
        
        if self.count / 10 > 1:
            self.size -= 2
            
        if self.size <= 0:
            del self
            
# Making the Map
rows = 8
cols = 12

wall_height = 100
wall_len = 100
wall_color = (127, 127, 127)

map_array = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
             [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
             [1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1],
             [1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],]

boxes = []

for i in range(rows):
    for j in range(cols):
        if map_array[i][j] == 1:
            boxes.append(Box(j * 100, i * 100, 0, 0, wall_color, 100))
            
player_boxes = []
effects = []

# Setup
running = True
clock = pygame.time.Clock()
FPS = 60

while running:
    deltaTime = clock.tick(FPS) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                random_vel_x = random.randint(-5, 5)
                random_vel_y = random.randint(-5, 5)
                
                while random_vel_x == 0 or random_vel_y == 0 or random_vel_x == 1 or random_vel_y == 1:
                    random_vel_x = random.randint(-5, 5)
                    random_vel_y = random.randint(-5, 5)
                    
                random_colour = (random.randint(0, 250), random.randint(0, 250), random.randint(0, 250))
                random_dimension = random.randint(10, 30)
                player_boxes.append(Box(mouse_x, mouse_y, random_vel_x, random_vel_y, random_colour, random_dimension))
            
            if event.button == 3:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                row = int(mouse_y / 100)
                col = int(mouse_x / 100)
                
                if map_array[row][col] == 0:
                    map_array[row][col] = 1
                else:
                    map_array[row][col] = 0
                    
                boxes = []
                
                for i in range(rows):
                    for j in range(cols):
                        if map_array[i][j] == 1:
                            boxes.append(Box(j * 100, i * 100, 0, 0, wall_color, 100))
    
    buttons = pygame.key.get_pressed()
    
    if buttons[pygame.K_SPACE]:
        player_boxes = []
    
    window.fill(WHITE)
    
    for box in boxes:
        box.update()
    
    for player in player_boxes:
        player.update()
        player.check_collision()

    for effect in effects:
        effect.update()
        
    pygame.display.flip()
    
pygame.quit()