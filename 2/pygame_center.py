import pygame
from pygame.locals import QUIT


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


def center_position():
    pygame.display.init()

    # create surface
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # fill the display surface to white
    screen.fill((255, 255, 255))

    # create a surface and pass in a tuple containing its length and width
    surf = pygame.Surface((50, 50))
    # give the surface a black color to separate it from the display surface
    surf.fill((0, 0, 0))
    # draw surface to display surface at the center.
    # the surface anchor point is top-left corner,
    # so you have to subtract each width and height of surface and divide each by 2
    surf_center = (
        (SCREEN_WIDTH - surf.get_width()) // 2,
        (SCREEN_HEIGHT - surf.get_height()) // 2
    )
    screen.blit(surf, surf_center)
    # updates the entire screen with everything
    pygame.display.flip()

    running = True
    while running:
        # look at the every event in the queue
        for event in pygame.event.get():
            # if the user click the close button, stop the loop
            if event.type == QUIT:
                running = False

    pygame.quit()


if __name__ == '__main__':
    center_position()
