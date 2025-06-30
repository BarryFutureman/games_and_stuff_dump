from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import random
from kivy.graphics import Color, Rectangle

class ChatApp(App):

    def build(self):
        # Create a BoxLayout for the main chat interface
        main_layout = BoxLayout(orientation='vertical')

        title = Button(text='GPT Swift', size_hint_y=None, height=50,
                       background_color=[.12, .12, .12, 1], background_normal="", color=(1, 1, 1, 1),
                       font_size=20)

        # Create a GridLayout to hold the widgets
        self.grid_layout = GridLayout(cols=1, spacing=0, size_hint_y=None)

        # Set the height of the GridLayout to allow scrolling
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))

        # Create a ScrollView to contain the chat messages
        self.scroll_view = ScrollView()
        self.scroll_view.add_widget(self.grid_layout)

        # Add the ScrollView to the main BoxLayout
        main_layout.add_widget(title)
        main_layout.add_widget(self.scroll_view)

        # Create a TextInput for entering chat messages
        self.chat_input = TextInput(size_hint_y=None, height=50)

        # Add a Button for sending messages
        send_button = Button(text='Send', size_hint_y=None, height=50,
                             background_color=[.12, .12, .12, 1],
                             color=(1, 1, 1))
        send_button.bind(on_press=self.send_message)

        # Add the TextInput and Button to the main BoxLayout
        main_layout.add_widget(self.chat_input)
        main_layout.add_widget(send_button)

        return main_layout

    def send_message(self, instance):
        # Get the text from the chat input and clear it
        message = self.chat_input.text
        # Add multiple widgets to the GridLayout
        self.chat_input.text = ''

        message += " : " + str(message.count('\n') + 1)
        h = 10 + 20 * (message.count('\n')+1)
        text_block = Button(text='Send', size_hint_y=None, height=h,
                            background_color=[random.uniform(0.15, 0.165), random.uniform(0.16, 0.165), 0.2, 1],
                            background_normal="")
        text_block.text = message
        self.grid_layout.add_widget(text_block)


if __name__ == '__main__':
    ChatApp().run()
