import constants
from client import Client
import pygame
import sys


def main():
    # Initialize the window
    pygame.init()
    WIN = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
    pygame.display.set_caption("Sorry!")
    clock = pygame.time.Clock()

    # Character selection
    client = Client(WIN)

    try:
        client.select_color()
    except TypeError:
        print("Please start the server")
        sys.exit()

    run = True
    while run:
        WIN.fill((192, 192, 192))

        # If the game is going, draw the board. Otherwise, draw the end screen
        if not client.get_server_response('check_won'):
            client.draw_screen()
            client.check_our_turn()
        else:
            client.win_screen()

        # Check for a quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client.get_server_response('quit')
                run = False

        # Update the window
        pygame.display.update()
        clock.tick(60)


main()
