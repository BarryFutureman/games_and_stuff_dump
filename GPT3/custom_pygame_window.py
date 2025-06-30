import pygame
import ctypes

pygame.init()

width = 800
height = 600

# Create the Pygame window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("My Pygame Window")

# Get the window handle
hwnd = pygame.display.get_wm_info()["window"]

# Set the window position
x = 100
y = 100
ctypes.windll.user32.SetWindowPos(hwnd, 0, x, y, 0, 0, 0x0001)

# Set the window style
style = ctypes.windll.user32.GetWindowLongW(hwnd, -16)
style &= ~0x00C00000  # remove WS_CAPTION style
style &= ~0x00080000  # remove WS_BORDER style
ctypes.windll.user32.SetWindowLongW(hwnd, -16, style)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the display
    pygame.display.update()

pygame.quit()
