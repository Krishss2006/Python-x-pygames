

"""
        "Instructions:",
        "Press 'A' to move left, 'D' to move right. to take power_booster",
        "Click on Enemey using your mouse cursor to attack.",
        "Press 'Space' to start the start the game.",
        "Press 'Esc' to quit the game.",

"""

import pygame
from random import randint, choice
from time import sleep,time
from sys import exit

class Player(pygame.sprite.Sprite):
    def __init__(self,):
        super().__init__()
        # Player
        player_idle = pygame.image.load('player/idle/idle_0.png').convert_alpha()
        player_idle = pygame.transform.scale2x(player_idle)
        player_hurt = pygame.image.load('player/hurt/hurt_0.png').convert_alpha()
        player_hurt = pygame.transform.scale2x(player_hurt) 
        player_attacking = pygame.image.load('player/attack_1/attack_1_1.png').convert_alpha()
        player_attacking = pygame.transform.scale2x(player_attacking)
        players = [player_idle,player_hurt,player_attacking]
        self.player_motion = [player.set_colorkey((255,255,255)) for player in players]
        self.player_motion = [player_idle,player_hurt,player_attacking]
        self.player_index = 0


        self.image = self.player_motion[self.player_index]
        self.rect = self.image.get_rect(midbottom = (400,100))

    def handle_key_press(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_d] and key[pygame.K_a]:
            pass
        elif key[pygame.K_d]:
            self.rect.x+=5

        elif key[pygame.K_a]:
            self.rect.x-=5
    
    def handle_mouse_motion(self):
        player_index = 0
        mouse_motion = pygame.mouse.get_pressed()
        if mouse_motion[0]:
            self.image = self.player_motion[player_index+2]
        else:
            self.image = self.player_motion[player_index]
                    
    def player_boundation(self):
        if self.rect.x < 120:
            self.rect.x = 120 
        if self.rect.x > 620:
            self.rect.x = 620 

    def player_attack(self):
        mouse_pos = pygame.mouse.get_pos()

    def player_pos(self):
        return self.rect.x,self.rect.y

    
    def update(self):
        self.handle_key_press()
        self.handle_mouse_motion()
        self.player_boundation()
        self.player_attack()

class Powers(pygame.sprite.Sprite):
    def __init__(self, player_pos_x):
        super().__init__()
        power_up = pygame.image.load('power_up.png').convert_alpha()
        power_up = pygame.transform.rotozoom(power_up, 270, 0.03)
        self.image = power_up
        self.rect = self.image.get_rect()

        while True:
            power_pos_x = randint(130, 600)
            if abs(power_pos_x - player_pos_x) > 50:
                break

        self.rect.center = (power_pos_x, 100)

    def power_pos(self):
        return self.rect

    def power_kill(self,game_active=True):
        if game_active:
            pass
        else:
            self.kill()

    def update(self,game_active):
        self.power_kill(game_active)
        self.power_pos()

class Attack_by_player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        wind_slash_1 = pygame.image.load('wind_slash/wind_slash_1.png').convert_alpha()
        wind_slash_2 = pygame.image.load('wind_slash/wind_slash_2.png').convert_alpha()
        wind_slash_3 = pygame.image.load('wind_slash/wind_slash_3.png').convert_alpha()
        wind_slash_4 = pygame.image.load('wind_slash/wind_slash_4.png').convert_alpha()
        wind_slash_5 = pygame.image.load('wind_slash/wind_slash_5.png').convert_alpha()
        wind_slash_6 = pygame.image.load('wind_slash/wind_slash_6.png').convert_alpha()
        self.wind_slashes = [wind_slash_1,wind_slash_2,wind_slash_3,wind_slash_4,wind_slash_5,wind_slash_6]
        self.wind_slashe_index = 0

        self.image = self.wind_slashes[self.wind_slashe_index]
        attack_pos_x = player.sprite.player_pos()[0]+19
        self.rect = self.image.get_rect(midbottom = (attack_pos_x, 86)) #408, 64
        self.attack_sound = pygame.mixer.Sound('sfx/player_attack.wav')

    def particle_pos(self):
        attack_pos_x = player.sprite.player_pos()[0]+24
        attack_pos_y = 64
        self.rect.x = attack_pos_x -  24
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] < 120 or mouse_pos[0] > 660 or mouse_pos[1] < 150:
            cross_border = True
            pass
        else:
            pygame.draw.line(screen, 'Red', (attack_pos_x,attack_pos_y), mouse_pos, 5)
            self.attack_sound.play()
            self.attack_sound.set_volume(0.1)


    def animation_state(self):
        self.wind_slashe_index += 0.09
        if self.wind_slashe_index >= len(self.wind_slashes):
            self.wind_slashe_index = 0
        self.image = self.wind_slashes[int(self.wind_slashe_index)]

    def attack(self):
        self.init_pos = player.sprite.player_pos()

    def takes_attack(self, damage_amount):
        self.player_health -= damage_amount

    def update(self):
        self.attack()  
        self.particle_pos() 
        self.animation_state()
        if not game_active:
            self.kill()

class Enemies(pygame.sprite.Sprite):
    def  __init__(self):
        super().__init__()
        global score
        walk_up_0 = pygame.image.load('enemy/walk_up/walk_up_0.png').convert_alpha()
        walk_up_0 = pygame.transform.scale2x(walk_up_0)
        walk_up_1 = pygame.image.load('enemy/walk_up/walk_up_1.png').convert_alpha()
        walk_up_1 = pygame.transform.scale2x(walk_up_1) 
        walks = [walk_up_0,walk_up_1]

        self.walk_motion = [walk.set_colorkey((255,255,255)) for walk in walks]
        self.walk_motion = [walk_up_0,walk_up_1]
        self.walk_index = 0
        self.image = self.walk_motion[self.walk_index]
        self.rect = self.image.get_rect(midbottom = (randint(130,600),490))
        self.speed = 2 + (score // 7) 
        self.player_hurt_sound = pygame.mixer.Sound('sfx/hurt.wav')

    def animation_state(self):
        self.walk_index += 0.1
        if self.walk_index >= len(self.walk_motion):
            self.walk_index = 0
        self.image = self.walk_motion[int(self.walk_index)]

    def check_collision(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True
        else:
            return False

    def update(self):
        c= 0
        self.animation_state()
        self.rect.y -= self.speed
        if self.rect.y <= 120:
            self.kill()
            global player_health,  can_spawn_enemies
            player_health -= 1
            self.player_hurt_sound.play()
            self.player_hurt_sound.set_volume(1.0)
            if player_health <= 0:
                can_spawn_enemies = False
                return "GAME OVER"

            else:
                draw_hearts(player_health)  

def draw_hearts(health):
    heart_icon = pygame.image.load('heart_icon.png').convert_alpha()  
    heart_icon = pygame.transform.scale(heart_icon, (20, 20))    
    for i in range(health):
        pygame.draw.rect(screen, '#07050570', (700 - i * 20, 20, 20, 20))
        screen.blit(heart_icon, (700 - i * 20, 20))

def animate_game_over():
    screen.fill((0,0,0))
    text_font = pygame.font.Font(None,50)
    screen.blit(game_over_bg,game_over_bg_rect) 
    global score
    
    import csv
    high_score = 0

    try:
        with open('scores.csv', 'r') as file:
            scores = list(csv.reader(file))
            if scores:
                high_score = max(int(score[0]) for score in scores)
    except FileNotFoundError:
        high_score = 0

    if score > high_score:
        with open('scores.csv', 'w', newline='\n') as file:
            cw = csv.writer(file)
            cw.writerow([score])
        high_score = score

    high_score_message = text_font.render(f'High Score: {high_score}', True, ('Blue'))
    high_score_rect = high_score_message.get_rect(center=(400, 450))
    screen.blit(high_score_message, high_score_rect)

    score_message = text_font.render(f'Your Score: {score}', True, (255, 0, 0))
    score_message_rect = score_message.get_rect(center=(400, 400)) 
    screen.blit(score_message, score_message_rect)

    restart_text = text_font.render("Press 'Space' to restart the game", False, (255, 255, 255))
    restart_rect = restart_text.get_rect(center=(400, 350))  
    screen.blit(restart_text, restart_rect)  

def power_player_collision():
    power_up_sound = pygame.mixer.Sound('sfx/power_up.wav')
    if pygame.sprite.spritecollide(player.sprite,powerups,bool):
        global player_health
        player_health+=1
        power_up_sound.play()

def showing_score():
    global score
    border_color = (0, 0, 0)
    text_color = (242, 222, 199)  
    offsets = [(-1, -1), (1, -1), (-1, 1), (1, 1)]  # Offsets of border

    score_text = text_font.render(f"Score: {score}", True, text_color)
    score_rect = score_text.get_rect(center=(100, 50))

    for offset in offsets:
        border_position = (score_rect.x + offset[0], score_rect.y + offset[1])
        border_text = text_font.render(f"Score: {score}", True, border_color)
        screen.blit(border_text, border_position)

    screen.blit(score_text, score_rect)

def intro_screen():
    startTime = pygame.time.get_ticks() - start_time
    return startTime

## Initializing game
pygame.init()
screen = pygame.display.set_mode((800,500))
pygame.display.set_caption('Ghost Killer')
clock = pygame.time.Clock()
Frame_rate = 60
spaw_enemy_evnt = 2200
spaw_pwerup_evnt = 2000
game_active = False
show_instruction = False

global player_health,can_spawn_enemies, score
player_health = 7
can_spawn_enemies = True
score = 0

text_font = pygame.font.Font(None,50)

# Backround image
bg_surf = pygame.image.load('background.png').convert_alpha()
bg_surf = pygame.transform.smoothscale(bg_surf,(800,500))

intro_bg_surf = pygame.image.load('new_bg.jpeg').convert_alpha()
intro_bg_surf = pygame.transform.rotozoom(intro_bg_surf,0,0.49)

game_over_bg = pygame.image.load('game_over.png').convert_alpha()
game_over_bg = pygame.transform.rotozoom(game_over_bg,0,0.3)
game_over_bg_rect = game_over_bg.get_rect(center = (400,200))

# Player Class Call
player = pygame.sprite.GroupSingle()
player.add(Player())

# Attack Class 
attack = pygame.sprite.GroupSingle()
attack.add(Attack_by_player())

# Enemies Class
enemies = pygame.sprite.Group()

# PowerUps
powerups = pygame.sprite.GroupSingle()

# Bg music
bg_music = pygame.mixer.music.load('music/Phantom\'s Fury.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)
# Event
SPAWNENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWNENEMY, spaw_enemy_evnt) 

POWRUP = pygame.USEREVENT + 2
pygame.time.set_timer(POWRUP, spaw_pwerup_evnt)

mouse_down = False
start_time = 0

## Game Main Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

        if game_active:   
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True
                    
            else:
                mouse_down = False

            if event.type == SPAWNENEMY:
                if can_spawn_enemies:
                    enemies.add(Enemies())

            if player_health <= 0:
                can_spawn_enemies = False
                game_active = False
            
            if player_health <= 4 and player_health >= 1:
                player_pos_x = player.sprite.player_pos()[0]
                if event.type == POWRUP:
                    powerups.add(Powers(player_pos_x))

        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    score  = 0
                    game_active = True
                    can_spawn_enemies = True
   
    if game_active:
        screen.blit(bg_surf,(0,0))
        start_time = intro_screen()
        player.draw(screen)
        player.update()
        showing_score()
        if mouse_down:
            attack.draw(screen)
            attack.update()
        enemies.draw(screen)
        enemies.update()

        if mouse_down:
            for enemy in enemies:
                if enemy.check_collision(pygame.mouse.get_pos()):
                    enemy.kill()
                    score += 1 
        draw_hearts(player_health) 
        powerups.draw(screen) 
        power_player_collision()

    else:  
        screen.blit(bg_surf,(0,0))
        screen.fill((54,110,245))

        if start_time == 0:
            screen.blit(intro_bg_surf,(-20,0)) 
          
        else:
            animate_game_over()
            
        powerups.update(game_active)
        player_health = 7
        
    pygame.display.update()
    clock.tick(Frame_rate)
