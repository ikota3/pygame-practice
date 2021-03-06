import pygame


def draw_circle():
    # initialize pygame
    # calling init to display module
    pygame.display.init()

    # set up the drawing window
    # pygame.display.set_mode() returns a Display Surface representing the visible part to the window
    screen = pygame.display.set_mode([250, 250])

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # if the user clicked the close button
                running = False

        # fill background with white color
        screen.fill((255, 255, 255))

        # draw solid blue circle in the center
        # 1: screen, 2: color, 3: position, 4: radius
        pygame.draw.circle(screen, (0, 0, 255), (125, 125), 75)

        # flip the display
        # the content of drawing circle will be pushed to the Display Surface
        # when you call pygame.display.flip()
        pygame.display.flip()

    # destroy display module
    pygame.display.quit()


if __name__ == '__main__':
    draw_circle()
