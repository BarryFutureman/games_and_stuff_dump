from card import *


class UnrevealedDestinyCard(UnrevealedCard):
    def __init__(self):
        # Base stats ----------------------------------------------------------
        hero_name = "Unrevealed Destiny Card"
        hero_description = """
                        Destiny is near.
                        """
        img_path = "Assets/PNGs/DestinyCard_Back.png"
        position = pgm.Vector2(0, 0)
        UnrevealedCard.__init__(self, hero_name, hero_description, img_path, position, DestinyCard_SCALE)