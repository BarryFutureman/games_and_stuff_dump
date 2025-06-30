# importing required library
import pygame

# activate the pygame library .
pygame.init()
X = 1280
Y = 720
card_scale = 0.25

# create the display surface object
# of specific dimension..e(X, Y).
scrn = pygame.display.set_mode((X, Y))

# set the pygame window name
pygame.display.set_caption('image')

# Text
font = pygame.font.Font('Assets/Fonts/roguehero.ttf', 9)
energy_text = font.render(str(12), True, (95,185,255))
energy_textRect = energy_text.get_rect()
energy_textRect.center = (80 * card_scale, 35*card_scale)
power_text = font.render(str(12), True, (225,155,23))
power_textRect = power_text.get_rect()
power_textRect.center = (335*card_scale, 35*card_scale)

# create a surface object, image is drawn on it.
imp = pygame.image.load("Assets/PNGs/HeroCard_Batman.png").convert_alpha()
imp = pygame.transform.smoothscale(imp, (822*card_scale, 1122*card_scale))

# Using blit to copy content from one surface to other
scrn.blit(imp, (0, 0))
scrn.blit(energy_text, energy_textRect)
scrn.blit(power_text, power_textRect)

# paint screen one time
pygame.display.flip()
status = True
while (status):

    # iterate over the list of Event objects
    # that was returned by pygame.event.get() method.
    for i in pygame.event.get():

        # if event object type is QUIT
        # then quitting the pygame
        # and program both.
        if i.type == pygame.QUIT:
            status = False

# deactivates the pygame library
pygame.quit()