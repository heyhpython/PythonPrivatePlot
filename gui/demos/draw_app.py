from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Line

class DrawInput(Widget):
    def on_touch_down(self, touch):
        # touch mouse motion event
        print(touch)
        with self.canvas:
            touch.ud["line"]=Line(points=(touch.x, touch.y))

    def on_touch_move(self, touch):
        # touch mouse motion event
        print(touch)
        touch.ud['line'].points += (touch.x, touch.y)
    
    def on_touch_up(self, touch):
        # touch mouse motion event
        print(touch)
    
    
class Simple4(App):
    def build(self):
        return DrawInput()


if __name__ == "__main__":
    Simple4().run()
