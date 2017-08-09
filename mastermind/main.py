import pygame, sys, words, random
from player_input import player_input
from board import *

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((544, 416))

clock = pygame.time.Clock()
FPS = 20
total_frames = 0

board_img = pygame.image.load('images/mm_board.png')
while True:

    screen.fill((150,150,150))

    screen.blit(board_img, (0,0))

    player_input(screen)

    board.update(screen)

    pygame.display.set_caption("Mastermind")
    pygame.display.flip()
    clock.tick(FPS)
    total_frames += 1
