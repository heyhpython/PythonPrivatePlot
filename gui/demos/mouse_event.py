from kivy.app import App
from kivy.uix.widget import Widget


class TouchInput(Widget):
    def on_touch_down(self, touch):
        # touch mouse motion event
        print(touch)

    def on_touch_move(self, touch):
        # touch mouse motion event
        print(touch)
    
    def on_touch_up(self, touch):
        # touch mouse motion event
        print(touch)
    
    
class Simple4(App):
    def build(self):
        return TouchInput()


if __name__ == "__main__":
    Simple4().run()
