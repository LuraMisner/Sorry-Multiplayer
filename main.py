from board import Board
import constants
from client import Client
import pygame
import time


def main():
    # Initialize the window
    pygame.init()
    WIN = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
    pygame.display.set_caption("Sorry!")
    clock = pygame.time.Clock()

    client = Client(WIN)
    client.select_color()

    run = True
    while run:
        WIN.fill((192, 192, 192))
        client.draw_screen()
        client.check_our_turn()

        # Check for a quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Update the window
        pygame.display.update()
        clock.tick(60)


main()
