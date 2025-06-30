import pygame
from pygame import math as pgm
from game import *

ScreenWIDTH, ScreenHEIGHT = 1920 * 4/5, 1080 * 4/5


class Debug:
    def __init__(self):
        self.debug_display = DebugDisplay((ScreenWIDTH*0.5, ScreenHEIGHT*0.4))

    def log(self, text):
        self.debug_display.update(text)

    def draw(self, _screen):
        self.debug_display.draw(_screen)


class DebugDisplay:
    def __init__(self, position):
        self.pos = pgm.Vector2(position)
        self.width = 50
        self.height = 50
        # Texts
        self.font1 = pygame.font.Font('Assets/Fonts/Exo Space DEMO.ttf', 15)
        self.power_text = self.font1.render(str("Debug display"), True, (255, 255, 255))
        self.power_text_rect = self.power_text.get_rect()
        self.power_text_rect.center = self.pos + pgm.Vector2(0, 0)

        # Backdrop image
        self.image = pygame.image.load("Assets/PNGs/DamageNumberBackdrop.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (self.power_text_rect.width, self.power_text_rect.height))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def set_text(self, text):
        self.power_text = self.font1.render(str(text), True, (235, 235, 255))
        self.power_text_rect = self.power_text.get_rect()
        self.power_text_rect.center = self.pos
        self.image = pygame.transform.smoothscale(self.image,
                                                  (self.power_text_rect.width * 1.2,
                                                   self.power_text_rect.height * 1.2))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.power_text, self.power_text_rect)

    def update(self, text):
        self.set_text(str(text))