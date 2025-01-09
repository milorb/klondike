import pygame
from board import Board
from input import InputManager


class Game:
    """
    Manages the Pygame window and main game loop
    """

    def __init__(self, w, h) -> None:

        pygame.init()
        self.screen = pygame.display.set_mode(
            (w, h), 
            flags=pygame.SCALED, 
            vsync=1)

        icon = pygame.image.load("assets/big_spade.png")
        pygame.display.set_caption("klondike")
        pygame.display.set_icon(icon)

        bg_img = pygame.image.load("assets/board.png").convert_alpha()
        self.bg = pygame.transform.scale_by(bg_img, 2)

        self.clock = pygame.time.Clock()
        self.bg_color = (30, 100, 90, 255)

        self.board = Board()

        InputManager.init()

    def run(self):

        self.running = True
        self.board.setup()

        while self.running:
            InputManager.frame_start()
            
            self.input_()
            self.update_()
            self.render_()
            self.clock.tick(60)

        pygame.quit()

    def input_(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.board.restart()

            InputManager.process_input(event)

        InputManager.cursor_pos = pygame.mouse.get_pos()
        InputManager.cursor_rel_pos = pygame.mouse.get_rel()

    def update_(self):
        self.board.update()

    def render_(self):

        self.screen.fill("white")
        self.screen.blit(self.bg, (0,0))
        self.board.draw(self.screen)

        pygame.display.flip()


game = Game(1280, 720)
game.run()
