import pygame, sys
from board import board

def player_input(screen):

    Mpos = pygame.mouse.get_pos()
    mouse_x = Mpos[0] 
    mouse_y = Mpos[1]
    #print Mpos

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            pygame.quit()
    	    sys.exit()


        if event.type == pygame.MOUSEBUTTONDOWN:    
            for piece in board.pieces:
                x, y = piece.w, piece.h

                if piece.x+x > mouse_x > piece.x and piece.y+y > mouse_y > piece.y:
                    piece.clicked()
            for piece in board.current_pegs:
                x, y = piece.w, piece.h

                if piece.x+x > mouse_x > piece.x and piece.y+y > mouse_y > piece.y:
                    piece.clicked()

