import pygame
from card import CardAssets
from scene import Scene
from board import Board
from input import InputManager
from ui import Button, SettingsMenu, UIAssets


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

        InputManager.init()

        CardAssets.load()
        UIAssets.load()

        bg_img = pygame.image.load("assets/klondike_bg.png").convert_alpha()
        self.bg = pygame.transform.scale_by(bg_img, 2)

        self.clock = pygame.time.Clock()
        self.bg_color = (30, 100, 90, 255)

        self.board = Board(self)
        self.settings_menu = SettingsMenu(self)

        self.active_scene: Scene = self.board

        self.settings_button = Button(
            UIAssets.settings_button, 
            UIAssets.settings_button_down, 
            pygame.Vector2(w - 40, 10), 
            self.swap_scene, 
            self.settings_menu)

        
    def run(self):

        self.running = True
        self.board.setup()

        while self.running:
            
            self.input_()
            self.update_()
            self.render_()
            self.clock.tick(60)

        pygame.quit()

    def input_(self):

        InputManager.frame_start()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.settings_button.func(*self.settings_button.func_args)
            else:
                InputManager.process_input(event)

    def update_(self):
        
        self.active_scene.update()
        self.settings_button.update()

    def render_(self):

        self.screen.fill("white")
        self.screen.blit(self.bg, (0,0))

        self.active_scene.draw()
        self.screen.blit(self.settings_button.image, self.settings_button.rect)

        self.prev_screen = self.screen.copy()

        pygame.display.flip()

    def swap_scene(self, new_scene):
        self.active_scene.on_exit()
        self.active_scene = new_scene
        self.active_scene.on_swap()

game = Game(1280, 720)
game.run()
