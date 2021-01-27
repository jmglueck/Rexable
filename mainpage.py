from kivy.app import App 
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button 
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_string("""
<MainScreen>:
    AnchorLayout:
        anchor_x: 'right'
        anchor_y: 'top'
        Button:
            text: 'Login'
            size_hint: (.5, .5)
    AnchorLayout:
        anchor_x: 'left'
        anchor_y: 'top'
        Button:
            text: 'Quit'
            size_hint: (.5, .5)
            on_press: app.stop()
""")

class MainScreen(Screen):
    pass


class RexableApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main_screen'))
        return sm

if __name__ == '__main__':

    RexableApp().run()