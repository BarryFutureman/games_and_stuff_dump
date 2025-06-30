import pygame
import pygame.math as pgm
import ui
from mia_interface import *

import win32api
import win32con
import win32gui
from pygame.locals import *
from ctypes import windll, Structure, c_long, byref


ScreenWidth, ScreenHeight = 300, 600

pygame.init()
main_window = MainWindow()
screen = main_window.screen


# set up the text input
input_box = ui.TextInput((0, (main_window.height-45) * main_window.scale), main_window)

# -----------------------------
# Set running and moving values
running = True

mouse_down_pos = query_mouse_pos()
mouse_down = False
# Setting what happens when game
# is in running state
while running:
    # Update every frame
    game_events = pygame.event.get()
    main_window.update(game_events)
    for event in game_events:
        input_box.handle_event(event)
        if event.type == MOUSEMOTION:
            if mouse_down:
                hwnd = pygame.display.get_wm_info()['window']
                x, y = query_mouse_pos()
                windll.user32.SetWindowPos(hwnd, 0, int(x-mouse_down_pos[0]), int(y-mouse_down_pos[1]), 0, 0, 0x0001)
                # r = event.rel
                # print(r)
                # windll.user32.MoveWindow(hwnd, int(0), int(0), 0, 0, False)
        elif event.type == MOUSEBUTTONDOWN:
            mouse_down = True
            mouse_down_pos = pygame.mouse.get_pos()
            # left, top, right, bottom = win32gui.GetWindowRect(hwnd)
            # screen_pos = (left, top)
        elif event.type == MOUSEBUTTONUP:
            mouse_down = False
    """
    new_mouse_pos = query_mouse_pos()
    r = list(pgm.Vector2(new_mouse_pos) - pgm.Vector2(last_mouse_pos))
    last_mouse_pos = new_mouse_pos
    # Get handle of the window and move it
    hwnd = pygame.display.get_wm_info()['window']
    print(r)
    windll.user32.MoveWindow(hwnd, int(r[0]), int(r[1]), ScreenWidth, ScreenHeight, False)
    """
    input_box.update()

    # Set screen color and image on screen
    screen.fill(fuchsia)
    input_box.draw(screen)

    # Update the GUI pygame
    pygame.display.update()

# Quit the GUI game
pygame.quit()