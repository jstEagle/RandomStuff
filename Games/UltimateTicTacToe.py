import pygame
import sys

from enum import Enum

pygame.init()

DARK = (26, 26, 26)
LIGHT = (250, 244, 230)
SELECTED_LIGHT = (230, 223, 209)
RED = (235, 104, 87)
BLUE = (108, 173, 230)

# Gets screen size
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

# Set the dispaly size as a fraction of the screen
display_height = int(screen_height * 0.8)
display_width = display_height

last_move = -1
current_player = 1

# Create screen
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Ultimate Tic Tac Toe")

class Board:
    def __init__(self, x, y, number, width, height):
        self.x = x
        self.y = y
        self.winner = -1
        self.visible = True
        self.end = False
        self.counter = 0
        self.win_line = (-1, -1, -1)
        self.number = number
        self.width = width
        self.height = height
        self.spacing = int(width / 3)
        self.board = [(-1, x, y, 0), (-1, x + self.spacing, y, 1), (-1, x + self.spacing * 2, y, 2), 
                      (-1, x, y + self.spacing, 3), (-1, x + self.spacing, y + self.spacing, 4), (-1, x + self.spacing * 2, y + self.spacing, 5), 
                      (-1, x, y + self.spacing * 2, 6), (-1, x + self.spacing, y + self.spacing * 2, 7), (-1, x + self.spacing * 2, y + self.spacing * 2, 8)]
        
    def update_position(self, x, y, move):
        global last_move
        box_dim = self.spacing - 2
        for num in self.board:
            if(x < num[1] + box_dim and x > num[1] and y < num[2] + box_dim and y > num[2]) and num[0] == -1 and not self.end and (last_move == -1 or last_move == self.number):
                self.board[num[3]] = (move, num[1], num[2], num[3])
                last_move = num[3] + 1
                return True
        
        return False
        
    def drawBoard(self, selected):
        global last_move
        global current_player
        #draw lines of board
        for i in range(1, 3):
            vert_start_pos = (self.x + (self.spacing * i), self.y + 10)
            vert_end_pos = (self.x + (self.spacing * i), self.y + (self.spacing * 3) - 10)
            
            hor_start_pos = (self.x + 10, self.y + (self.spacing * i))
            hor_end_pos = (self.x + (self.spacing * 3) - 10, self.y + (self.spacing * i))
            
            chosen_colour = DARK
            line_thickness = 1
            
            if (last_move == self.number or last_move == -1):
                if current_player == 1:
                    chosen_colour = BLUE
                elif current_player == 0:
                    chosen_colour = RED
                line_thickness = 2
            
            pygame.draw.line(screen, chosen_colour, vert_start_pos, vert_end_pos, line_thickness)
            pygame.draw.line(screen, chosen_colour, hor_start_pos, hor_end_pos, line_thickness)
            
        #draw squares of board
        box_dim = self.spacing - 2
        for num in self.board:
            if num[0] == 1:
                line1_start = (num[1] + 20, num[2] + 20)
                line1_end = ((num[1] + box_dim) - 20, (num[2] + box_dim) - 20)
                
                line2_start= ((num[1] + box_dim) - 20, num[2] + 20)
                line2_end = (num[1] + 20, (num[2] + box_dim) - 20)
                
                pygame.draw.line(screen, BLUE, line1_start, line1_end, 5)
                pygame.draw.line(screen, BLUE, line2_start, line2_end, 5)
            elif num[0] == 0:
                circle_center = (int(num[1] + (self.spacing / 2)), int(num[2] + (self.spacing / 2)))
                circle_radius = int(self.spacing / 2) - 15
                pygame.draw.circle(screen, RED, circle_center, circle_radius, 4)
            elif(selected[0] < num[1] + box_dim and selected[0] > num[1] and selected[1] < num[2] + box_dim and selected[1] > num[2]) and not self.end:
                pygame.draw.rect(screen, SELECTED_LIGHT, (num[1] + 2, num[2] + 2, box_dim, box_dim))
        
        #Check to see if player has won
        if not self.end:
            #Check the rows
            for i in range(0, 7, 3):
                if(self.board[i][0] == 1 and self.board[i+1][0] == 1 and self.board[i + 2][0] == 1):
                    print(f"X won in {self.number}")
                    self.end = True
                    self.winner = 1
                    
                    line_start = (self.board[i][1] + 5, self.board[i][2] + (box_dim / 2))
                    line_end = (self.board[i + 2][1] + (box_dim - 10), self.board[i + 2][2] + (box_dim / 2))
                    
                    self.win_line = (BLUE, line_start, line_end)
                    
                elif(self.board[i][0] == 0 and self.board[i+1][0] == 0 and self.board[i + 2][0] == 0):
                    print(f"O won in {self.number}")
                    self.end = True
                    self.winner = 0
                    
                    line_start = (self.board[i][1] + 5, self.board[i][2] + (box_dim / 2))
                    line_end = (self.board[i + 2][1] + (box_dim - 10), self.board[i + 2][2] + (box_dim / 2))
                    
                    self.win_line = (RED, line_start, line_end)
            
            #Check columns
            for i in range(3):
                if(self.board[i][0] == 1 and self.board[i + 3][0] == 1 and self.board[i + 6][0] == 1):
                    print(f"X won {self.number}")
                    self.end = True
                    self.winner = 1
                    
                    line_start = (self.board[i][1] + (box_dim / 2), self.board[i][2] + 10)
                    line_end = (self.board[i + 6][1] + (box_dim / 2), self.board[i + 6][2] + (box_dim - 10))
                    
                    self.win_line = (BLUE, line_start, line_end)
                    
                if(self.board[i][0] == 0 and self.board[i + 3][0] == 0 and self.board[i + 6][0] == 0):
                    print(f"O won {self.number}")
                    self.end = True
                    self.winner = 0
                    
                    line_start = (self.board[i][1] + (box_dim / 2), self.board[i][2] + 10)
                    line_end = (self.board[i + 6][1] + (box_dim / 2), self.board[i + 6][2] + (box_dim - 10))
                    
                    self.win_line = (RED, line_start, line_end)
                    
            #Check diags
            if(self.board[0][0] == 1 and self.board[4][0] == 1 and self.board[8][0] == 1):
                print(f"X won {self.number}")
                self.end = True
                self.winner = 1
                
                line_start = (self.board[0][1] + 10, self.board[0][2] + 10)
                line_end = (self.board[8][1] + (box_dim - 10), self.board[8][2] + (box_dim - 10))
                
                self.win_line = (BLUE, line_start, line_end)
                
            elif(self.board[0][0] == 0 and self.board[4][0] == 0 and self.board[8][0] == 0):
                print(f"O won {self.number}")
                self.end = True
                self.winner = 0
                
                line_start = (self.board[0][1] + 10, self.board[0][2] + 10)
                line_end = (self.board[8][1] + (box_dim - 10), self.board[8][2] + (box_dim - 10))
                
                self.win_line = (RED, line_start, line_end)
                
            if(self.board[2][0] == 1 and self.board[4][0] == 1 and self.board[6][0] == 1):
                print(f"X won {self.number}")
                self.end = True
                self.winner = 1
                
                line_start = (self.board[2][1] + (box_dim - 10), self.board[2][2] + 10)
                line_end = (self.board[6][1] + 10, self.board[6][2] + (box_dim - 10))
                
                self.win_line = (BLUE, line_start, line_end)
                
            elif(self.board[2][0] == 0 and self.board[4][0] == 0 and self.board[6][0] == 0):
                print(f"O won {self.number}")
                self.end = True
                self.winner = 0
                
                line_start = (self.board[2][1] + (box_dim - 10), self.board[2][2] + 10)
                line_end = (self.board[6][1] + 10, self.board[6][2] + (box_dim - 10))
                
                self.win_line = (RED, line_start, line_end)
        else:
            if self.counter < 271:
                pygame.draw.line(screen, self.win_line[0],self.win_line[1], self.win_line[2], 8)
                self.counter += 1
            else:
                self.visible = False

def checkWin(big_board):
    winner = -1
    
    #Check the rows
    for i in range(0, 7, 3):
        if(big_board[i].winner == 1 and big_board[i+1].winner == 1 and big_board[i+2].winner == 1):
            print("X Wins overal")
            winner = 1
        elif(big_board[i].winner == 0 and big_board[i+1].winner == 0 and big_board[i+2].winner == 0):
            print("O Wins overal")
            winner = 0
    
    #Check columns
    for i in range(3):
        if(big_board[i].winner == 1 and big_board[i+3].winner == 1 and big_board[i + 6] == 1):
            print("X Wins overal")
            winner = 1
        if(big_board[i].winner == 0 and big_board[i + 3].winner == 0 and big_board[i+6] == 0):
            print("O Wins overal")
            winner = 0
    
    #Check Diags
    if(big_board[0].winner == 1 and big_board[4].winner == 1 and big_board[8].winner == 1):
        print("X Wins overal")
        winner = 1
    elif(big_board[0].winner == 0 and big_board[4].winner == 0 and big_board[8].winner == 0):
        print("O Wins overal")
        winner = 0
    if(big_board[2].winner == 1 and big_board[4].winner == 1 and big_board[6].winner == 1):
        print("X Wins overal")
        winner = 1
    elif(big_board[2].winner == 0 and big_board[4].winner == 0 and big_board[6].winner == 0):
        print("O Wins overal")
        winner = 0
        
    return winner

# Setup the Big board
big_board_width = int(display_width * 0.8)
big_board_height = int(display_height * 0.8)

big_board_position = (display_width / 2 - big_board_width / 2, display_height / 2 - big_board_height / 2) # (x, y)

board_width = int(big_board_width / 3) -1
board_height = int(big_board_height / 3) -1
board_spacing = board_height + 2

big_board = [Board(big_board_position[0], big_board_position[1], 1, board_width, board_height), Board(big_board_position[0] + board_spacing, big_board_position[1], 2, board_width, board_height), Board(big_board_position[0] + (board_spacing * 2), big_board_position[1], 3, board_width, board_height),
             Board(big_board_position[0], big_board_position[1] + board_spacing, 4, board_width, board_height), Board(big_board_position[0] + board_spacing, big_board_position[1] + board_spacing, 5, board_width, board_height), Board(big_board_position[0] + (board_spacing * 2), big_board_position[1] + board_spacing, 6, board_width, board_height),
             Board(big_board_position[0], big_board_position[1] + (board_spacing * 2), 7, board_width, board_height), Board(big_board_position[0] + board_spacing, big_board_position[1] + (board_spacing * 2), 8, board_width, board_height), Board(big_board_position[0] + (board_spacing * 2), big_board_position[1] + (board_spacing * 2), 9, board_width, board_height)]

# 1, 2, 3
# 4, 5, 6
# 7, 8, 9

max_fps = 90
clock = pygame.time.Clock()

running = True

clicked = False
winner = -1

font = pygame.font.Font(None, int(display_height * 0.2))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        
        # Check mouse button click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not clicked:
            clicked = True
            
            
    screen.fill(LIGHT)
    
    mouse_pos = pygame.mouse.get_pos()
    mouse_x = mouse_pos[0]
    mouse_y = mouse_pos[1]
    
    # Drawing the big board lines
    big_line_spacing = int(big_board_width / 3)
    
    if winner == -1:
        for board in big_board:
            if(mouse_x < board.x + board.width and mouse_x > board.x and mouse_y < board.y + board.height and mouse_y > board.y) and board.visible:
                board.drawBoard((mouse_x, mouse_y))
                if clicked and current_player == 1:
                    if board.update_position(mouse_x, mouse_y, current_player):
                        current_player = 0
                    clicked = False
                elif clicked and current_player == 0:
                    if board.update_position(mouse_x, mouse_y, current_player):
                        current_player = 1
                    clicked = False
            elif board.visible:
                board.drawBoard((-1, -1))
            elif not board.visible:
                if board.winner == 1:
                    first_line_start = (board.x + 10, board.y + 10)
                    first_line_end = (board.x + (board.width - 10), board.y + (board.width - 10))
                    
                    second_line_start = (board.x + (board.width - 10), board.y + 10)
                    second_line_end = (board.x + 10, board.y + (board.width - 10))
                    
                    pygame.draw.line(screen, BLUE, first_line_start, first_line_end, 10)
                    pygame.draw.line(screen, BLUE, second_line_start, second_line_end, 10)
                else:
                    circle_center = (board.x + int(board.width / 2), board.y + int(board.width / 2))
                    circle_radius = int(board.width / 2) - 10
                    pygame.draw.circle(screen, RED, circle_center, circle_radius, 8)
            if last_move == board.number and board.end:
                last_move = -1
                
        for i in range(1, 3):
            pygame.draw.line(screen, DARK, (big_board_position[0] + (big_line_spacing * i), big_board_position[1]), (big_board_position[0] + (big_line_spacing * i), big_board_position[1] + big_board_height), 3)
            pygame.draw.line(screen, DARK, (big_board_position[0], big_board_position[1] + (big_line_spacing * i)), (big_board_position[0] + big_board_width, big_board_position[1] + (big_line_spacing * i)), 3)
    
    if winner == -1: winner = checkWin(big_board)
    elif winner == 1:
        text = "X Wins!"
        text_surface = font.render(text, True, BLUE)
        shadow_surface = font.render(text, True, SELECTED_LIGHT)
        
        text_rect = text_surface.get_rect()
        shadow_rect = shadow_surface.get_rect()
        
        text_cords = (int(display_width / 2) - int(text_rect.width / 2), int(display_height / 2) - text_rect.height)
        shadow_cords = (text_cords[0] + 5, text_cords[1] + 5)
        
        screen.blit(shadow_surface, shadow_cords)
        screen.blit(text_surface, text_cords)
        
    elif winner == 0:
        text = "O Wins!"
        text_surface = font.render(text, True, RED)
        shadow_surface = font.render(text, True, RED)
        
        text_rect = text_surface.get_rect()
        shadow_rect = shadow_surface.get_rect()
        
        text_cords = (int(display_width / 2) - int(text_rect.width / 2), int(display_height / 2) - text_rect.height)
        shadow_cords = (text_cords[0] + 5, text_cords[1] + 5)
        
        screen.blit(shadow_surface, shadow_cords)
        screen.blit(text_surface, text_cords)
        
    
    clock.tick(max_fps)
    
    # Update display
    pygame.display.update()
                