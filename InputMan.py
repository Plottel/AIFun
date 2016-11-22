import pygame, sys

class InputMan:
    # Pygame integer representations of mouse buttons
    __LEFT_MOUSE = 1
    __RIGHT_MOUSE = 3

    # Mouse
    mouse_x = 0
    mouse_y = 0
    left_mouse_clicked = False
    left_mouse_down = False

    right_mouse_clicked = False
    right_mouse_down = False

    # W Key
    s_down = False
    s_typed = False
    s_released = False

    # S Key
    w_down = False
    w_typed = False
    w_released = False

    # A Key
    a_down = False
    a_typed = False
    a_released = False

    # D Key
    d_down = False
    d_typed = False
    d_released = False

    @staticmethod
    def process_events():
        InputMan.left_mouse_clicked = False
        InputMan.right_mouse_clicked = False

        InputMan.w_typed = False
        InputMan.w_released = False

        InputMan.s_typed = False
        InputMan.s_released = False

        # Process each event and map key / mouse states
        for event in pygame.event.get():
            #
            # KEY DOWN
            #
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    InputMan.w_down = True
                    InputMan.w_typed = True
                elif event.key == pygame.K_s:
                    InputMan.s_down = True
                    InputMan.s_typed = True
                elif event.key == pygame.K_a:
                    InputMan.a_down = True
                    InputMan.a_typed = True
                elif event.key == pygame.K_d:
                    InputMan.d_down = True
                    InputMan.s_typed = True

            #
            # KEY UP
            #
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    InputMan.w_down = False
                    InputMan.w_released = True
                elif event.key == pygame.K_s:
                    InputMan.s_down = False
                    InputMan.s_released = True
                elif event.key == pygame.K_a:
                    InputMan.a_down = False
                    InputMan.a_released = True
                elif event.key == pygame.K_d:
                    InputMan.d_down = False
                    InputMan.d_released = True

            #
            # MOUSE BUTTON DOWN
            #
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == InputMan.__LEFT_MOUSE:
                    InputMan.left_mouse_down = True
                elif event.button == InputMan.__RIGHT_MOUSE:
                    InputMan.right_mouse_down = True

            #
            # MOUSE BUTTON UP
            #
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == InputMan.__LEFT_MOUSE:
                    InputMan.left_mouse_clicked = True
                    InputMan.left_mouse_down = False
                elif event.button == InputMan.__RIGHT_MOUSE:
                    InputMan.right_mouse_clicked = True
                    InputMan.right_mouse_down = False

            #
            # MOUSE MOVEMENT
            #
            if event.type == pygame.MOUSEMOTION:
                InputMan.mouse_x = pygame.mouse.get_pos()[0]
                InputMan.mouse_y = pygame.mouse.get_pos()[1]

            #
            # QUIT
            #
            if event.type == pygame.QUIT:
                pygame.quit()