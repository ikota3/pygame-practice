import pygame
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)
import random
import os

# define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# directory for images
IMG_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '../images'))
# directory for sounds
SOUND_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '../sounds'))


# define a Player object by extending pygame.sprite.Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load(os.path.join(IMG_DIR, 'jet.png')).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self, keys):
        # if the key was pressed, move the .rect to proper direction
        # move_ip stands for move in place
        if keys[K_UP]:
            self.rect.move_ip(0, -5)
            move_up_sound.play()
        if keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            move_down_sound.play()
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
        self.surf = pygame.image.load(os.path.join(IMG_DIR, 'missile.png')).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            # setting position for surface
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )
        self.speed = random.randint(5, 20)

    # move the sprite based on speed
    # remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load(os.path.join(IMG_DIR, 'cloud.png')).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )

    # move the cloud based on a constant speed
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()


# setup for sounds
# if you want change the default of mixer,
# you have to initialize before the all module initialize
pygame.mixer.init()

# initializing all pygame module
pygame.init()

# create surface
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# create a custom event for adding a new enemy and a cloud
ADD_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_ENEMY, 250)
ADD_CLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADD_CLOUD, 1000)

# setup the clock for a decent frame rate
clock = pygame.time.Clock()

# instantiate player
player = Player()

# create groups to hold enemy sprites and all sprites
# enemies is used for collision detection and position updates
# all_sprites is used for rendering
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# set up background music
# Sound source: http://ccmixter.org/files/Apoxode/59262
# License: https://creativecommons.org/licenses/by/3.0/
pygame.mixer.music.load(os.path.join(SOUND_DIR, 'ApoxodeElectric1.mp3'))
pygame.mixer.music.play(loops=-1)

# load all sound files
# Sound sources: Jon Fincher
move_up_sound = pygame.mixer.Sound(f'{SOUND_DIR}/Rising_putter.ogg')
move_down_sound = pygame.mixer.Sound(f'{SOUND_DIR}/Falling_putter.ogg')
collision_sound = pygame.mixer.Sound(f'{SOUND_DIR}/Collision.ogg')

# Set the base volume for all sounds
move_up_sound.set_volume(0.5)
move_down_sound.set_volume(0.5)
collision_sound.set_volume(0.5)

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
        elif event.type == ADD_ENEMY:
            # create the new enemy and add it to sprite group
            enemy = Enemy()
            enemies.add(enemy)
            all_sprites.add(enemy)
        elif event.type == ADD_CLOUD:
            # create the new cloud and add it to sprite group
            cloud = Cloud()
            clouds.add(cloud)
            all_sprites.add(cloud)

    # get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    # update the player sprite based on user keypress
    player.update(pressed_keys)

    # update the enemy
    enemies.update()

    # update the cloud
    clouds.update()

    # fill the display surface to white
    screen.fill((135, 205, 250))

    # draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()

        # stop any moving sounds and play the collision sound
        move_up_sound.stop()
        move_down_sound.stop()
        collision_sound.stop()

        running = False

    # update the display
    pygame.display.flip()

    # ensure program maintains a rate of 30 frames per second
    clock.tick(30)


pygame.mixer.music.stop()
pygame.mixer.quit()
pygame.quit()
