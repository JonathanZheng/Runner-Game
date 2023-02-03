import pygame 
from sys import exit
from random import randint, choice 

pygame.init()
clock = pygame.time.Clock()

FPS = 60
game_active = False
screen_width, screen_height = 800, 400
start_time = 0
current_score = 0
high_score = 0

screen = pygame.display.set_mode((screen_width, screen_height))

sky = pygame.image.load('graphics/sky.png').convert_alpha()
ground = pygame.image.load('graphics/ground.png').convert_alpha()

player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400, 200))

font = pygame.font.Font('font/pixeltype.ttf', 50)
small_font = pygame.font.Font('font/pixeltype.ttf', 35)

game_name = font.render("[Insert game name]", False, (255,255,51))
game_name_rect = game_name.get_rect(center = (400, 65))

game_msg = font.render("Press [ENTER] to run", False, (255,255,51))
game_msg_rect = game_msg.get_rect(center = (400, 345))

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1150)