from kivy.app import App
from kivy.uix.floatlayout import FloatLayout

    
class Simple4(App):
    def build(self):
        return FloatLayout()


if __name__ == "__main__":
    Simple4().run()