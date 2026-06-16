import pygame
from sys import exit
from random import randint

def obstacle_spawn(obstacle_list):
    global score
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300: screen.blit(snail_surf, obstacle_rect)
            else: screen.blit(fly_surf, obstacle_rect)
            if obstacle_rect.x < -50: score += 1
        
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    
    else: return []
def collisions(player, obstacles):
    if obstacles:
        for obstacles_rect in obstacles:
            if player.colliderect(obstacles_rect): return False
    return True
def player_animation():
    global player_surf, player_index

    if player_rect.bottom < 300: player_surf = player_jump
    else:  
        player_index += 0.1
        if player_index >= len(player_walk): player_index = 0
        player_surf = player_walk[int(player_index)]


pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Snails are stinky")
clock = pygame.time.Clock()
game_active = True

#sounds
pygame.mixer.init()
jump_sound = pygame.mixer.Sound("audio\jump.mp3")

#importing start menu
result_icon = pygame.image.load("graphics\Player\player_stand.png").convert_alpha() 
result_icon = pygame.transform.scale(result_icon, (200, 200))
result_icon_rect = result_icon.get_rect(center = (400, 200))
game_level = 0

#importing sky
sky = pygame.image.load("graphics\Sky.png")

#importing ground
ground = pygame.image.load("graphics\ground.png")

#importing obstacle
n = 800


snail_surf1 = pygame.image.load("graphics\snail\snail1.png").convert_alpha()
snail_surf2 = pygame.image.load("graphics\snail\snail2.png").convert_alpha()
snail_glide = [snail_surf1, snail_surf2]
snail_index = 0
snail_surf = snail_glide[snail_index]


fly_surf1 = pygame.image.load("graphics\Fly\Fly1.png").convert_alpha()
fly_surf2 = pygame.image.load("graphics\Fly\Fly2.png").convert_alpha()
fly = [fly_surf1, fly_surf2]
fly_index = 0
fly_surf = fly[fly_index]


#importing player
player_walk1 = pygame.image.load("graphics\Player\player_walk_1.png").convert_alpha()
player_walk2 = pygame.image.load("graphics\Player\player_walk_2.png").convert_alpha()
player_walk = [player_walk1, player_walk2]
player_index = 0
player_jump = pygame.image.load("graphics\Player\jump.png").convert_alpha()
player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (50, 300))
player_gravity = 0

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 2000)
obstacle_rect_list = []

snail_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_timer, 300)

fly_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_timer, 200)

#animation timre
animation_timer = pygame.USEREVENT
pygame.time.set_timer(animation_timer, 500)

#play again button
reload_surf = pygame.image.load("graphics\gameover\_reload.png").convert_alpha()
reload_surf = pygame.transform.scale(reload_surf, (50, 50))
reload_rect = reload_surf.get_rect(center = (600, 190))

#text
score = 0
sample_t_font = pygame.font.Font("font/Pixeltype.ttf", 50)
score_surf = sample_t_font.render(str(score), False, '#261F1F')
score_rect = score_surf.get_rect(midtop = (400, 10))
game_over = pygame.font.Font("font\Pixeltype.ttf", 100)
game_over_surf = game_over.render("GAME OVER!", True, "#FF0000")
game_over_rect = game_over_surf.get_rect(center = (400,200))
score_menu = sample_t_font.render("Score: " + str(score), True, "#1D1D1D")
score_menu_rect = score_menu.get_rect(center = (400, 350))
guide_surf = sample_t_font.render("(Press SPACE to start)", True, "#1F1F1F")
guide_rect = guide_surf.get_rect(center = (405, 80))
while True:

    score_surf = sample_t_font.render(str(score), False, '#261F1F')
    score_rect = score_surf.get_rect(midtop = (400, 10))
    score_menu = sample_t_font.render("Score: " + str(score), True, "#1D1D1D")
    score_menu_rect = score_menu.get_rect(center = (400, 350))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                player_gravity = -20
                jump_sound.play()
            if (event.key == pygame.K_SPACE and game_active == False):
                game_active = True
                score = 0
                # snail_rect.left = 800

        if event.type == pygame.MOUSEBUTTONDOWN:
            if player_rect.collidepoint(event.pos) and player_rect.bottom == 300: player_gravity = -20
            if reload_rect.collidepoint(event.pos) and game_active == False: 
                game_active = True
                # snail_rect.left = 800
        if game_active:
            if event.type == obstacle_timer:
                if randint(0,2): obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900,1100), 300)))
                else: obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900,1100), 200)))
            if event.type == snail_timer:
                if snail_index == 0: snail_index = 1
                else: snail_index = 0
                snail_surf = snail_glide[snail_index]
            if event.type == fly_timer:
                if fly_index == 0: fly_index = 1
                else: fly_index = 0
                fly_surf = fly[fly_index]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_level = 1

    if game_active:
        if game_level == 0:
            screen.fill("cyan3")
            screen.blit(result_icon, result_icon_rect)
            screen.blit(score_menu, score_menu_rect)
            screen.blit(guide_surf, guide_rect)
        else:
            screen.blit(sky,(0, 0))
            screen.blit(ground,(0, 300))
            screen.blit(score_surf, score_rect)

            #player
            player_gravity += 1
            player_rect.y += player_gravity
            if player_rect.bottom >= 300:
                player_rect.bottom = 300
            player_animation()
            screen.blit(player_surf, player_rect)

            #spawn logic obstacle
            obstacle_rect_list = obstacle_spawn(obstacle_rect_list)

            # snail_rect.left -= 5
            # if snail_rect.right < 0:
            #     score += 1
            #     snail_rect.left = 800 
            # screen.blit(snail_surf, snail_rect)

            #COLLISIONS
            game_active = collisions(player_rect, obstacle_rect_list)


    else:
        game_level = 0
        screen.fill("cyan3")
        screen.blit(result_icon, result_icon_rect)
        screen.blit(score_menu, score_menu_rect)
        screen.blit(guide_surf, guide_rect)
        obstacle_rect_list.clear()

    pygame.display.update()
    clock.tick(60)




