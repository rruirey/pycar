import pygame

from util.constants import WINDOW_SIZE, NAME

# Determines if the game is running or not.
running = False


def start() -> None:
    # Initialize pygame.
    pygame.init()

    # Create the window.
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption(NAME)

    # Create the tick loop.
    clock = pygame.time.Clock()

    # Run the game.
    global running
    running = True

    # then listen for events
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw the screen.
        screen.fill((255, 255, 255))

        # Updates the display.
        pygame.display.flip()

        # Limits the interface to 60 FPS.
        clock.tick(60)


def stop() -> None:
    global running
    running = False
