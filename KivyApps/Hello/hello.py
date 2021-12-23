from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


class SayHello(App):
    # jelen példában az init-rész nem feltétlenül szükséges
    def __init__(self):
        super().__init__()
        self.window = None
        self.greeting = None
        self.user = None
        self.button = None

    def build(self):
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        # img
        self.window.add_widget(Image(source="hello2.png"))

        # label
        self.greeting = Label(
                        text="What's your name?",
                        font_size=18,
                        color="#00FFCE")
        self.window.add_widget(self.greeting)

        # txt input
        self.user = TextInput(
                    multiline=False,
                    padding_y=(20, 20),
                    size_hint=(1, 0.5))
        self.window.add_widget(self.user)

        # btn
        self.button = Button(
                    text="Greet!",
                    size_hint=(1, 0.5),
                    bold=True,
                    background_color="#00FFCE",
                    background_normal="")
        self.button.bind(on_press=self.callback)
        self.window.add_widget(self.button)

        return self.window

    def callback(self, inst):
        self.greeting.text = f"Hello {self.user.text} !"


if __name__ == "__main__":
    SayHello().run()
