from kivy.app import App 
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button 

class RexableApp(App):
    def build(self):
        layout = AnchorLayout(
            anchor_x='left', anchor_y='top')
        butn = Button(text='Test')
        layout.add_widget(butn)
        return layout

if __name__ == '__main__':

    RexableApp().run()