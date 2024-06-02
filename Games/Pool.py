import pygame
import math
import random

pygame.init()
pygame.mixer.init()

screen_width = 1200
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))

friction = 0.1
border_width = 60

# Making border
class Border:
    def __init__(self, width, num_holes):
        self.width = width
        self.num_holes = num_holes
        self.holes = []
        
    def drawBorder(self):
        border_green = (28, 153, 62)
        border_wood = (110, 84, 44)
        
        
        #top
        pygame.draw.rect(screen, border_green, (0, self.width * 0.3, screen_width, self.width * 0.7))
        pygame.draw.rect(screen, border_green, (self.width * 0.3, self.width, self.width * 0.7, screen_height))
        pygame.draw.rect(screen, border_green, (screen_width - self.width, self.width, screen_width, screen_height))
        pygame.draw.rect(screen, border_green, (self.width * 0.3, screen_height - self.width, screen_width, screen_height))
        
        #wood
        pygame.draw.rect(screen, border_wood, (0, 0, screen_width, self.width * 0.3))
        pygame.draw.rect(screen, border_wood, (0, 0, self.width * 0.3, screen_height))
        pygame.draw.rect(screen, border_wood, (0, screen_height - self.width * 0.3, screen_width, screen_height))
        pygame.draw.rect(screen, border_wood, (screen_width - self.width * 0.3, 0, screen_width, screen_height))

        #Holes
        hole_colour = (48, 48, 48)

        for hole in self.holes:
            pygame.draw.circle(screen, hole_colour, hole, 20)
        
    
    def add_holes(self):
        if self.num_holes == 0:
            return
        elif self.num_holes == 1:
            self.holes.append((screen_width - self.width * 0.8, screen_height / 2))
        elif self.num_holes == 2:
            self.holes.append((self.width * 0.8, screen_height / 2))
            self.holes.append((screen_width - self.width * 0.8, screen_height / 2))
        elif self.num_holes == 3:
            self.holes.append((self.width * 0.8, screen_height / 2))
            self.holes.append((screen_width - self.width * 0.8, screen_height / 2))
            self.holes.append((screen_width / 2, self.width * 0.8))
        elif self.num_holes == 4:
            self.holes.append((self.width, self.width))
            self.holes.append((self.width, screen_height - self.width))
            self.holes.append((screen_width - self.width, screen_height - self.width))
            self.holes.append((screen_width - self.width, self.width))
        elif self.num_holes == 5:
            self.holes.append((self.width, self.width))
            self.holes.append((self.width, screen_height - self.width))
            self.holes.append((screen_width - self.width, screen_height - self.width))
            self.holes.append((screen_width - self.width, self.width))
            self.holes.append((screen_width / 2, self.width * 0.8))
        elif self.num_holes == 6:
            self.holes.append((self.width, self.width))
            self.holes.append((self.width, screen_height - self.width))
            self.holes.append((screen_width - self.width, screen_height - self.width))
            self.holes.append((screen_width - self.width, self.width))
            self.holes.append((screen_width / 2, self.width * 0.8))
            self.holes.append((screen_width / 2, screen_height - self.width * 0.8))
            
class Ball:
    def __init__(self, x, y, r, x_vel, y_vel, colour, main_ball):
        self.x = x
        self.y = y
        self.r = r
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.hole = False
        self.colour = colour
        self.main = main_ball
        
    def drawBall(self):
        if not self.main:
            pygame.draw.circle(screen, self.colour, (self.x, self.y), self.r)
        else:
            pygame.draw.circle(screen, (10, 10, 10), (self.x, self.y), self.r + 1)
            pygame.draw.circle(screen, (230, 230, 230), (self.x, self.y), self.r)
            
        if not self.hole:
            self.updateBall()
        else:
            self.holeCollision()
    
    def updateBall(self):
        # Update ball position
        self.x += self.x_vel
        self.y += self.y_vel

        # Apply friction
        if self.x_vel != 0:
            friction_x = friction * abs(self.x_vel) / (abs(self.x_vel) + abs(self.y_vel))
            self.x_vel -= friction_x * (self.x_vel / abs(self.x_vel))
        
        if self.y_vel != 0:
            friction_y = friction * abs(self.y_vel) / (abs(self.x_vel) + abs(self.y_vel))
            self.y_vel -= friction_y * (self.y_vel / abs(self.y_vel))
            
            self.ballCollision()

    
    def ballCollision(self):
        collide = False
        # Check if the ball collides with the border
        if (self.x - self.r <= border_width): 
            self.x = border_width + self.r
            self.x_vel *= -1
            collide = True
        elif (self.x + self.r >= screen_width - border_width):
            self.x = screen_width - border_width - self.r
            self.x_vel *= -1
            collide = True
            
        if (self.y - self.r <= border_width):
            self.y = border_width + self.r
            self.y_vel *= -1
            collide = True
        elif (self.y + self.r >= screen_height - border_width):
            self.y = screen_height - border_width - self.r
            self.y_vel *= -1
            collide = True
            
        if collide:
            sound = pygame.mixer.Sound("../edge_hit.wav")
            sound.set_volume(0.3)
            sound.play()
        
        self.holeCollision()

    def holeCollision(self):
        # Check if the ball collides with a hole
        global border
        for hole in border.holes:
            distance = math.sqrt((hole[0] - self.x)**2 + (hole[1] - self.y)**2)
            
            if distance <= 20 + self.r:
                self.x = hole[0]
                self.y = hole[1]
                
                if not self.hole:
                    sound = pygame.mixer.Sound("../ball_hole.wav")
                    sound.play()
                
                # Reduce ball's radius if greater than 0, else remove the ball
                if self.r > 0:
                    self.hole = True
                    self.r -= 1
                else:
                    # Remove the ball from the list of balls
                    if not self.main:
                        balls.remove(self)
                    else:
                        self.r = 15
                        self.x = screen_width / 3
                        self.y = screen_height / 2
                        self.hole = False
                        self.x_vel = 0
                        self.y_vel = 0

    def check_collision(self, balls):
        for ball in balls:
            if ball is not self:
                # Calculate the distance between the balls
                distance = math.sqrt((ball.x - self.x)**2 + (ball.y - self.y)**2)
                
                # Check if there is a collision
                if distance <= self.r + ball.r:
                    # Calculate the normal vector
                    nx = (ball.x - self.x) / distance
                    ny = (ball.y - self.y) / distance
                    
                    # Calculate the tangent vector
                    tx = -ny
                    ty = nx
                    
                    # Calculate the dot product of the velocity vectors with the normal and tangent vectors
                    dpTan1 = self.x_vel * tx + self.y_vel * ty
                    dpTan2 = ball.x_vel * tx + ball.y_vel * ty
                    
                    dpNorm1 = self.x_vel * nx + self.y_vel * ny
                    dpNorm2 = ball.x_vel * nx + ball.y_vel * ny
                    
                    # Conservation of momentum in 1D
                    m1 = (dpNorm1 * (self.r - ball.r) + 2 * ball.r * dpNorm2) / (self.r + ball.r)
                    m2 = (dpNorm2 * (ball.r - self.r) + 2 * self.r * dpNorm1) / (self.r + ball.r)
                    
                    # Update velocities
                    self.x_vel = tx * dpTan1 + nx * m1
                    self.y_vel = ty * dpTan1 + ny * m1
                    ball.x_vel = tx * dpTan2 + nx * m2
                    ball.y_vel = ty * dpTan2 + ny * m2
                    
                    sound = pygame.mixer.Sound("../ball_hit.wav")
                    sound.play()
                    
                    # Move the balls apart to avoid overlap
                    overlap = 0.5 * (self.r + ball.r - distance + 1)
                    self.x -= overlap * nx
                    self.y -= overlap * ny
                    ball.x += overlap * nx
                    ball.y += overlap * ny

            
def calc_force(initial_x, initial_y, end_x, end_y, ball):
    # Calculate the change in position along x and y axes
    delta_x = end_x - initial_x
    delta_y = end_y - initial_y
    
    # Calculate the magnitude of the distance
    distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
    
    # Avoid division by zero
    if distance == 0:
        return
    
    # Calculate the unit vector components
    unit_x = delta_x / distance
    unit_y = delta_y / distance
    
    # Determine the maximum speed
    max_speed = 12
    
    # Calculate the velocity components based on the unit vector and speed factor
    ball.x_vel = -unit_x * min(max_speed, distance / 10)
    ball.y_vel = -unit_y * min(max_speed, distance / 10)

def draw_arrow(initial_x, initial_y, end_x, end_y):
    # Calculate the change in position along x and y axes
    delta_x = initial_x - end_x
    delta_y = initial_y - end_y
    
    # Calculate the magnitude of the distance
    distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
    
    # Determine the maximum length of the arrow corresponding to the max speed
    max_speed = 12
    max_distance = max_speed * 20  # Distance corresponding to maximum speed
    
    end_x = initial_x + delta_x
    end_y = initial_y + delta_y
    
    if distance > max_distance:
        # Scale the end coordinates to cap the arrow length
        scale = max_distance / distance
        end_x = initial_x + delta_x * scale
        end_y = initial_y + delta_y * scale
    
    pygame.draw.line(screen, (250, 250, 250), (initial_x, initial_y), (end_x, end_y), 5)

def start_position():
    balls = []
    positions = []
    
    for i in range(random.randint(3, 20)):
        x = random.randint(80, screen_width - 80)
        y = random.randint(80, screen_height - 80)
        
        while (x, y) in positions:
            x = random.randint(80, screen_width - 80)
            y = random.randint(80, screen_height - 80)
            
        positions.append((x, y))
        balls.append(Ball(x, y, 15, 0, 0, (random.randint(10, 240), random.randint(10, 240), random.randint(10, 240)), False))
        
    balls.append(Ball(screen_width / 3, screen_height / 2, 15, 0, 0, (250, 250, 250), True))

    for ball in balls:
        ball.check_collision(balls)
        
    return balls


border = Border(border_width, 6)
border.add_holes()

mouse_initial_x = 0
mouse_initial_y = 0

running = True
arrow = False
arrow_start_x  = -1
arrow_start_y = -1

clock = pygame.time.Clock()
fps = 60

balls = start_position()

while running:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_initial_x, mouse_initial_y = mouse_x, mouse_y 
            arrow = True

            for ball in balls:
                distance = math.sqrt((mouse_initial_x - ball.x) ** 2 + (mouse_initial_y - ball.y) ** 2)

                # Check if the mouse is within the radius
                if distance <= ball.r and ball.main:
                    arrow_start_x, arrow_start_y = ball.x, ball.y

        elif event.type == pygame.MOUSEBUTTONUP:
            arrow = False
            arrow_start_x  = -1
            arrow_start_y = -1
            for ball in balls:
                distance = math.sqrt((mouse_initial_x - ball.x) ** 2 + (mouse_initial_y - ball.y) ** 2)

                # Check if the mouse is within the radius
                if distance <= ball.r and ball.main:
                    calc_force(mouse_initial_x, mouse_initial_y, mouse_x, mouse_y, ball)
                
    for ball in balls:
        if ball.x_vel != 0 and ball.y_vel != 0:
            ball.check_collision(balls)

    screen.fill((40, 176, 77))
    
    border.drawBorder()
    for ball in balls:
        ball.drawBall()

    if arrow and arrow_start_x > -1 and arrow_start_y > -1:
        draw_arrow(arrow_start_x, arrow_start_y, mouse_x, mouse_y)
    
    pygame.display.flip()

    clock.tick(fps)
            
pygame.quit()