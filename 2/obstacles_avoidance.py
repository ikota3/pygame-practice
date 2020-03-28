import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)
import random

# define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


# define a Player object by extending pygame.sprite.Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()

    def update(self, keys):
        # if the key was pressed, move the .rect to proper direction
        # move_ip stands for move in place
        if keys[K_UP]:
            self.rect.move_ip(0, -5)
        if keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


# define the enemy object by extending pygame.sprite.Sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            # setting position for surface
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )
        self.speed = random.randint(5, 20)

    # move the sprite based on speed
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


# initializing all pygame module
pygame.init()

# create surface
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# instantiate player
player = Player()

running = True
while running:
    # look at the every event in the queue
    for event in pygame.event.get():
        # if the user hit the key
        if event.type == KEYDOWN:
            # if the hit key was Escape key, stop the loop
            if event.key == K_ESCAPE:
                running = False
        # if the user click the close button, stop the loop
        elif event.type == QUIT:
            running = False

    # get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()

    # update the player sprite based on user keypress
    player.update(pressed_keys)

    # fill the display surface to white
    screen.fill((0, 0, 0))

    # draw the player on the screen
    screen.blit(player.surf, player.rect)

    # update the display
    pygame.display.flip()


pygame.quit()
