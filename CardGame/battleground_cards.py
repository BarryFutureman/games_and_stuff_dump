from card import *


class GothamCityBGC(BattlegroundCard):
    def __init__(self):
        # Base stats ----------------------------------------------------------
        battleground_name = "Unrevealed Destiny Card"
        battleground_description = """
                        When the darkness falls.
                        """
        img_path = "Assets/PNGs/DestinyCard_Back.png"
        position = pgm.Vector2(0, 0)
        BattlegroundCard.__init__(self, battleground_name, battleground_description, img_path, position)