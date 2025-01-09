from pygame import Color, sprite, image
import pygame
from input import InputManager

class Button(sprite.Sprite):
    """
    base button class
    """

    def __init__(self, img, pos, func, *args):
        super().__init__()
        
        self.image = img
        self.rect = img.get_rect()
        self.rect.x = pos.x
        self.rect.y = pos.y

        self.func = func
        self.func_args = args

        self.hovered = False

    def update(self):
        if self.rect.collidepoint(InputManager.cursor_pos):
            if InputManager.MOUSE_LEFT_DOWN():
                self.on_click()
            else:
                self.on_hover()
        else:
            if self.hovered:
                self.image.fill(Color(10,10,10,255), special_flags=pygame.BLEND_SUB)
            self.hovered = False

    def on_hover(self):
        if not self.hovered:
            color = Color(10,10,10,255)
            self.image.fill(color, special_flags=pygame.BLEND_ADD)
            self.hovered = True

    def on_click(self):
        self.func(*self.func_args)

class UIAssets():
    def __init__(self):

        self.reset_button = image.load("assets/button_reset.png").convert_alpha()

