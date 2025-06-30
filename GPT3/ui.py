import pygame
from mia_interface import *


class Notch:
    def __init__(self, owner):
        notch_height = 62
        pos = (0, (owner.height - notch_height) * owner.scale)

        self.width = owner.width * owner.scale
        self.height = notch_height * owner.scale
        self.owner = owner

        # Backdrop image
        self.image = pygame.image.load("Assets/PNGs/Notch.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class TextInput:
    def __init__(self, owner: MainWindow, font_size=15, text_color=(255, 255, 255), bg_color=(255, 255, 255)):
        pos = (0, (owner.height - 45) * owner.scale)

        self.width = owner.width * owner.scale
        self.height = 45 * owner.scale
        self.owner = owner

        self.text = ''

        # Backdrop image
        self.image = pygame.image.load("Assets/PNGs/Inputbar.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

        self.font = pygame.font.Font('Assets/Fonts/Roboto-Regular.ttf', font_size)
        self.font_size = font_size
        self.text_color = text_color
        self.max_text_length = int((self.width-50) / self.font.size(' ')[0]) - 1
        self.bg_color = bg_color
        self.active = False
        self.color = self.text_color if self.active else self.bg_color

        self.cursor_pos = 0
        self.cursor_visible = True
        self.cursor_timer = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.text_color if self.active else self.bg_color
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.on_send()
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_LEFT:
                    self.move_cursor(-1)
                else:
                    self.on_type(event)

    def on_send(self):
        self.owner.send_message(self.text)
        self.text = ''

    def move_cursor(self, amount):
        self.cursor_pos += amount
        if self.cursor_pos < 0:
            self.cursor_pos = len(self.text) + self.cursor_pos
        elif self.cursor_pos > len(self.text):
            self.cursor_pos = len(self.text)

    def on_type(self, event):
        char = ""
        if event.key == pygame.K_BACKSLASH:
            char = "\n"
            self.move_cursor(2)
        else:
            char = event.unicode
        self.text = self.text[:self.cursor_pos] + char + self.text[self.cursor_pos:]
        self.move_cursor(1)

    def update(self, dt):
        self.color = self.text_color if self.active else self.bg_color

        # update the cursor timer
        self.cursor_timer += dt
        if self.cursor_timer > 500:
            self.cursor_timer = 0
            self.cursor_visible = not self.cursor_visible

    def draw(self, screen):
        # pygame.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(self.image, self.rect)

        # Text
        display_text = self.text
        text_surface = self.font.render(display_text, True, self.text_color)
        text_width, text_height = text_surface.get_size()
        target_width = self.rect.width - 50 * self.owner.scale
        if text_width > target_width:
            cropped_text = ''
            total_width = 0
            for i in range(len(self.text)-1, 0, -1):
                char_width = self.font.size(self.text[i])[0]
                if total_width + char_width > target_width:
                    break
                cropped_text = self.text[i] + cropped_text
                total_width += char_width
            display_text = cropped_text
            text_surface = self.font.render(display_text, True, self.text_color)
        text_rect = text_surface.get_rect()
        text_rect.x = self.rect.x + 15 * self.owner.scale
        text_rect.y = self.rect.y + 12 * self.owner.scale
        screen.blit(text_surface, text_rect)

        # draw the cursor
        if self.active and self.cursor_visible:
            font_height = self.font.get_height()
            cursor_x = text_rect.x + self.font.render(display_text[:self.cursor_pos], True, self.text_color).get_width()
            cursor_y = text_rect.y
            pygame.draw.line(screen, self.text_color, (cursor_x, cursor_y),
                             (cursor_x, cursor_y + font_height - 2))


class TextBlock:
    def __init__(self, owner, text: str, font, pos: tuple[int, int]):
        self.owner = owner
        self.font = font
        text = self.text_auto_change_line(text)
        self.text = text
        self.pos = pos

        # Rect
        self.width = owner.width * owner.scale
        self.height = self.font.get_height() * (text.count("\n") + 1) + 5 * self.owner.scale
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)

        # Text Display
        self.text_color = (255, 255, 255)
        # self.text_surf = self.font.render(str(self.text), True, self.text_color)
        """
        self.text_rect = self.text_surf.get_rect()
        self.text_rect.center = self.rect.center
        self.text_rect.x = 10 * self.owner.scale
        """
        self.lines = text.split('\n')
        self.rendered_lines = []
        for line in self.lines:
            self.rendered_lines.append(self.font.render(line, True, self.text_color))

    def update_text(self, new_text):
        self.text = new_text
        self.lines = new_text.split('\n')
        self.rendered_lines = []
        for line in self.lines:
            self.rendered_lines.append(self.font.render(line, True, self.text_color))

    def set_position(self, pos):
        self.pos = pos
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def draw(self, screen):
        y = self.pos[1]
        for line in self.rendered_lines:
            screen.blit(line, (self.pos[0], y))
            y += line.get_height()

    def text_auto_change_line(self, text):
        lines = text.split('\n')
        new_lines = []
        target_width = self.owner.width * self.owner.scale
        for line in lines:
            line_render = self.font.render(line, True, (0, 0, 0))
            if line_render.get_width() <= target_width:
                new_lines.append(line)
                continue

            fitted_lines = []
            while line_render.get_width() > target_width:
                cropped_text = ''
                total_width = 0
                for i in range(len(line)):
                    char_width = self.font.size(line[i])[0]
                    if total_width + char_width > target_width:
                        # Get the last " " in line, so we can put the word into the next line
                        new_line = line[i:]
                        curr_line = line[:i+1]
                        for c in range(i, 0, -1):
                            if curr_line[c] == " ":
                                new_line = line[c:]
                                cropped_text = cropped_text[:c]
                                break
                        line = new_line.lstrip()
                        break
                    cropped_text += line[i]
                    total_width += char_width
                fitted_lines.append(cropped_text)
                line_render = self.font.render(line, True, (0, 0, 0))
            fitted_lines.append(line)
            new_lines.extend(fitted_lines)

        return "\n".join(new_lines)


class RightHandTextBlock(TextBlock):
    # def __init__(self, owner, text: str, font, pos: tuple[int, int]):
        # TextBlock.__init__(self, owner, text, font, pos)

    def draw(self, screen):
        y = self.pos[1]
        for line in self.rendered_lines:
            x = self.owner.width * self.owner.scale - line.get_width()
            screen.blit(line, (x, y))
            y += line.get_height()


class TextBlocksManager:
    text_blocks: list[TextBlock]

    def __init__(self, owner: MainWindow):
        self.owner = owner
        self.text_blocks = []
        self.bottom = (owner.height - 62) * owner.scale
        self.top = 0
        self.total_height = self.bottom
        self.font = pygame.font.Font('Assets/Fonts/Roboto-Regular.ttf', 16)

    def draw(self, screen):
        for block in self.text_blocks:
            block.draw(screen)

    def push(self, text_block: TextBlock):
        self.text_blocks.append(text_block)

    def add_text_block(self, text, right_hand_side=False):
        if not text:
            return

        new_text_block = None
        if right_hand_side:
            new_text_block = RightHandTextBlock(self.owner, text, self.font, (0, self.total_height))
        else:
            new_text_block = TextBlock(self.owner, text, self.font, (0, self.total_height))
        self.total_height -= new_text_block.height
        new_text_block.set_position((0, self.total_height))
        self.push(new_text_block)

    def add_text_block_right_hand_side(self, text):
        if not text:
            return
        new_text_block = RightHandTextBlock(self.owner, text, self.font, (0, self.total_height))
        self.total_height -= new_text_block.height
        self.push(new_text_block)
