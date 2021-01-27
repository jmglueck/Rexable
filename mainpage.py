from kivy.app import App 
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button 
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_string("""
<MainScreen>:
    AnchorLayout:
        Button:
            text: 'Login'
        Button:
            text: 'Quit'
            on_press: app.stop()
""")

class MainScreen(Screen):
    pass


class RexableApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(AnchorLayout(anchor_x='left', anchor_y='top'))
        return sm

if __name__ == '__main__':

    RexableApp().run()