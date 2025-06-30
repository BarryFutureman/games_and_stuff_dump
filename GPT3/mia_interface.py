import pygame
import win32api
import win32con
import win32gui
from pygame.locals import *
from ctypes import windll, Structure, c_long, byref

import ui
import mia_chat


fuchsia = (65, 65, 65)  # Transparency color


class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]


def query_mouse_pos():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return pt.x, pt.y


class MainWindow:
    def __init__(self):
        self.width = 500
        self.height = 1000
        self.scale = 0.7
        self.screen = pygame.display.set_mode((self.width * self.scale, self.height * self.scale), pygame.NOFRAME)

        self.mouse_down = False
        self.mouse_down_pos = query_mouse_pos()
        self.can_drag = False

        hwnd = pygame.display.get_wm_info()['window']
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                               win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
        win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)
        # win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0, 0, 0), 255, win32con.LWA_ALPHA)

        # set up the text input
        self.input_box = ui.TextInput(self, font_size=14)
        self.notch = ui.Notch(self)
        self.text_blocks_manager = ui.TextBlocksManager(self)

        # Set up Mia
        self.mia = mia_chat.Mia()

    def update(self, dt):
        self.input_box.update(dt)
        self.handle_dragging()

    def handle_event(self, event):
        self.input_box.handle_event(event)

        if event.type == MOUSEMOTION:
            self.on_mouse_motion(event.rel)

        elif event.type == MOUSEBUTTONDOWN:
            self.on_mouse_down()

        elif event.type == MOUSEBUTTONUP:
            self.on_mouse_up()

    def draw(self):
        self.notch.draw(self.screen)
        self.input_box.draw(self.screen)
        self.text_blocks_manager.draw(self.screen)

    def on_mouse_motion(self, rel):
        pass

    def on_mouse_down(self):
        mouse_pos = pygame.mouse.get_pos()
        self.mouse_down = True
        self.mouse_down_pos = mouse_pos
        if mouse_pos[1] > (self.height-45) * self.scale:
            self.can_drag = False
        else:
            self.can_drag = True

    def on_mouse_up(self):
        self.mouse_down = False

    def handle_dragging(self):
        if self.mouse_down and self.can_drag:
            hwnd = pygame.display.get_wm_info()['window']
            x, y = query_mouse_pos()
            windll.user32.SetWindowPos(hwnd, 0,
                                       int(x - self.mouse_down_pos[0]), int(y - self.mouse_down_pos[1]),
                                       0, 0, 0x0001)

    def send_message(self, text):
        self.text_blocks_manager.add_text_block(text, right_hand_side=True)
        print(text)
        response = self.mia.request_response(text)
        print(response)
        self.text_blocks_manager.add_text_block(response)
