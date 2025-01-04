import pygame

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

        self.clock = pygame.time.Clock()
        self.bg_color = (30, 100, 90, 255)


    def run(self):

        self.running = True

        while self.running:
            self.input_()
            self.update_()
            self.render_()

            self.clock.tick(60)

        pygame.quit()

    def input_(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update_(self):

        pass

    def render_(self):

        self.screen.fill(self.bg_color)
        pygame.display.flip()


game = Game(1280, 720)
game.run()
