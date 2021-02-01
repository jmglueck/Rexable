from kivy.app import App 
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button 
from kivy.lang import Builder
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.storage.jsonstore import JsonStore
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

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
        orientation: 'vertical'
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
        DietDropDown:
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
        Button:
            text: '=>'
<DietDropDown>:
    text: 'Diet'
            
<MainScreen>:
    name: 'main_screen'
    BoxLayout:
        orientation: 'vertical'
        RecipeSearchBar:
        RecommendationLayout:
        BoxLayout:
            orientation: 'horizontal'
            Button:
                text: 'Login'
                size_hint: (.5, .5)
                on_release: root.manager.current = 'login_screen'
            Button:
                text: 'Quit'
                size_hint: (.5, .5)
                on_press: app.stop()
<RecipeSearchBar>:
    hint_text: 'Search Recipes Here'
    size_hint: (1, 0.1)
<RecommendationLayout>:
    size_hint: (0.5, 0.5)
    height: 100 
    width: 100

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
        drop_down.bind(on_select=lambda instance, x: setattr(self, 'text', x))

class RecommendationLayout(GridLayout):
    pass

class RecipeSearchBar(TextInput):
    pass

class LoginScreen(Screen):
    pass

class SignUpScreen(Screen):
    pass

class MainScreen(Screen):
    pass

class RexableApp(App):
    def __init__(self):
        self.logged_in = False
        data_dir = getattr(self, 'user_data_dir')
        store = JsonStore(data_dir.join('app_storage.json'))
        user_login = ["", ""]


    def login(self):
        #this is just a preliminary password/username system; will add hashing and encryption later
        username = self.username_login.text
        password = self.username_password.text
        RexableApp.store.put('credentials', username = username, password = password)

    def build(self):
        username = ''
        password = ''
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main_screen'))
        sm.add_widget(LoginScreen(name='login_screen'))
        sm.add_widget(SignUpScreen(name='signup_screen'))

        try:
            RexableApp.store.get('credentials')['username']
        except KeyError:
            username = ""
        else:
            username = RexableApp.store.get('credentials')['username']
        
        try:
            RexableApp.store.get('credentials')['password']
        except KeyError:
            password = ""
        else:
            password = RexableApp.store.get('credentials')['password']

        self.user_login = [username, password]

        #again, just a preliminary login system, we check if password is "111" and username is "000", if it is we're logged in, if not we are back to log in page
        if self.user_login[0] == "000" and self.user_login[1] == "111":
            sm.manager.current = 'main_screen'
        else:
            sm.manager.current = 'login_screen'

        return sm

if __name__ == '__main__':
    RexableApp().run()