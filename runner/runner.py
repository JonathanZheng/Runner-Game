import pygame
from sys import exit
from random import randint as r, choice
from runner_settings import *

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.gravity = 0
        self.idx = 0
        

        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
        
        self.image = PLAYER["walk"][self.idx] 
        self.rect = self.image.get_rect(bottomleft = (100, 300))

        self.mask = pygame.mask.from_surface(self.image)
    
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
            self.image = PLAYER["walk"][int(self.idx)]
            self.idx += 0.1

        if int(self.idx) == len(PLAYER["walk"]):
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
            self.frame_list = SNAIL
            y_pos = 300

        else:
            self.frame_list = FLY
            y_pos = 200

        self.image = self.frame_list[self.idx]
        self.rect = self.image.get_rect(bottomleft = (r(1000,1200), y_pos))

        self.mask = pygame.mask.from_surface(self.image)

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

def redraw_screen():
    screen.blit(sky, (0, 0))
    screen.blit(ground, (0, 300))

    player_grp.draw(screen)
    obstacle_grp.draw(screen)

    player_grp.update()
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

def check_collision(): # Use masks
    global game_active, high_score, obstacle_speed, player_speed, ok

    if pygame.sprite.groupcollide(player_grp, obstacle_grp, False, False, pygame.sprite.collide_mask):    
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
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        keys = pygame.key.get_pressed()
        if game_active:
            if event.type == obstacle_timer:
                obstacle_grp.add(Obstacle(choice(['snail', 'snail', 'fly'])))
            if event.type == lvl_up_timer and obstacle_speed < max_obstacle_speed:
                obstacle_speed += 1
        else:
            if keys[pygame.K_RETURN]:
                game_active = True
                start_time = pygame.time.get_ticks()*(60/FPS)/1000

    if game_active:

        redraw_screen()
        display_scores()

        check_collision()
        
    else:
        end_screen()
    
    pygame.display.flip()
