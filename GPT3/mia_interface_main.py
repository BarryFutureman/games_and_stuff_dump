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
FPS = 60 # frames per second setting
fpsClock = pygame.time.Clock()
main_window = MainWindow()
screen = main_window.screen


# -----------------------------
# Set running and moving values
running = True

mouse_down_pos = query_mouse_pos()
mouse_down = False
# Setting what happens when game
# is in running state
while running:
    dt = fpsClock.tick(FPS)

    # Update every frame
    events = pygame.event.get()
    for event in events:
        # Close if the user quits
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        # Pass event to main window
        main_window.handle_event(event)

    main_window.update(dt)

    # Set screen color and image on screen
    screen.fill(fuchsia)
    main_window.draw()

    # Update the GUI pygame
    pygame.display.update()

# Quit the GUI game
pygame.quit()