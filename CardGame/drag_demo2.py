# Python program to move the image
# with the mouse

# Import the library pygame
import pygame
from pygame.locals import *
import hero_cards as hc
import destiny_cards as dc
import game

# Construct the GUI game
pygame.init()
FPS = 60 # frames per second setting
fpsClock = pygame.time.Clock()

# Set dimensions of game GUI
# w, h = 1920 * 4/5, 1080 * 4/5
screen = pygame.display.set_mode((game.ScreenWIDTH, game.ScreenHEIGHT), FULLSCREEN)

# Board prototype
bg_img = pygame.image.load("Assets/PNGs/BattleBoard_GothamCity.png").convert_alpha()
bg_img = pygame.transform.smoothscale(bg_img, (game.ScreenWIDTH, game.ScreenHEIGHT))
bg_img_rect = bg_img.get_rect()
screen.blit(bg_img, bg_img.get_rect())

# Game Manager
game_manager = game.GameManager(screen)
"""game_manager.card_manager.add_card(hc.UnrevealedHeroCard())
game_manager.card_manager.add_card(dc.UnrevealedDestinyCard())
game_manager.card_manager.add_card(hc.InjusticeBatman())
game_manager.card_manager.add_card(hc.InjusticeBatman())"""


# Create card
"""cards = []
new_card = hc.InjusticeBatman()
cards.append(new_card)
new_card = hc.CardBack()
cards.append(new_card)"""

# Set running and moving values
running = True
moving = False

# Setting what happens when game
# is in running state
while running:
    # Update every frame
    game_events = pygame.event.get()
    game_manager.update(game_events)
    for event in game_events:
        # Close if the user quits
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

    # Set screen color and image on screen
    screen.fill((85, 85, 95))
    screen.blit(bg_img, bg_img_rect)
    game_manager.draw()

    # Update the GUI pygame
    pygame.display.update()
    fpsClock.tick(FPS)

# Quit the GUI game
pygame.quit()
