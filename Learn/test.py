# This is a test

import pygame
from sys import exit
from random import randint as r

pygame.init()
clock = pygame.time.Clock()
screen_width, screen_height = 800, 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game Trial")

FPS = 60
game_active = False
obstacle_rect_list = []
gravity = 0
start_time = 0
high_score = 0
current_score = 0
player_idx = 0
snail_idx = 0
fly_idx = 0

sky = pygame.image.load('graphics/sky.png').convert_alpha()
ground = pygame.image.load('graphics/ground.png').convert_alpha()

snail1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_list = [snail1, snail2]
snail = snail_list[snail_idx]

fly1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
fly2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
fly_list = [fly1, fly2]
fly = fly_list[fly_idx]

player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

player_list = [player_walk_1, player_walk_2]
player = player_list[player_idx]
player_rect = player.get_rect(bottomleft = (80, 300))

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

snail_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_timer, 500)

fly_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_timer, 200)

def player_animation():
    global player, player_idx

    if player_rect.bottom < 300:
        player = player_jump
    else:
        player = player_list[int(player_idx)]
        player_idx += 0.1

    if int(player_idx) == len(player_list):
        player_idx = 0

def redraw_screen():
    screen.blit(sky, (0, 0))
    screen.blit(ground, (0, 300))
    screen.blit(player, player_rect)

def display_scores():
    global current_score, high_score

    current_score = int(pygame.time.get_ticks()*(FPS/60)//1000- start_time)
    score = font.render(str(current_score), False, (93, 63, 211))
    score_rect = score.get_rect(center = (400, 60))

    highscore = small_font.render("Highscore: " + str(high_score), False, (93, 63, 211) )
    highscore_rect = highscore.get_rect(center = (400, 90))

    if not game_active:
        high_score = max(high_score, current_score)

    screen.blit(score, score_rect)
    screen.blit(highscore, highscore_rect)

def obstacle_movement():
    global obstacle_rect_list
    
    for obstacle_rect in obstacle_rect_list:
        obstacle_rect.x -= 7
        if obstacle_rect.bottom == 300:
            screen.blit(snail, obstacle_rect)
        else:
            screen.blit(fly, obstacle_rect)
    obstacle_rect_list = [obstacle for obstacle in obstacle_rect_list if obstacle.x >= -100]

def collision():
    for obstacle_rect in obstacle_rect_list:
        if player_rect.colliderect(obstacle_rect):
            return True
    return False

def end_screen():
    global gravity

    screen.fill((94, 129, 162))
    screen.blit(player_stand, player_stand_rect)
    screen.blit(game_name, game_name_rect)

    if high_score == 0:
        screen.blit(game_msg, game_msg_rect)
    else:
        highscore = font.render("Highscore: " + str(high_score), False, (255,255,51))
        highscore_rect = highscore.get_rect(center = (400, 345))
        screen.blit(highscore, highscore_rect)
    
    obstacle_rect_list.clear()
    player_rect.bottomleft = (80, 300)
    gravity = 0
    
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if not game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_active = True
                start_time = pygame.time.get_ticks()*(FPS/60)//1000
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    gravity = -20
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos):
                    gravity = -30

            if event.type == obstacle_timer:
                if r(0,2):
                    obstacle_rect_list.append(snail.get_rect(bottomleft = (r(900,1100), 300)))
                else:
                    obstacle_rect_list.append(fly.get_rect(bottomleft = (r(900,1100), 200)))
            
            if event.type == snail_timer:
                if snail_idx == 0:
                    snail_idx = 1
                else:
                    snail_idx = 0
                snail = snail_list[snail_idx]
            if event.type == fly_timer:
                if fly_idx == 0:
                    fly_idx = 1
                else:
                    fly_idx = 0
                fly = fly_list[fly_idx]

    if game_active:
        game_active = not collision()

        gravity += 1
        player_rect.y += gravity
        if player_rect.bottom > 300:
            player_rect.bottom = 300
            
        player_animation()
        redraw_screen()
        display_scores()
        obstacle_movement()

    else:
        end_screen()
    
    pygame.display.flip()
    clock.tick(FPS)