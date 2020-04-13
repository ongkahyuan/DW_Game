# Simple pygame program

# Import and initialize the pygame library
import pygame
import time
from pygame.locals import (K_ESCAPE, KEYDOWN, QUIT)
from Game.sprites import *

pygame.init()

player = Player()
user = pygame.sprite.Group()
enemies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
user.add(player)

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 650
score = 0

# Set up the drawing window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Corona Blaster")
font = pygame.font.SysFont("arial", 18)
font_big = pygame.font.SysFont("arial bold", 40)

FIRE_PROJ = pygame.USEREVENT +1
SPAWN_ENEMY = pygame.USEREVENT +2
pygame.time.set_timer(FIRE_PROJ,300)
pygame.time.set_timer(SPAWN_ENEMY, 300)
clock = pygame.time.Clock()

# Run until the user asks to quit
running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == FIRE_PROJ:
            new_proj = Projectile(player.rect.center)
            projectiles.add(new_proj)
            all_sprites.add(new_proj)
        elif event.type == SPAWN_ENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
    
    if pygame.sprite.groupcollide(user,enemies, False, True):
        player.lives -= 1
    if pygame.sprite.groupcollide(projectiles,enemies,True,True):
        score += 1
    
    if player.lives == 0:
        running = False
    
    #Rendering the Counter
    
    lives_counter = font.render("Lives: "+ str(player.lives), True, (175,175,175))
    score_counter = font.render("Score: " + str(score), True, (175,175,175))
    
    lives_rect = lives_counter.get_rect()
    score_rect = score_counter.get_rect()

    lives_rect.left = 10
    lives_rect.top = 10
    score_rect.left = 10
    score_rect.top = 40
    
    #Refreshing all elements
    screen.fill((255, 255, 255))
    for entity in all_sprites:
        entity.update()
        screen.blit(entity.surf, entity.rect)
    screen.blit(lives_counter,lives_rect)
    screen.blit(score_counter,score_rect)
    
    # Flip the display
    pygame.display.flip()
    clock.tick(30)

died = font_big.render("YOU DIED! ",True, (0,0,0),(255,255,255))
end_screen = font_big.render("SCORE: " + str(score),True, (0,0,0),(255,255,255))
died_rect = died.get_rect()
end_rect = end_screen.get_rect()
died_rect.center =(SCREEN_WIDTH/2, SCREEN_HEIGHT/2) 
end_rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2+30)
screen.blit(died, died_rect)
screen.blit(end_screen, end_rect)
pygame.display.flip()
time.sleep(4)

# Done! Time to quit.
pygame.quit()
player.control.stop()