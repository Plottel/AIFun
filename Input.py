# Works just like SwinGame input system, but init() needs to be called
# to initialise everything.
#
# Consists of three main functions:
# key_down -> If the key is currently pressed
# key_typed -> If the key was pressed this frame
# key_released -> If the key was released this frame
#
# Mouse positions are fetched with mouse_x() and mouse_y()
#
# process_events() is exactly like SwinGame ProcessEvents() and needs
# to be called each frame.

import pygame
from enum import Enum


class KeyState(Enum):
    Down = 1        # Key is currently pressed
    Typed = 2       # Key was pressed this frame
    Released = 3    # Key was released this frame


class Input:
    # Pygame integer representations of mouse buttons
    __LEFT_MOUSE = 1
    __RIGHT_MOUSE = 3

    # Mouse values. Clicked is registered when the button is released
    left_mouse_clicked = False
    left_mouse_down = False
    right_mouse_clicked = False
    right_mouse_down = False

    # Key values
    keys = {}

    # Initialises variables and specifies which keys will be tracked for input
    @staticmethod
    def init():
        Input.add_key(pygame.K_w)
        Input.add_key(pygame.K_s)
        Input.add_key(pygame.K_a)
        Input.add_key(pygame.K_d)

    # Adds a new key to be tracked for input
    @staticmethod
    def add_key(key):
        Input.keys[key] = {}
        Input.keys[key][KeyState.Down] = False
        Input.keys[key][KeyState.Typed] = False
        Input.keys[key][KeyState.Released] = False

    # Specifies if a key is currently pressed
    @staticmethod
    def key_down(key):
        return Input.keys[key][KeyState.Down]

    # Specifies if a key has been pressed this frame
    @staticmethod
    def key_typed(key):
        return Input.keys[key][KeyState.Typed]

    # Specifies if a key has been released this frame
    @staticmethod
    def key_released(key):
        return Input.keys[key][KeyState.Released]

    # Returns the x position of the mouse
    @staticmethod
    def mouse_x():
        return pygame.mouse.get_pos()[0]

    # Returns the y position of the mouse
    @staticmethod
    def mouse_y():
        return pygame.mouse.get_pos()[1]

    # Updates all key and mouse states
    @staticmethod
    def process_events():
        Input.left_mouse_clicked = False
        Input.right_mouse_clicked = False

        # Typed and released states set to false at start of each frame
        for key in Input.keys:
            Input.keys[key][KeyState.Typed] = False
            Input.keys[key][KeyState.Released] = False

        # Process each event and map key / mouse states
        for event in pygame.event.get():
            # Key Down event
            if event.type == pygame.KEYDOWN:
                if event.key in Input.keys:
                    Input.keys[event.key][KeyState.Down] = True
                    Input.keys[event.key][KeyState.Typed] = True

            # Key Up event
            if event.type == pygame.KEYUP:
                if event.key in Input.keys:
                    Input.keys[event.key][KeyState.Down] = False
                    Input.keys[event.key][KeyState.Released] = True

            # Mouse Button Down event
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == Input.__LEFT_MOUSE:
                    Input.left_mouse_down = True
                elif event.button == Input.__RIGHT_MOUSE:
                    Input.right_mouse_down = True

            # Mouse Button Up event
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == Input.__LEFT_MOUSE:
                    Input.left_mouse_clicked = True
                    Input.left_mouse_down = False
                elif event.button == Input.__RIGHT_MOUSE:
                    Input.right_mouse_clicked = True
                    Input.right_mouse_down = False

            # Quit event
            if event.type == pygame.QUIT:
                pygame.quit()