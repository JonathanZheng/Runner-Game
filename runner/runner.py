import pygame
from sys import exit
from random import randint as r, choice
from runner_settings import *

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game Trial")

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.gravity = 0
        self.idx = 0
        
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
        
        self.frame_list = [player_walk_1, player_walk_2]
        self.image = self.frame_list[self.idx]
        self.rect = self.image.get_rect(bottomleft = (100, 300))
    
    def jump(self):
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = - jump_height

    def fall(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom > 300 or not game_active:
            self.rect.bottom = 300
            self.gravity = 0

    def move(self):
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= player_speed
        elif keys[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += player_speed

    def animation(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.image = self.frame_list[int(self.idx)]
            self.idx += 0.1

        if int(self.idx) == len(self.frame_list):
            self.idx = 0

    def update(self):
        self.jump()
        self.fall()
        self.move()
        self.animation()

class Obstacle(pygame.sprite.Sprite):

    def __init__(self, type):
        super().__init__()
        self.idx = 0

        if type == "snail":
            snail1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frame_list = [snail1, snail2]
            y_pos = 300
        else:
            fly1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frame_list = [fly1, fly2]
            y_pos = 200

        self.image = self.frame_list[self.idx]
        self.rect = self.image.get_rect(bottomleft = (r(850,1050), y_pos))

    def move(self):
        if self.rect.x <= -100:
            self.kill()
        self.rect.x -= obstacle_speed

    def animation(self):
        self.image = self.frame_list[int(self.idx)]
        self.idx += 0.1
        if int(self.idx) == len(self.frame_list):
            self.idx = 0

    def update(self):
        self.animation()
        self.move()
        
player_grp = pygame.sprite.GroupSingle()
player_grp.add(Player())

obstacle_grp = pygame.sprite.Group()

def rng_events():
    global first, second, third, ok
    if ok:
        ok = False
        first = r(10, 16)
        second = r(18,27)
        third = r(35,40)

def increase_difficulty():
    global obstacle_speed, player_speed
    
    if current_score == 5:
        obstacle_speed = 6
    elif current_score == first:
        obstacle_speed = 12
    elif current_score == first + 1:
        obstacle_speed = 6
    elif current_score == 16:
        obstacle_speed = 7
        player_speed = 4.5
    elif current_score == second:
        obstacle_speed = 12
    elif current_score == second + 1:
        obstacle_speed = 8
    elif current_score == third:
        obstacle_speed = 13
    elif current_score == third + 1:
        obstacle_speed = 9
    elif current_score == 50:
        obstacle_speed = 11
        player_speed = 3

def redraw_screen():
    screen.blit(sky, (0, 0))
    screen.blit(ground, (0, 300))

    player_grp.draw(screen)
    player_grp.update()
    obstacle_grp.draw(screen)
    obstacle_grp.update()

def display_scores():
    global current_score

    current_score = int(pygame.time.get_ticks()*(60/FPS)/1000 - start_time)
    score = font.render(str(current_score), False, (93, 63, 211))
    score_rect = score.get_rect(center = (400, 60))

    highscore = small_font.render("Highscore: " + str(high_score), False, (93, 63, 211) )
    highscore_rect = highscore.get_rect(center = (400, 90))

    screen.blit(score, score_rect)
    screen.blit(highscore, highscore_rect)

def check_collision():
    global game_active, high_score, obstacle_speed, player_speed, ok

    if pygame.sprite.spritecollide(player_grp.sprite, obstacle_grp, False):
        game_active = False
        ok = True
        high_score = max(high_score, current_score)
        obstacle_speed, player_speed = 5, 4

        obstacle_grp.empty()
        player_grp.sprite.rect = player_grp.sprite.image.get_rect(bottomleft = (100, 300))
        player_grp.sprite.gravity = 0

def end_screen():
    screen.fill((94, 129, 162))
    screen.blit(player_stand, player_stand_rect)
    screen.blit(game_name, game_name_rect)

    if high_score == 0:
        screen.blit(game_msg, game_msg_rect)
    else:
        highscore = font.render("Highscore: " + str(high_score), False, (255,255,51))
        highscore_rect = highscore.get_rect(center = (400, 345))
        screen.blit(highscore, highscore_rect)
    
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        keys = pygame.key.get_pressed()
        if game_active:
            if event.type == obstacle_timer:
                obstacle_grp.add(Obstacle(choice(['snail', 'snail', 'fly'])))
        else:
            if keys[pygame.K_RETURN]:
                game_active = True
                start_time = pygame.time.get_ticks()*(60/FPS)/1000

    if game_active:
        rng_events()
        redraw_screen()
        display_scores()
        increase_difficulty()
        check_collision()
        
    else:
        end_screen()
    
    pygame.display.flip()
    clock.tick(FPS)