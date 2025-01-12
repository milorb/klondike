from typing import Tuple
import pygame
from pygame.event import Event


class InputManager:
    """
    class for managing the pygame event queue, 
    provides class method interface for determing clicks, etc
    """

    @classmethod
    def init(cls):
        cls.cursor_pos: Tuple[int, int] = (0, 0)
        cls.cursor_rel_pos: Tuple[int, int] = (0, 0)

        cls.mouse = [False, False, False]
        # per frame
        cls.mouse_down = [False, False, False]
        cls.mouse_up = [False, False, False]

    @classmethod
    def frame_start(cls):
        cls.cursor_pos = pygame.mouse.get_pos()
        cls.cursor_rel_pos = pygame.mouse.get_rel()

        cls.mouse_down = [False, False, False]
        cls.mouse_up = [False, False, False]

    @classmethod
    def process_input(cls, event: Event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            idx = event.button - 1
            cls.mouse_down[idx] = not cls.mouse[idx]
            cls.mouse[idx] = True

        elif event.type == pygame.MOUSEBUTTONUP:
            idx = event.button - 1
            cls.mouse_up[idx] = cls.mouse[idx]
            cls.mouse[idx] = False

    @classmethod
    def MOUSE_LEFT(cls) -> bool:
        return cls.mouse[0]

    @classmethod
    def MOUSE_LEFT_DOWN(cls) -> bool:
        return cls.mouse_down[0]

    @classmethod
    def MOUSE_LEFT_UP(cls) -> bool:
        return cls.mouse_up[0]

    @classmethod
    def MOUSE_RIGHT(cls) -> bool:
        return cls.mouse[2]

    @classmethod
    def MOUSE_RIGHT_DOWN(cls) -> bool:
        return cls.mouse_down[2]

    @classmethod
    def MOUSE_RIGHT_UP(cls) -> bool:
        return cls.mouse_up[2]


