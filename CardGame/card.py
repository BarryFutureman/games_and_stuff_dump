import pygame
from pygame import math as pgm

# Global variables
DIMENSION = (822, 1122)  # Regular card dimension
HeroCard_SCALE = 0.1
DestinyCard_SCALE = 0.15
BattlegroundCard_SCALE = 0.1


class Card:
    def __init__(self, n, d, front, pos):
        self.name = n
        self.description = d
        self.card_front = front
        self.pos = pgm.Vector2(pos)
        self.anchor = pgm.Vector2(pos)

    def on_drag(self, offset):
        self.card_front.move_ip(offset)
        self.pos += offset

    def on_release(self):
        self.set_position(self.anchor.copy())

    def set_position(self, new_pos):
        offset = new_pos - self.pos
        self.pos = pgm.Vector2(new_pos)
        self.card_front.move_ip(offset)
        return offset

    def set_anchor_position(self, new_anchor_pos):
        self.anchor = pgm.Vector2(new_anchor_pos)
        self.set_position(new_anchor_pos)

    def draw(self, screen):
        self.card_front.draw(screen)

    def get_main_rect(self):
        return self.card_front.rect

    def update(self):
        pass


class HeroCard(Card):
    def __init__(self, n, d, img_path, pos, cst, pwr, tags, game_, owner_card_group):
        self.game_manager = game_
        self.owner = owner_card_group
        card_front = CardFront(img_path, HeroCard_SCALE, pos)
        self.stat_texts = HeroStatTexts(pos, cst, pwr)
        Card.__init__(self, n, d, card_front, pos)
        self.cost = cst
        self.power = pwr
        self.tags = tags

    def on_drag(self, offset):
        Card.on_drag(self, offset)
        self.stat_texts.move_ip(offset)

    def set_position(self, new_pos):
        offset = Card.set_position(self, new_pos)
        self.stat_texts.move_ip(offset)

    def draw(self, screen):
        Card.draw(self, screen)
        self.stat_texts.draw(screen)

    def on_drop_to_slot(self, position):
        self.set_anchor_position(position)

    def transfer(self, new_card_group):
        self.owner.transfer_card(self, new_card_group)


class DestinyCard(Card):
    def __init__(self, n, d, img_path, pos):
        card_front = CardFront(img_path, DestinyCard_SCALE, pos)
        Card.__init__(self, n, d, card_front, pos)


class UnrevealedCard(Card):
    def __init__(self, n, d, img_path, pos, scale):
        card_front = CardFront(img_path, scale, pos)
        Card.__init__(self, n, d, card_front, pos)


class BattlegroundCard(Card):
    def __init__(self, n, d, img_path, pos):
        card_front = CardFront(img_path, BattlegroundCard, pos)
        Card.__init__(self, n, d, card_front, pos)


class CardFront:
    def __init__(self, base_image_path, card_scale, pos):
        self.scale = card_scale
        self.pos = pgm.Vector2(pos)
        self.width = DIMENSION[0] * self.scale
        self.height = DIMENSION[1] * self.scale

        # Card base image
        self.image = pygame.image.load(base_image_path).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def move_ip(self, offset):
        self.pos += offset
        self.rect.move_ip(offset)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class HeroStatTexts:
    def __init__(self, position, cost, power):
        self.pos = pgm.Vector2(position)
        self.scale = HeroCard_SCALE
        self.width = DIMENSION[0] * self.scale
        self.height = DIMENSION[1] * self.scale
        # Texts
        self.font1 = pygame.font.Font('Assets/Fonts/origintech.ttf', 18)
        self.cost_text = self.font1.render(str(cost), True, (205, 205, 255))
        self.cost_text_rect = self.cost_text.get_rect()
        self.cost_text_rect.center = self.pos + pgm.Vector2(-self.width/2+12, -self.height/2-9)
        self.power_text = self.font1.render(str(power), True, (235, 225, 205))
        self.power_text_rect = self.power_text.get_rect()
        self.power_text_rect.center = self.pos + pgm.Vector2(self.width/2-12, -self.height/2-9)

    def move_ip(self, offset):
        self.pos += offset
        self.cost_text_rect.move_ip(offset)
        self.power_text_rect.move_ip(offset)

    def draw(self, screen):
        screen.blit(self.cost_text, self.cost_text_rect)
        screen.blit(self.power_text, self.power_text_rect)

    def update(self, cost, power):
        self.cost_text = self.font1.render(str(cost), True, (205, 205, 255))
        self.power_text = self.font1.render(str(power), True, (235, 225, 205))


class TotalPowerNumberDisplay:
    def __init__(self, position):
        self.pos = pgm.Vector2(position)
        self.width = 50
        self.height = 50
        # Texts
        self.font1 = pygame.font.Font('Assets/Fonts/origintech.ttf', 30)
        self.power_text = self.font1.render(str(0), True, (235, 235, 255))
        self.power_text_rect = self.power_text.get_rect()
        self.power_text_rect.center = self.pos + pgm.Vector2(0, 0)

        # Backdrop image
        self.image = pygame.image.load("Assets/PNGs/DamageNumberBackdrop.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (self.power_text_rect.width, self.power_text_rect.height))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.power_text, self.power_text_rect)

    def update(self, power):
        self.power_text = self.font1.render(str(power), True, (235, 235, 255))
        self.power_text_rect = self.power_text.get_rect()
        self.power_text_rect.center = self.pos
        self.image = pygame.transform.smoothscale(self.image, (self.power_text_rect.width, self.power_text_rect.height))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

"""
class DebugWindow:
    def __init__(self, position):
        self.pos = pgm.Vector2(position)
        self.width = 50
        self.height = 50
        # Texts
        self.font1 = pygame.font.Font('Assets/Fonts/origintech.ttf', 30)
        self.text = self.font1.render(str(0), True, (235, 235, 255))
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.pos + pgm.Vector2(0, 0)

        # Backdrop image
        self.image = pygame.image.load("Assets/PNGs/DamageNumberBackdrop.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (self.text_rect.width, self.text_rect.height))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def set_text(self, text):
        self.text = self.font1.render(str(text), True, (235, 235, 255))
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.pos
        self.image = pygame.transform.smoothscale(self.image,
                                                  (self.text_rect.width * 1.2,
                                                   self.text_rect.height * 1.2))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def log(self, text):
        self.set_text(str(text))"""


class RoundDisplay:
    def __init__(self, position):
        self.pos = pgm.Vector2(position)
        self.width = 50
        self.height = 50
        # Texts
        self.font1 = pygame.font.Font('Assets/Fonts/Exo Space DEMO.ttf', 50)
        self.text = self.font1.render(str(0), True, (235, 235, 255))
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.pos + pgm.Vector2(0, 0)

        # Backdrop image
        self.image = pygame.image.load("Assets/PNGs/DamageNumberBackdrop.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (self.text_rect.width, self.text_rect.height))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def set_text(self, text):
        self.text = self.font1.render(str(text), True, (235, 235, 255))
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.pos
        self.image = pygame.transform.smoothscale(self.image,
                                                  (self.text_rect.width * 1.2,
                                                   self.text_rect.height * 1.2))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def draw(self, screen):
        # screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def log(self, text):
        self.set_text(str(text))