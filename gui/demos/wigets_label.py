from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
import logging
logger = logging.getLogger(__name__)

class LoginScreen(GridLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        # two cols for label and input
        self.cols = 2
        # username label
        self.add_widget(Label(text="Username:"))
        # username input 
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)

        self.add_widget(Label(text="Password:"))
        self.password = TextInput(multiline=False, password=True)
        self.add_widget(self.password)

        self.add_widget(Label(text="two factor auth:"))
        self.tfa = TextInput(multiline=False)
        self.add_widget(self.tfa)

class Simple(App):
    def build(self):
        return LoginScreen()


if __name__ == "__main__":
    Simple().run()
