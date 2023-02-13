import pygame 

FPS = 60
game_active = False
ok = True
screen_width, screen_height = 800, 400
start_time = 0
current_score = 0
high_score = 0
player_speed = 4
jump_height = 21
obstacle_speed = 5
max_obstacle_speed = 10

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game Trial")

sky = pygame.image.load('graphics/sky.png').convert_alpha()
ground = pygame.image.load('graphics/ground.png').convert_alpha()

PLAYER = {}

player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400, 200))

PLAYER["walk"] = (
    player_walk_1 := pygame.image.load('graphics/player/player_walk_1.png').convert_alpha(),
    player_walk_2 := pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
)

PLAYER["jump"] = pygame.image.load('graphics/player/jump.png').convert_alpha()

SNAIL = (
    snail1 := pygame.image.load('graphics/snail/snail1.png').convert_alpha(),
    snail2 := pygame.image.load('graphics/snail/snail2.png').convert_alpha()
)


FLY = (
    fly1 := pygame.image.load('graphics/fly/fly1.png').convert_alpha(),
    fly2 := pygame.image.load('graphics/fly/fly2.png').convert_alpha()
)

font = pygame.font.Font('font/pixeltype.ttf', 50)
small_font = pygame.font.Font('font/pixeltype.ttf', 35)

game_name = font.render("[Insert game name]", False, (255,255,51))
game_name_rect = game_name.get_rect(center = (400, 65))

game_msg = font.render("Press [ENTER] to run", False, (255,255,51))
game_msg_rect = game_msg.get_rect(center = (400, 345))

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

lvl_up_timer = pygame.USEREVENT + 2
pygame.time.set_timer(lvl_up_timer, 10000)
