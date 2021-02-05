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
                on_text: root.get_username(self.text)
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
                on_text: root.get_password(self.text)
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'center'
        size_hint: (0.7, 0.3)
        BoxLayout:
            padding: [15]
            orientation: 'horizontal'
            Button:
                text: 'Login'
                on_release: root.login()
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
            on_release: self.diet_dropdown()
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

<SettingScreen>:
    name: 'setting_screen'
    BoxLayout:
        orientation: 'vertical'
        Button:
            text: 'Profile'
            size_hint: (.5, .5)
            on_release: root.manager.current = 'profile_screen'
        Button:
            text: 'Recommendation Preference'
            size_hint: (.5, .5)
            on_release: root.manager.current = 'recommendation_preference_screen'
        Button:
            text: 'About'
            size_hint: (.5, .5)
            on_release: root.manager.current = 'about_screen'
        Button:
            text: 'Back'
            size_hint: (.5, .5)
            on_release: root.manager.current = 'main_screen'
            
<ProfileScreen>:
    name: 'profile_screen'
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'You can reset your username and password'
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
        Button:
            text: 'Back'
            size_hint: (.5, .5)
            on_release: root.manager.current = 'setting_screen'
    
<RecommendationPreferenceScreen>:
    name: 'recommendation_preference_screen'
    BoxLayout:
        orientation: 'vertical'
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
            text: 'Back'
            size_hint: (.5, .5)
            on_release: root.manager.current = 'setting_screen'
    
<AboutScreen>:
    name: 'about_screen'
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Rexable'
        Label: 
            text: 'Develop by UCI CS 125 Group 4'
        Label:
            text: 'Winter Quarter 2021'
        Button:
            text: 'Back'
            size_hint: (.5, .5)
            on_release: root.manager.current = 'setting_screen'
                                  
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
                text: 'Setting'
                size_hint: (.5, .5)
                on_release: root.manager.current = 'setting_screen'
            Button:
                text: 'Quit'
                size_hint: (.5, .5)
                on_press: app.stop()
            Button:
                text: 'Logout'
                size_hint: (.5, .5)
                on_press: root.logout()
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
        drop_down = DropDown(size_hint_y=0.5, height=100)
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

class SignUpScreen(Screen):
    pass

class SettingScreen(Screen):
    pass

class ProfileScreen(Screen):
    pass

class RecommendationPreferenceScreen(Screen):
    pass

class AboutScreen(Screen):
    pass


class RexableApp(App):
    def __init__(self):
        App.__init__(self)
        self.logged_in = False
        self._app_name = 'rexable_app'
        data_dir = getattr(self, 'user_data_dir')
        #store = JsonStore(data_dir.join('app_storage.json'))
        RexableApp.store = JsonStore('app_storage.json')
        user_login = ["", ""]
        self.sm = ScreenManager()

    def login(self):
        #this is just a preliminary password/username system; will add hashing and encryption later
        username = self.username_login.text
        password = self.username_password.text
        RexableApp.store.put('credentials', username = username, password = password)
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
            self.sm.current = 'main_screen'
        else:
            self.sm.current = 'login_screen'

    def build(self):
        username = ''
        password = ''
        self.sm.add_widget(MainScreen(name='main_screen'))
        self.sm.add_widget(LoginScreen(name='login_screen'))
        self.sm.add_widget(SignUpScreen(name='signup_screen'))
        self.sm.add_widget(SettingScreen(name='setting_screen'))
        self.sm.add_widget(ProfileScreen(name='profile_screen'))
        self.sm.add_widget(RecommendationPreferenceScreen(name='recommendation_preference_screen'))
        self.sm.add_widget(AboutScreen(name='about_screen'))

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
            self.sm.current = 'main_screen'
        else:
            self.sm.current = 'login_screen'

        return self.sm

class LoginScreen(Screen):
    def get_username(self, username):
        self.username = username
    def get_password(self, password):
        self.password = password

    def login(self):
        #this is just a preliminary password/username system; will add hashing and encryption later
        RexableApp.store.put('credentials', username = self.username, password = self.password)

        #again, just a preliminary login system, we check if password is "111" and username is "000", if it is we're logged in, if not we are back to log in page
        if self.username == "000" and self.password == "111":
            self.parent.current = 'main_screen'
        else:
            self.parent.current = 'login_screen'

class MainScreen(Screen):
    def logout(self):
        RexableApp.store.put('credentials', username = "", password = "")
        RexableApp.stop()

if __name__ == '__main__':
    RexableApp().run()
