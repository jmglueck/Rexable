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
from pymongo import MongoClient, errors
from search_basic import search 

try:
    # try to instantiate a client instance
    client = MongoClient(
        host = [ "localhost:" + "27017" ],
        serverSelectionTimeoutMS = 3000 # 3 second timeout
    )
    db = client["rexableDatabase"]
    userCollect = db["users"]
    recipeCollect = db["recipes"]

    # print the version of MongoDB server if connection successful
    print ("server version:", client.server_info()["version"])

except errors.ServerSelectionTimeoutError as err:
    # set the client and db names to 'None' and [] if exception
    client = None
    db = None
    userCollect = None
    recipeCollect = None
    
    # catch pymongo.errors.ServerSelectionTimeoutError
    print ("pymongo ERROR:", err)

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
            on_text: root.get_username(self.text)
        Label:
            text: 'Password'
        TextInput:
            multiline: False
            font_size: '12sp'
            height: 30
            size_hint: (.2, None)
            on_text: root.get_password(self.text)
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
            on_text: root.get_allergies(self.text)
        Label: 
            text: 'How many hours in a day do you have to cook?'
        TextInput:
            multiline: False
            font_size: '12sp'
            height: 30
            size_hint: (.2, None)
            on_text: root.get_cookingtime(self.text)
        Button:
            text: '=>'
            on_release: root.enter_info()
<DietDropDown>:
    text: 'Diet'

<SettingsScreen>:
    name: 'settings_screen'
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
            on_release: root.manager.current = 'settings_screen'
    
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
            on_release: root.manager.current = 'settings_screen'
    
<AboutScreen>:
    name: 'about_screen'
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Rexable'
        Label: 
            text: 'Developed by UCI CS 125 Group 4'
        Label:
            text: 'Winter Quarter 2021'
        Button:
            text: 'Back'
            size_hint: (.5, .5)
            on_release: root.manager.current = 'settings_screen'



<RecipeSearchBar>:
    name: 'recipe_search_bar'
    BoxLayout:
        orientation: 'horizontal'
        TextInput:
            
            multiline: False
            font_size: '18sp'
            height: 40
            width: 80
            size_hint: (8, None)
            on_text: root.get_query(self.text)
        Button:
            text: 'Search'
            size_hint: (0.6,0.18)
            on_release: root.start_search()

            
                                  
<MainScreen>:
    name: 'main_screen'
    BoxLayout:
        orientation: 'vertical'
        RecipeSearchBar:
        RecommendationLayout:
        BoxLayout:
            orientation: 'horizontal'
            Button:
                text: 'Settings'
                size_hint: (.5, .5)
                on_release: root.manager.current = 'settings_screen'

                
            Button:
                text: 'Quit'
                size_hint: (.5, .5)
                on_press: app.stop()
            Button:
                text: 'Logout'
                size_hint: (.5, .5)
                on_press: root.logout()




    
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

class RecipeSearchBar(Screen):

    def get_query(self,query):

        self.query = query
##        print(query)
        
    def start_search(self):
##        print(self.query)
        result = search(self.query)
        self.result = result

##        print(result)
        
        if recipeCollect != None:
            recipeCollect.insert_many(result)



class SignUpScreen(Screen):
    def __init__(self):
        Screen.__init__(self)
        self.name='signup_screen'
        self.allergies = []
        self.cooking_time = -1
        self.username = ""
        self.password = ""

    def get_username(self, the_text):
        self.username = the_text

    def get_password(self, the_text):
        #later add message if it's not at least 8 characters and/or doesn't contain a lowercase letter, uppercase letter, and number
        self.password = the_text

    def get_allergies(self, the_text):
        temp_list = the_text.split()
        #now removing whitespace
        for i in temp_list:
            self.allergies.append(i.replace(" ", ""))

    def get_cookingtime(self, the_text):
        #later add exception handling
        try:
            self.cooking_time = int(the_text)
        except Exception:
            self.cooking_time = -1

    def enter_info(self):
        #later add function where we can use a hashing function to store a hashed password instead the literal password
        #if collection in database exists, create user's document
        if userCollect != None:
           the_dict = {"username": self.username, "password": self.password, "allergies": self.allergies, 
           "cookingTime": self.cooking_time, "viewedRecipes": dict()} 
           userCollect.insert_one(the_dict)
        RexableApp.store.put('credentials', username = self.username, password = self.password)
        self.parent.current = "main_screen"
        


class SettingsScreen(Screen):
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


        if self.user_login[0] != "" and self.user_login[1] != "":
            self.sm.current = 'main_screen'
        else:
            self.sm.current = 'login_screen'

    def build(self):
        username = ''
        password = ''
        self.sm.add_widget(MainScreen(name='main_screen'))
        self.sm.add_widget(LoginScreen(name='login_screen'))
        self.sm.add_widget(SignUpScreen())
        self.sm.add_widget(SettingsScreen(name='setting_screen'))
        self.sm.add_widget(ProfileScreen(name='profile_screen'))
        self.sm.add_widget(RecommendationPreferenceScreen(name='recommendation_preference_screen'))
        self.sm.add_widget(AboutScreen(name='about_screen'))
        self.sm.add_widget(RecipeSearchBar(name='recipe_search_bar'))

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

        
        if self.user_login[0] != "" and self.user_login[1] != "":
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
        try:
            results = userCollect.find_one({"username": self.username})
            #if results == None:
            #    self.parent.current = 'login_screen'
            if results["password"] == self.password:
                #this is just a preliminary password/username system; will add hashing and encryption later
                RexableApp.store.put('credentials', username = self.username, password = self.password)
                self.parent.current = 'main_screen'
            else:
                self.parent.current = 'login_screen'
        except errors.CollectionInvalid:
            self.parent.current = 'login_screen'

class MainScreen(Screen):
    def logout(self):
        RexableApp.store.put('credentials', username = "", password = "")
        RexableApp().stop()

if __name__ == '__main__':
    RexableApp().run()
