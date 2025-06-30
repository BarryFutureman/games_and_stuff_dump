from card import*
import hero_cards as hc
import destiny_cards as dc
import input
from pygame.locals import *
import debug
import decks

import random

# Global variables
ScreenWIDTH, ScreenHEIGHT = 1920 * 4/5, 1080 * 4/5


class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return not self.items

    def enqueue(self, item):
        self.items.append(item)

    def pop(self):
        return self.pop()

    def dequeue(self):
        return self.items.pop(0)


class GameManager:
    def __init__(self, screen_):
        self.screen = screen_
        self.debug = debug.Debug()
        self.player1 = UserPlayer(screen_, "Player 1", game_=self)
        self.player2 = AIPlayer(screen_, "Player 2", game_=self)
        # We need the players created to init these two
        self.input_manager = input.InputManager(self)
        self.battleground_manager = BattlegroundManager(screen_, self)

        self.round_display = RoundDisplay((ScreenWIDTH/2, ScreenHEIGHT/8))
        self.round_step_progress = 0
        self.curr_round_count = 0

    #def on_cursor_hover(self):
    #   slot_cards = self.battleground_manager.get_all_slot_cards()
    #   for slot in slot_cards:
    #       slot.on_hover()

    def update(self, events):
        self.input_manager.update(events)

        # Get the next step
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == K_RETURN:
                    self.next_step()

    def draw(self):
        self.battleground_manager.draw()
        self.player1.draw()
        # self.player2.draw()
        self.debug.draw(self.screen)
        self.round_display.draw(self.screen)

    def next_step(self):
        if self.round_step_progress == 0:
            self.player1.play_round(self)
            self.player2.play_round(self)
            self.input_manager.set_active(True)
            self.round_step_progress += 1
            self.debug.log("Round begin, putting down cards.")
            self.curr_round_count += 1
            self.player1.set_energy(self.curr_round_count)
            self.player2.set_energy(self.curr_round_count)
            self.round_display.set_text(f"Round {self.curr_round_count}\nRemaining Energy: {self.player1.curr_energy}")
            self.battleground_manager.play_draw_cards_from_deck(1)
        elif self.round_step_progress == 1:
            self.input_manager.set_active(False)
            self.battleground_manager.deploy_landing_queue()
            self.round_step_progress += 1
            self.debug.log("All cards ready, initializing.")
        elif self.round_step_progress == 2:
            if not self.battleground_manager.reveal_card():
                #  self.battleground_manager.revealing_queue.is_empty():
                self.battleground_manager.initiate_ongoing_update_queue()
                self.round_step_progress += 1
                self.debug.log("All cards revealed.")
            self.debug.log("Reveal card.")
        elif self.round_step_progress >= 3:
            if not self.battleground_manager.update_ongoing_card():
                self.round_step_progress = 0
                self.debug.log("All on going effects updated.")
            self.debug.log("On going effect update.")

        # print(self.round_step_progress)
        self.battleground_manager.update_total_power_displays()

    def get_clickable_cards(self):
        c_cards = []
        c_cards.extend(self.battleground_manager.get_all_movable_cards())
        c_cards.extend(self.player1.get_clickable_cards())
        return c_cards


class BattlegroundManager:
    def __init__(self, screen_, game_):
        self.screen = screen_

        # register_players
        self.players = [game_.player1, game_.player2]

        self.lanes = []
        self.destiny_cards = []
        # Initialize anchors
        anchor_h = ScreenHEIGHT*13/27
        self.anchors = [(ScreenWIDTH*9/80, anchor_h), (ScreenWIDTH*1/4, anchor_h),
                        (ScreenWIDTH*3/4, anchor_h), (ScreenWIDTH*71/80, anchor_h)]
        # Initialize unrevealed cards
        self.unrevealed_destiny_cards = []
        for i in range(4):
            # Set up destiny cards
            new_udc = dc.UnrevealedDestinyCard()
            self.unrevealed_destiny_cards.append(new_udc)
            new_udc.set_anchor_position(self.anchors[i])
            # Set up sub lanes
            self.lanes.append(Lane(screen_, self.anchors[i][0], 2))
        # Set up main lane
        self.lanes.append(Lane(screen_, ScreenWIDTH/2, 5))

        # Gameplay
        self.revealing_queue = Queue()
        self.update_queue = Queue()

    def draw(self):
        for c in self.unrevealed_destiny_cards:
            c.draw(self.screen)

        for lane in self.lanes:
            lane.draw(self.screen)

    def get_all_slot_cards(self, player_):
        # player_ = self.players[0]
        all_slot_cards = []
        for lane in self.lanes:
            for c in self.get_cards_of_lane_by_player(lane, player_):
                if isinstance(c, hc.EmptySlotCard):
                    all_slot_cards.append(c)
        return all_slot_cards

    def get_all_movable_cards(self):
        player_ = self.players[0]
        all_mhc = []
        for lane in self.lanes:
            for c in self.get_cards_of_lane_by_player(lane, player_):
                if isinstance(c, HeroCard):
                    all_mhc.append(c)
        return all_mhc

    def get_cards_of_lane_by_player(self, lane, player_):
        return lane.slot_groups[self.players.index(player_)].cards

    def get_available_slots(self, player_):
        i = self.players.index(player_)
        return

    def deploy_landing_queue(self):
        def process():
            cards = landing_queue.dequeue()
            hero_card = cards[0]
            slot_card = cards[1]
            unrevealed_hero_card = hc.UnrevealedHeroCard(slot_card.owner, hero_card)

            # Remove hero card from hand and place unrevealed version of it
            hero_card.owner.remove_card(hero_card)
            slot_card.owner.swap_cards(slot_card, unrevealed_hero_card)
            # Equeue
            self.revealing_queue.enqueue(unrevealed_hero_card)
        # Deploy landing queue------------------------------------------------------
        # Player 1
        landing_queue = self.players[0].landing_queue
        while not landing_queue.is_empty():
            process()
        # Player 2
        landing_queue = self.players[1].landing_queue
        while not landing_queue.is_empty():
            process()
        # Note: Apparently, tuple being immutable copies the slot object, making it not exist in the "owner"

    def reveal_card(self):
        if not self.revealing_queue.is_empty():
            card = self.revealing_queue.dequeue()
            card.owner.swap_cards(card, card.hero_card)
            card.hero_card.on_reveal()
            return True
        return False

    def update_total_power_displays(self):
        for lane in self.lanes:
            display = lane.total_power_displays[0]
            power_sum = lane.slot_groups[0].calculate_power_sum()
            display.update(power_sum)
            display = lane.total_power_displays[1]
            power_sum = lane.slot_groups[1].calculate_power_sum()
            display.update(power_sum)

    def initiate_ongoing_update_queue(self):
        cards = []
        for lane in self.lanes:
            for c in self.get_cards_of_lane_by_player(lane, self.players[1]):
                if isinstance(c, HeroCard):
                    cards.append(c)
        for c in cards:
            self.update_queue.enqueue(c)

    def update_ongoing_card(self):
        while not self.update_queue.is_empty():
            card = self.update_queue.dequeue()
            if card.ongoing_update():
                return True
        return False

    def play_draw_cards_from_deck(self, amount: int):
        for p in self.players:
            for i in range(amount):
                new_card = p.get_card_from_deck()
                p.hand.add_card(new_card)


class Lane:
    def __init__(self, screen_, pos_x, num_of_slots):
        slot_group_lower = SlotGroup(screen_, (pos_x, ScreenHEIGHT*17/24), num_of_slots)
        slot_group_upper = SlotGroup(screen_, (pos_x, ScreenHEIGHT*1/4), num_of_slots)
        self.slot_groups = [slot_group_lower, slot_group_upper]

        self.total_power_displays = [TotalPowerNumberDisplay((pos_x, ScreenHEIGHT*15/25)),
                                     TotalPowerNumberDisplay((pos_x, ScreenHEIGHT*9/25))]

    def draw(self, screen_):
        for display in self.total_power_displays:
            display.draw(screen_)
        self.slot_groups[0].draw()
        self.slot_groups[1].draw()


class CardGroup:
    cards: list[Card]

    def __init__(self, screen_, position):
        self.screen = screen_
        self.cards = []
        self.anchors = []
        self.pos = pgm.Vector2(position)

    def draw(self):
        for c in self.cards:
            c.draw(self.screen)

    def add_card(self, new_card):
        new_card.owner = self
        self.cards.append(new_card)
        # Recalculate and apply new anchor points
        self.recalculate_anchors()
        for i in range(len(self.cards)):
            self.cards[i].set_anchor_position(self.anchors[i].copy())

    def remove_card(self, card):
        for i in range(len(self.cards)):
            if self.cards[i] == card:
                self.cards.pop(i)
                self.anchors.pop(i)
                break
        self.recalculate_anchors()

    def recalculate_anchors(self):
        default_height = self.pos.y
        length = len(self.cards)
        gap = 2
        half_card = DIMENSION[0] * HeroCard_SCALE / 2
        push_start_x = self.pos.x - (gap + half_card*2) * (length/2) + half_card# - length % 2 * (half_card + gap)
        new_anchors = []
        for i in range(length):
            new_anchors.append(pgm.Vector2(push_start_x + i * (gap + half_card * 2), default_height))
        self.anchors = new_anchors

        for i in range(len(new_anchors)):
            self.cards[i].set_anchor_position(new_anchors[i].copy())

    def recalculate_anchors_old(self):
        default_height = self.pos.y
        length = len(self.anchors)
        if length == 0:
            self.anchors.append(pgm.Vector2(self.pos.x, default_height))
        else:
            gap = 2
            push_amount = DIMENSION[0] * HeroCard_SCALE / 2 + gap
            for i in range(length):
                self.anchors[i].x -= push_amount
            r_mst_card = self.anchors[length - 1]
            new_anchor = pgm.Vector2(r_mst_card.x + push_amount * 2, default_height)
            self.anchors.append(new_anchor)

    def swap_cards(self, old_card, new_card):
        i = self.cards.index(old_card)
        new_card.set_anchor_position(old_card.anchor)
        new_card.owner = self
        self.cards[i] = new_card

    def transfer_card(self, card, new_card_group):
        self.remove_card(card)
        new_card_group.add_card(card)

    def calculate_power_sum(self):
        power_sum = 0
        for card in self.cards:
            if isinstance(card, HeroCard):
                power_sum += card.power
        return power_sum


class SlotGroup(CardGroup):
    def __init__(self, screen_, position, n):
        self.num_slots = n
        CardGroup.__init__(self, screen_, position)
        # Add empty slots:
        for i in range(self.num_slots):
            self.add_card(hc.EmptySlotCard(owner_=self))

    def try_set_slot(self, hero_card, slot):
        for i in range(len(self.cards)):
            if self.cards[i] == slot:
                # Set slot to new card
                self.cards[i] = hero_card
                hero_card.on_drop_to_slot(self.anchors[i])
                break

    def remove_card(self, card):
        i = self.cards.index(card)
        self.cards[i] = hc.EmptySlotCard(self)
        self.cards[i].set_anchor_position(card.anchor)

    def move_card_to_slot(self, hero_card, slot):
        hero_card.owner.remove_card(hero_card)
        i = self.cards.index(slot)
        # Set hero_card to new owner
        hero_card.set_anchor_position(slot.anchor)
        hero_card.owner = self
        # --------------------------
        self.cards[i] = hero_card

    def setup_unrevealed_card(self, hero_card):
        unrevealed_hero_card = hc.UnrevealedHeroCard(hero_card)
        i = self.cards.index(hero_card)
        unrevealed_hero_card.set_anchor_position(hero_card.anchor)
        self.cards[i] = unrevealed_hero_card
        return unrevealed_hero_card


class Deck:
    def __init__(self, preset: decks.DeckPreset):
        self.cards = []
        for c in preset.cards:
            self.cards.append(c)

    def random_get_card(self):
        length = len(self.cards)
        if length > 0:
            index = random.randint(0, length - 1)
            card = self.cards[index]
            self.cards.pop(index)
            return card


class Player:
    deck: Deck
    hand: CardGroup

    def __init__(self, screen_, p_id, game_, pos_):
        self.screen = screen_

        self.player_id = p_id
        self.deck = Deck(decks.Preset1(game_, None))
        self.hand = CardGroup(screen_, pos_)
        self.landing_queue = Queue()
        self.allow_inputs = False
        self.curr_energy = 0

        # Initialize Hand
        for i in range(3):
            new_card = self.get_card_from_deck()
            if new_card:
                self.hand.add_card(new_card)

    def draw(self):
        self.hand.draw()

    def get_clickable_cards(self):
        cards = []
        for c in self.hand.cards:
            if c.cost <= self.curr_energy:
                cards.append(c)
        return cards

    def get_card_from_deck(self):
        return self.deck.random_get_card()

    def play_round(self, game_):
        pass

    def place_card(self, hero_card, slot):
        self.landing_queue.enqueue((hero_card, slot))
        hero_card.set_anchor_position(slot.pos)
        self.curr_energy -= hero_card.cost
        #slot.move_card_here(hero_card)

    def set_energy(self, amount: int):
        self.curr_energy = amount


class UserPlayer(Player):
    def __init__(self, screen_, p_id, game_):
        pos = (ScreenWIDTH / 2, ScreenHEIGHT - 100)
        Player.__init__(self, screen_, p_id, game_, pos)


class AIPlayer(Player):
    def __init__(self, screen_, p_id, game_):
        pos = (ScreenWIDTH / 2, 50)
        Player.__init__(self, screen_, p_id, game_, pos)

    def play_round(self, game_):
        slot_cards = game_.battleground_manager.get_all_slot_cards(self)
        if self.hand.cards and slot_cards:
            self.landing_queue.enqueue((self.hand.cards[0], slot_cards[0]))
        #self.place_card(self.hand.cards[0], slot_cards[0])

    #def draw(self):
    #   pass


