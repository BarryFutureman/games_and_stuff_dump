from card import *
from pygame import math as pgm


class UnrevealedHeroCard(UnrevealedCard):
    def __init__(self, owner_, hero_card_):
        # Base stats ----------------------------------------------------------
        hero_name = "Unrevealed Hero Card"
        hero_description = """
                Who is this?
                """
        img_path = "Assets/PNGs/HeroCard_Back.png"
        position = pgm.Vector2(0, 0)
        self.hero_card = hero_card_
        self.owner = owner_
        UnrevealedCard.__init__(self, hero_name, hero_description, img_path, position, HeroCard_SCALE)


class EmptySlotCard(Card):
    def __init__(self, owner_):
        self.owner = owner_
        img_path = "Assets/PNGs/EmptySlotCard.png"
        pos = pgm.Vector2(0, 0)
        scale = HeroCard_SCALE
        card_front = CardFront(img_path, scale, pos)
        card_front_hover = CardFront("Assets/PNGs/EmptySlotCard_OnHover.png", scale, pos)
        self.card_front_on_hover = card_front_hover
        self.card_front_normal = card_front
        Card.__init__(self, "Empty Slot Card", "Just enough to fit a card.", card_front, pos)

    def on_hover(self):
        offset = self.pos - self.card_front_on_hover.pos
        self.card_front_on_hover.move_ip(offset)
        self.card_front = self.card_front_on_hover

    def exit_hover(self):
        offset = self.pos - self.card_front_normal.pos
        self.card_front_normal.move_ip(offset)
        self.card_front = self.card_front_normal

    def move_card_here(self, card_):
        self.owner.move_card_to_slot(card_, self)


class InjusticeBatman(HeroCard):
    def __init__(self, game_, owner_card_group):
        # Base stats ----------------------------------------------------------
        hero_name = "Injustice Batman"
        hero_description = """
        "I'm Batman!": On Reveal - Power doubles after 3 rounds 
        """
        hero_cost = 2
        hero_power = 20
        hero_tags = ["Batman", "Tech"]
        position = (0, 0)
        img_path = "Assets/PNGs/HeroCard_Batman.png"

        HeroCard.__init__(self, hero_name, hero_description, img_path, position, hero_cost, hero_power, hero_tags, game_, owner_card_group)

        # Extra variables -----------------------------------------------------
        self.OnRevealEffectActivated = False
        self.round_count = 0

    # Functions -----------------------------------------------------------
    def im_batman(self):
        if self.OnRevealEffectActivated:
            self.round_count += 1
            if self.round_count > 3:
                self.OnRevealEffectActivated = False
                self.round_count = 0
                self.power *= 2

    def on_reveal(self):
        self.OnRevealEffectActivated = True

    def ongoing_update(self):
        self.im_batman()
        self.stat_texts.update(self.cost,self.power)
        print("Im batman")
        return True


class JL17Batman(HeroCard):
    def __init__(self, game_, owner_card_group):
        # Base stats ----------------------------------------------------------
        hero_name = "Injustice Batman"
        hero_description = """
        "I'm Batman!": On Reveal - Power doubles after 3 rounds 
        """
        hero_cost = 2
        hero_power = 20
        hero_tags = ["Batman", "Tech"]
        position = (0, 0)
        img_path = "Assets/PNGs/HeroCard_JL17Batman.png"

        HeroCard.__init__(self, hero_name, hero_description, img_path, position, hero_cost, hero_power, hero_tags, game_, owner_card_group)

        # Extra variables -----------------------------------------------------
        self.OnRevealEffectActivated = False
        self.round_count = 0

    # Functions -----------------------------------------------------------
    def on_reveal(self):
        return False

    def ongoing_update(self):
        return False


class JL17Flash(HeroCard):
    def __init__(self, game_, owner_card_group):
        # Base stats ----------------------------------------------------------
        hero_name = "Injustice Batman"
        hero_description = """
        "I'm Batman!": On Reveal - Power doubles after 3 rounds 
        """
        hero_cost = 2
        hero_power = 20
        hero_tags = ["Batman", "Tech"]
        position = (0, 0)
        img_path = "Assets/PNGs/HeroCard_JL17TheFlash.png"

        HeroCard.__init__(self, hero_name, hero_description, img_path, position, hero_cost, hero_power, hero_tags, game_, owner_card_group)

        # Extra variables -----------------------------------------------------
        self.OnRevealEffectActivated = False
        self.round_count = 0

    # Functions -----------------------------------------------------------
    def on_reveal(self):
        return False

    def ongoing_update(self):
        return False


class JL17WonderWoman(HeroCard):
    def __init__(self, game_, owner_card_group):
        # Base stats ----------------------------------------------------------
        hero_name = "Injustice Batman"
        hero_description = """
        "I'm Batman!": On Reveal - Power doubles after 3 rounds 
        """
        hero_cost = 2
        hero_power = 20
        hero_tags = ["Batman", "Tech"]
        position = (0, 0)
        img_path = "Assets/PNGs/HeroCard_JL17WonderWoman.png"

        HeroCard.__init__(self, hero_name, hero_description, img_path, position, hero_cost, hero_power, hero_tags, game_, owner_card_group)

        # Extra variables -----------------------------------------------------
        self.OnRevealEffectActivated = False
        self.round_count = 0

    # Functions -----------------------------------------------------------
    def on_reveal(self):
        return False

    def ongoing_update(self):
        return False


class JL17Cyborg(HeroCard):
    def __init__(self, game_, owner_card_group):
        # Base stats ----------------------------------------------------------
        hero_name = "Injustice Batman"
        hero_description = """
        "I'm Batman!": On Reveal - Power doubles after 3 rounds 
        """
        hero_cost = 2
        hero_power = 20
        hero_tags = ["Batman", "Tech"]
        position = (0, 0)
        img_path = "Assets/PNGs/HeroCard_JL17Cyborg.png"

        HeroCard.__init__(self, hero_name, hero_description, img_path, position, hero_cost, hero_power, hero_tags, game_, owner_card_group)

        # Extra variables -----------------------------------------------------
        self.OnRevealEffectActivated = False
        self.round_count = 0

    # Functions -----------------------------------------------------------
    def on_reveal(self):
        return False

    def ongoing_update(self):
        return False


class JL17Aquaman(HeroCard):
    def __init__(self, game_, owner_card_group):
        # Base stats ----------------------------------------------------------
        hero_name = "Injustice Batman"
        hero_description = """
        "I'm Batman!": On Reveal - Power doubles after 3 rounds 
        """
        hero_cost = 2
        hero_power = 20
        hero_tags = ["Batman", "Tech"]
        position = (0, 0)
        img_path = "Assets/PNGs/HeroCard_JL17Aquaman.png"

        HeroCard.__init__(self, hero_name, hero_description, img_path, position, hero_cost, hero_power, hero_tags, game_, owner_card_group)

        # Extra variables -----------------------------------------------------
        self.OnRevealEffectActivated = False
        self.round_count = 0

    # Functions -----------------------------------------------------------
    def on_reveal(self):
        return False

    def ongoing_update(self):
        return False


class JL17Superman(HeroCard):
    def __init__(self, game_, owner_card_group):
        # Base stats ----------------------------------------------------------
        hero_name = "Injustice Batman"
        hero_description = """
        "I'm Batman!": On Reveal - Power doubles after 3 rounds 
        """
        hero_cost = 2
        hero_power = 20
        hero_tags = ["Batman", "Tech"]
        position = (0, 0)
        img_path = "Assets/PNGs/HeroCard_JL17Superman.png"

        HeroCard.__init__(self, hero_name, hero_description, img_path, position, hero_cost, hero_power, hero_tags, game_, owner_card_group)

        # Extra variables -----------------------------------------------------
        self.OnRevealEffectActivated = False
        self.round_count = 0

    # Functions -----------------------------------------------------------
    def on_reveal(self):
        return False

    def ongoing_update(self):
        return False