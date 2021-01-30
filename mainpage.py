from kivy.app import App 
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button 
from kivy.lang import Builder
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput

Builder.load_string("""
<LoginScreen>:
    name: 'login_screen'
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'top'
        BoxLayout:
            orientation: 'vertical'
            size_hint: (0.9, 0.7)
            Label:
                text: 'Username'
                halign: 'center'
                text_size: (75, 50)
                size_hint: (.2, .2)
            TextInput:
                multiline: False
                halign: 'center'
                font_size: '12sp'
                height: 30
                size_hint: (.2, None)
            Label:
                text: 'Password'
                halign: 'center'
                text_size: (75, 50)
                size_hint: (.2, .2)
            TextInput:
                multiline: False
                halign: 'center'
                font_size: '12sp'
                height: 30
                size_hint: (.2, None)
                password_mask: 'True'
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'center'
        size_hint: (0.7, 0.3)
        BoxLayout:
            padding: [15]
            orientation: 'horizontal'
            Button:
                text: 'Login'
            Button:
                text: 'Sign Up'
                on_release: root.manager.current = 'signup_screen'

<SignUpScreen>:
    name: 'signup_screen'
    BoxLayout:
        Label:
            text: 'Username'
        TextInput:
            multiline: False
            font_size: '12sp'
            height: 30
            size_hint: (.2, None)
        Label:
            text: 'Password'
        TextInput:
            multiline: False
            font_size: '12sp'
            height: 30
            size_hint: (.2, None)
        Label:
            text: 'Choose your diet'
        <DietDropDown>:
            text: 'Diet'
        Label: 
            text: 'List any allergies (separated by comma, such as "Peanuts,Shellfish")'
        TextInput:
            multiline: False
            font_size: '12sp'
            height: 30
            size_hint: (.2, None)
        Label: 
            text: 'How many hours in a day do you have to cook?'
        TextInput:
            multiline: False
            font_size: '12sp'
            height: 30
            size_hint: (.2, None)
            
<MainScreen>:
    name: 'main_screen'
    AnchorLayout:
        anchor_x: 'right'
        anchor_y: 'top'
        Button:
            text: 'Login'
            size_hint: (.5, .5)
            on_release: root.manager.current = 'login_screen'
    AnchorLayout:
        anchor_x: 'left'
        anchor_y: 'top'
        Button:
            text: 'Quit'
            size_hint: (.5, .5)
            on_press: app.stop()
        

""")

class DietDropDown(Button):
    def diet_dropdown(self):
        drop_down = DropDown()
        for i in ['kosher', 'halal', 'keto', 'vegetarian', 'vegan', 'low-carb', 'low-fat', 'none']:
            diet_button = Button(text=i, size_hint_y=None, height =35)
            diet_button.bind(on_release=lambda diet_button: drop_down.select(diet_button.text))
            drop_down.add_widget(diet_button)
        #main_button = Button(text='Diet', size_hint=(None, None), height=40)
        #main_button.bind(on_release=drop_down.open)
        self.bind(on_release=drop_down.open)
        drop_down.bind(on_select=lambda instance, x: setattr(main_button, 'text', x))

class LoginScreen(Screen):
    pass

class SignUpScreen(Screen):
    pass

class MainScreen(Screen):
    pass

class RexableApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main_screen'))
        sm.add_widget(LoginScreen(name='login_screen'))
        sm.add_widget(SignUpScreen(name='signup_screen'))
        return sm

if __name__ == '__main__':

    RexableApp().run()