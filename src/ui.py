import pygame
from pygame import Color, sprite, image, transform
from debug import Debug
from input import InputManager
from scene import Scene

class Button(sprite.Sprite):
    """
    base button class
    """

    def __init__(self, img, down_img, pos, func, *args):
        super().__init__()
        
        self.image = img

        self.up_image = img
        self.hovered_image = img.copy()
        self.down_image = down_img
 
        self.hover_color = Color(15,15,15,255)

        self.rect = img.get_rect()
        self.rect.x = pos.x
        self.rect.y = pos.y

        self.func = func
        self.func_args = args

        self.hovered = False
        self.down = False

    def update(self):
        if InputManager.MOUSE_LEFT_UP() or not InputManager.MOUSE_LEFT():
            if InputManager.MOUSE_LEFT_UP():
                self.on_release()
            self.image = self.up_image
            self.down = False

        if self.rect.collidepoint(InputManager.cursor_pos):
            if InputManager.MOUSE_LEFT_DOWN():
                self.on_click()
            else:
                if not self.down: 
                    self.on_hover()
        else:
            if self.hovered and not self.down:
                self.image = self.up_image
                self.image.fill(self.hover_color, special_flags=pygame.BLEND_SUB)
                self.hovered = False

    def on_hover(self):
        if not self.hovered:
            self.image.fill(self.hover_color, special_flags=pygame.BLEND_ADD)
            self.hovered = True

    def on_click(self):
        if not self.down:
            self.down = True
            self.image = self.down_image
            

    def on_release(self):
        if self.down and self.rect.collidepoint(InputManager.cursor_pos):
            self.func(*self.func_args)


class UIAssets():

    @classmethod
    def load(cls):
        cls.reset_button = image.load("assets/button_reset.png").convert_alpha()
        cls.reset_button_down = image.load("assets/button_reset_down.png").convert_alpha()

        cls.settings_button = image.load("assets/button_settings.png").convert_alpha()
        cls.settings_button_down = image.load("assets/button_settings_down.png").convert_alpha()

        cls.settings_bg = image.load("assets/settings.png").convert_alpha()

class SettingsMenu(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.menu = transform.scale_by(UIAssets.settings_bg, 2)
        self.menu_rect = self.menu.get_rect()
        
    def on_exit(self, *args):
        Debug.Log("closed settings menu")
        self.game.settings_button.func_args = (self,)

    def on_swap(self, *args):
        Debug.Log("opened settings menu")
        self.prev_bg = self.game.prev_screen.copy()
        self.prev_bg.fill(Color(15,15,8,20), special_flags=pygame.BLEND_SUB)

        self.game.settings_button.func_args = (self.game.board,)

    def draw(self):
        x = self.prev_bg.get_width() / 2
        y = self.prev_bg.get_height() / 2

        x = x - (self.menu_rect.width / 2)
        y = y - (self.menu_rect.height / 2)

        self.prev_bg.blit(self.menu, (x, y))
        self.game.screen.blit(self.prev_bg, (0,0))
        




