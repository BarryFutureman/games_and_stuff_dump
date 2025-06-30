from card import*
from pygame.locals import *


class InputManager:
    def __init__(self, game_):
        self.game_manager = game_
        self.user_player = game_.player1
        self.disabled = False

        self.draggable_item = None
        self.on_hover_item = None
        # Input
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_down = False

    def update(self, events):
        if self.disabled:
            return
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                self.on_click_down()
            elif event.type == MOUSEBUTTONUP:
                self.on_click_up()
            elif event.type == MOUSEMOTION:
                self.on_mouse_motion(event.rel)

    def on_click_down(self):
        self.mouse_down = True
        draggable_items = self.game_manager.get_clickable_cards()
        """ draggable_items.extend(self.game_manager.player1.get_clickable_cards())
        draggable_items.extend(self.game_manager.battleground_manager.get_all_movable_cards()) """
        self.draggable_item = self.cursor_to_item(draggable_items)

    def on_click_up(self):
        self.mouse_down = False
        if self.draggable_item:
            # If Hovering over an item ----------------------------
            if self.on_hover_item:
                self.user_player.place_card(self.draggable_item, self.on_hover_item)
                # self.on_hover_item.owner.move_card_to_slot(self.draggable_item, self.on_hover_item)
                self.on_hover_item.exit_hover()
            # -----------------------------------------------------
            self.draggable_item.on_release()
            self.draggable_item = None

    def cursor_to_item(self, items):
        for i in reversed(range(len(items))):
            item = items[i]
            if item.get_main_rect().collidepoint(self.mouse_pos):
                return item
        return None

    def on_mouse_motion(self, rel):
        self.mouse_pos = pygame.mouse.get_pos()

        self.on_cursor_hover()

        if self.mouse_down:
            self.drag(rel)

    def on_cursor_hover(self):
        if self.draggable_item:
            empty_slots = []
            empty_slots.extend(self.game_manager.battleground_manager.get_all_slot_cards(self.user_player))
            selected_slot = self.cursor_to_item(empty_slots)
            if selected_slot != self.on_hover_item:
                if selected_slot:
                    selected_slot.on_hover()
                if self.on_hover_item:
                    self.on_hover_item.exit_hover()
            self.on_hover_item = selected_slot

    def drag(self, offset):
        if self.draggable_item:
            self.draggable_item.on_drag(offset)

    def set_active(self, state):
        self.disabled = not state
