import pygame
from connectfour import ConnectFour as CF
import time

def run_game(game: CF) -> None:
    BLACK = (0, 0, 0)
    GRAY = (120, 120, 120)
    BLUE = (20, 60, 160)
    YELLOW = (200, 160, 40)
    RED = (200, 40, 40)
    GREEN = (0, 100, 0)
    SQUARE_WIDTH = 100
    SQUARE_HEIGHT = 80
    PIECE_SIZE = 30
    NROWS = game.nrows
    NCOLS = game.ncols
    FPS = 30

    pygame.init()
    screen = pygame.display.set_mode((SQUARE_WIDTH * (NCOLS), SQUARE_HEIGHT * (NROWS + 2)))
    pygame.display.set_caption("Connect Four")

    running = True
    while running:
        screen.fill(BLACK)
        pygame.draw.rect(screen, BLUE, (0, SQUARE_HEIGHT, SQUARE_WIDTH * NCOLS, SQUARE_HEIGHT * NROWS)) # Main blue board

        for y, row in enumerate(game.board): # Draw all of the pieces
            for x, piece in enumerate(row):
                if piece == 1:
                    pygame.draw.circle(screen, RED, ((.5 + x) * SQUARE_WIDTH, (1.5 + y) * SQUARE_HEIGHT), PIECE_SIZE)
                if piece == 0:
                    pygame.draw.circle(screen, GRAY, ((.5 + x) * SQUARE_WIDTH, (1.5 + y) * SQUARE_HEIGHT), PIECE_SIZE)
                if piece == -1:
                    pygame.draw.circle(screen, YELLOW, ((.5 + x) * SQUARE_WIDTH, (1.5 + y) * SQUARE_HEIGHT), PIECE_SIZE)
        
        x, _ = pygame.mouse.get_pos() # Where the mouse is

        if game.winner is None:
            if game.player == 1:
                pygame.draw.circle(screen, RED, (x, 0.5 * SQUARE_HEIGHT), PIECE_SIZE) # Draw a small piece tracking the mouse
            if game.player == -1:
                pygame.draw.circle(screen, YELLOW, (x, 0.5 * SQUARE_HEIGHT), PIECE_SIZE) # to see where it would go
        else:
            font = pygame.font.SysFont('Arial', min(SQUARE_HEIGHT // 2, SQUARE_WIDTH * NCOLS // 18)) # Game over text
            text = font.render('Game Over! Press enter to play again. ', True, GREEN)
            screen.blit(text, (0, SQUARE_HEIGHT // 6))

        time.sleep(1 / FPS) 

        pygame.display.flip() # Display the board

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # In order to exit out
                running = False 
            if event.type == pygame.MOUSEBUTTONDOWN: # Play a move where you click
                game.make_move(x // SQUARE_WIDTH)
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_ESCAPE: # Use escape to exit the window
                    running = False
                if event.key == pygame.K_RETURN: # Restart the game (after it is over)
                    if game.winner is not None:
                        game.reset()
        
    pygame.quit()

if __name__ == "__main__":
    game = CF()
    run_game(game)

# Have the thingy run the Monte Carlo thingy when the mouse is pressed