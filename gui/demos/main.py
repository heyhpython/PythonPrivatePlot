from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Line
from kivy.lang import Builder

presentation = Builder.lo
    
class MainApp(App):
    def build(self):
        return DrawInput()


if __name__ == "__main__":
    MainApp().run()
