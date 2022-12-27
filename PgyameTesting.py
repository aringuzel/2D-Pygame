import random
import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        player_1= pygame.image.load('graphics/player_walk_1.png').convert_alpha()
        player_2= pygame.image.load('graphics/player_walk_2.png').convert_alpha()
        self.player_walk = [player_1, player_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (200, 300))
        self.gravity = 0

        #self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        #self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            #self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
            
    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_frame1 = pygame.image.load('graphics/fly1.png').convert_alpha()
            fly_frame2 = pygame.image.load('graphics/fly2.png').convert_alpha()
            self.frames = [fly_frame1, fly_frame2]
            y_pos = 210
        else:
            snail_frame1 = pygame.image.load('graphics/snail1.png').convert_alpha()
            snail_frame2 = pygame.image.load('graphics/snail2.png').convert_alpha()
            self.frames = [snail_frame1, snail_frame2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
    
    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = TF.render(f'Score: {current_time}', False, (64,64,64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            
            if obstacle_rect.bottom == 300:
                screen.blit(snail, obstacle_rect)
            else:
                screen.blit(fly, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else:
        return []


def collision(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


def player_animation():
    global pl_surf, player_index
    if pl_rect.bottom < 300:
        pl_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        pl_surf = player_walk[int(player_index)]

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('ADVENTURE!')
clock = pygame.time.Clock()
TF = pygame.font.Font('font/Pixeltype.ttf', 50)
Game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.play(loops = -1)
bg_music.set_volume(0.3)


#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

back = pygame.image.load('graphics/0.jpg').convert()
ground = pygame.image.load('graphics/ground.png').convert()

#score = TF.render('My Game', False, (64, 64, 64))
#score_rect = score.get_rect(center = (400, 50))

#obstacles
snail_frame1 = pygame.image.load('graphics/snail1.png').convert_alpha()
snail_frame2 = pygame.image.load('graphics/snail2.png').convert_alpha()
snail_frames = [snail_frame1, snail_frame2]
snail_frame_index = 0
snail = snail_frames[snail_frame_index]

fly_frame1 = pygame.image.load('graphics/fly1.png').convert_alpha()
fly_frame2 = pygame.image.load('graphics/fly2.png').convert_alpha()
fly_frames = [fly_frame1, fly_frame2]
fly_frame_index = 0
fly = fly_frames[fly_frame_index]

obstacle_rect_list = []


player_1= pygame.image.load('graphics/player_walk_1.png').convert_alpha()
player_2= pygame.image.load('graphics/player_walk_2.png').convert_alpha()
player_walk = [player_1, player_2]
player_index = 0
player_jump = player_1= pygame.image.load('graphics/jump.png').convert_alpha()

pl_surf = player_walk[player_index]
pl_rect = player_1.get_rect(midbottom = (80, 300))
pl_gravity = 0

#Intro screen
player_stand = pygame.image.load('graphics/player_stand.png').convert_alpha()
player_stand = pygame.transform.scale2x(player_stand)
player_stand_rect = player_stand.get_rect(center = (400, 200))

game_name = TF.render('YO', False, (111,196,169))
game_name_rect = game_name.get_rect(center = (400, 60))


instruction = TF.render('Press space to start!', False, (111, 196, 169))
instruction_rect = instruction.get_rect(center = (400, 350))

#timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT+2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT+3
pygame.time.set_timer(fly_animation_timer, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if Game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and pl_rect.bottom >= 300:
                    pl_gravity = -20     
            
            
            if event.type == pygame.MOUSEBUTTONDOWN and pl_rect.bottom >= 300:      
                    pl_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                Game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

        if Game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
                #if randint(0, 2):
                    #obstacle_rect_list.append(snail.get_rect(bottomright = (randint(900, 1100),300)))
                #else:
                    #obstacle_rect_list.append(fly.get_rect(bottomright = (randint(900, 1100),210)))

            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail = snail_frames[snail_frame_index]
            
            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly = fly_frames[fly_frame_index]



    if Game_active:
        screen.blit(back, (0, 0))
        screen.blit(ground, (0, 300))
        #pygame.draw.rect(screen, '#c0e8ec', score_rect)
        #pygame.draw.rect(screen, '#c0e8ec', score_rect, 10)
        #screen.blit(score, score_rect)
        score = display_score()

        #s_rect.x -= 4
        #if s_rect.right <= 0:
            #s_rect.left = 800
        #screen.blit(snail, s_rect)

        #Player
        #pl_gravity += 1
        #pl_rect.y += pl_gravity
        #if pl_rect.bottom >= 300:
            #pl_rect.bottom = 300
        #player_animation()
        #screen.blit(pl_surf, pl_rect)
        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        #obsatcle movement
        #obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        #collision
        Game_active= collision_sprite()
        #Game_active = collision(pl_rect, obstacle_rect_list)

    else:
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()
        pl_rect.midbottom = (80, 300)
        player_gravity = 0

        score_message = TF.render(f'Your score: {score} Press space to restart', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center = (400, 350))
        if score == 0:
            screen.blit(game_name, game_name_rect)
            screen.blit(instruction, instruction_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)