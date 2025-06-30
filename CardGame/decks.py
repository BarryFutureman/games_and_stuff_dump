from hero_cards import*


class DeckPreset:
    def __init__(self):
        self.cards = []


class Preset1(DeckPreset):
    def __init__(self, _game, _deck):
        DeckPreset.__init__(self)
        self.cards.append(InjusticeBatman(_game, _deck))
        self.cards.append(JL17Batman(_game, _deck))
        self.cards.append(JL17Flash(_game, _deck))
        self.cards.append(JL17WonderWoman(_game, _deck))
        self.cards.append(JL17Cyborg(_game, _deck))
        self.cards.append(JL17Aquaman(_game, _deck))
        self.cards.append(JL17Superman(_game, _deck))






