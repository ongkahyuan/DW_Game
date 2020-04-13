# Simple pygame program

# Import and initialize the pygame library
import pygame
import time
import random

from pygame.locals import (
    K_w,
    K_s,
    K_a,
    K_d,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
from Game.YOLO.video_control import player_tracker


SCREEN_WIDTH = 500
SCREEN_HEIGHT = 650

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy,self).__init__()
        self.surf = pygame.Surface((30,30))
        self.surf.fill((180,100,0))
        self.rect = self.surf.get_rect(center = (random.randint(0,SCREEN_WIDTH),-random.randint(25, 125)))
        self.speed = 3
        
    def update(self):
        self.rect.move_ip(0,self.speed)
        if self.rect.bottom > SCREEN_HEIGHT:
            self.kill()

class Projectile(pygame.sprite.Sprite):
    def __init__(self,player_coords):
        super(Projectile,self).__init__()
        self.surf = pygame.Surface((3,10))
        self.surf.fill((30,200,180))
        self.rect = self.surf.get_rect(center=(player_coords))
        self.speed = 10
        
    def update(self):
        self.rect.move_ip(0,-self.speed)
        if self.rect.top <0:
            self.kill

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player,self).__init__()
        self.surf = pygame.Surface((25,25))
        self.surf.fill((50,140,180))
        self.rect = self.surf.get_rect()
        self.control = player_tracker()
        self.control.start()
        self.lives = 3
        
    def update(self):
        # self.rect.move_ip(self.control.x_val/25,self.control.y_val/25)
        # print(self.control.y_val)
        if -self.control.y_val >10:
            self.rect.move_ip(0,3)
        else:
            self.rect.move_ip(0,-5)
        self.rect.right = (self.control.x_val+50)/100*SCREEN_WIDTH*1.2

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= SCREEN_HEIGHT*5/9:
            self.rect.top = SCREEN_HEIGHT*5/9
        if self.rect.bottom >= SCREEN_HEIGHT*11/12:
            self.rect.bottom = SCREEN_HEIGHT*11/12
        if self.lives == 0:
            self.kill()


if __name__ == "__main__":
    pygame.init()

    player = Player()

    SCREEN_WIDTH = 500
    SCREEN_HEIGHT = 650

    # Set up the drawing window
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

    # Run until the user asks to quit
    running = True
    time.sleep(4)
    while running:

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        # Fill the background with white
        

        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
        
        screen.fill((255, 255, 255))
        screen.blit(player.surf,player.rect)
        
        # Flip the display
        pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()