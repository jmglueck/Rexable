from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.dropdown import DropDown
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.gridlayout import GridLayout
from kivy.storage.jsonstore import JsonStore
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from pymongo import MongoClient,errrors
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
    canvas.before:
        Color:
            rgba: 0, 0, 102, 0.2
        Rectangle:
            pos: self.pos
            size: self.size
    name: 'login_screen'
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'top'
        pos_hint: {'x': 0.35}
        BoxLayout:
            orientation: 'vertical'
            size_hint: (0.9, 0.7)
            padding: [15,15]
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
        pos_hint: {'x': 0.15}
        BoxLayout:
            spacing: 15
            orientation: 'horizontal'
            Button:
                text: 'Login'
                background_normal: ''
                background_color: 102, 102, 153, 0.4
                size_hint: (0.5, 0.5)
                pos_hint: {'y': 0.5}
                on_release: root.login()
            Button:
                text: 'Sign Up'
                background_normal: ''
                background_color: 102, 102, 153, 0.4
                size_hint: (0.5, 0.5)
                pos_hint: {'y': 0.5}
                on_release: root.manager.current = 'signup_screen'

<SignUpScreen>:
    canvas.before:
        Color:
            rgba: 0, 0, 102, 0.2
        Rectangle:
            pos: self.pos
            size: self.size
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
            background_normal: ''
            background_color: 102, 102, 153, 0.4
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
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.enter_info()
<DietDropDown>:
    text: 'Diet'

<SettingsScreen>:
    canvas.before:
        Color:
            rgba: 0, 0, 102, 0.2
        Rectangle:
            pos: self.pos
            size: self.size
    name: 'settings_screen'
    BoxLayout:
        orientation: 'vertical'
        Button:
            text: 'Profile'
            size_hint: (.5, .5)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.manager.current = 'profile_screen'
        Button:
            text: 'Recommendation Preferences'
            size_hint: (.5, .5)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.manager.current = 'recommendation_preference_screen'
        Button:
            text: 'About'
            size_hint: (.5, .5)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.manager.current = 'about_screen'
        Button:
            text: 'Back'
            size_hint: (.5, .5)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.manager.current = 'main_screen'

<ProfileScreen>:
    canvas.before:
        Color:
            rgba: 0, 0, 102, 0.2
        Rectangle:
            pos: self.pos
            size: self.size
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
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.manager.current = 'settings_screen'

<RecommendationPreferenceScreen>:
    canvas.before:
        Color:
            rgba: 0, 0, 102, 0.2
        Rectangle:
            pos: self.pos
            size: self.size
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
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.manager.current = 'settings_screen'

<AboutScreen>:
    canvas.before:
        Color:
            rgba: 0, 0, 102, 0.2
        Rectangle:
            pos: self.pos
            size: self.size
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
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.manager.current = 'settings_screen'



<RecipeSearchBar>:

    name: 'recipe_search_bar'

    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            orientation: 'horizontal'
            size_hint: (1, 0.5)
            TextInput:
                id: text_input
                multiline: False
                font_size: '18sp'
                size_hint: (7, 0.3)
                pos_hint:{'center_x':0,'center_y':0.9}
                on_text: root.get_query(self.text)
            Button:
                text: 'Search'
                size_hint: (1,0.3)
                pos_hint:{'center_x':0,'center_y':0.9}
                background_normal: ''
                background_color: 102, 102, 153, 0.4
                font_size: '18sp'
                text_size: self.width - dp(5), self.height - dp(5)
                on_release: root.start_search()

        BoxLayout:
            orientation: 'vertical'
            size_hint: (1, 0.5)
            spacing: 20
            Label:
                id: result_1
                pos_hint:{'center_x':0.5,'center_y':0.7}
                text: ''
                halign: 'left'

            Label:
                id: result_2
                pos_hint:{'center_x':0.5,'center_y':0.7}
                text: ''
                halign: 'left'

            Label:
                id: result_3
                pos_hint:{'center_x':0.5,'center_y':0.7}
                text: ''
                halign: 'left'

            Label:
                id: result_4
                pos_hint:{'center_x':0.5,'center_y':0.6}
                text: ''
                halign: 'left'

            Label:
                id: result_5
                pos_hint:{'center_x':0.5,'center_y':0.5}
                text: ''
                halign: 'left'

            Label:
                id: result_6
                pos_hint:{'center_x':0.5,'center_y':0.4}
                text: ''

            Label:
                id: result_7
                pos_hint:{'center_x':0.5,'center_y':0.3}
                text: ''
                halign: 'left'

            Label:
                id: result_8
                pos_hint:{'center_x':0.5,'center_y':0.2}
                text: ''
                halign: 'left'


            Label:
                id: result_9
                pos_hint:{'center_x':0.5,'center_y':0.1}
                text: ''
                halign: 'left'

            Label:
                id: result_10
                pos_hint:{'center_x':0.5,'center_y':0.0}
                text: ''
                halign: 'left'


<MeatCategory>
    name: 'meat_category'

    size_hint: (1, 1)


    BoxLayout:
        orientation: 'horizontal'

        Button:
            text: 'Chicken'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('chicken')




        Button:
            text: 'Beef'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('beef')


        Button:
            text: 'Pork'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('pork')



        Button:
            text: 'Lamb'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('lamb')


        Button:
            text: 'Turkey'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('turkey')


        Button:
            text: 'Back'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.manager.current = 'recommendation'

    BoxLayout:
        orientation: 'vertical'
        Label:
            id: result_1
            pos_hint:{'center_x':0.5,'center_y':0.8}
            text: ''
            size_hint: (0.8,0.1)
            halign: 'left'

        Label:
            id: result_2
            pos_hint:{'center_x':0.5,'center_y':0.7}
            text: ''
            size_hint: (0.8,0.1)
            halign: 'left'

        Label:
            id: result_3
            pos_hint:{'center_x':0.5,'center_y':0.6}
            text: ''
            size_hint: (0.8,0.1)
            halign: 'left'

        Label:
            id: result_4
            pos_hint:{'center_x':0.5,'center_y':0.5}
            text: ''
            size_hint: (0.8,0.1)
            halign: 'left'

        Label:
            id: result_5
            pos_hint:{'center_x':0.5,'center_y':0.4}
            text: ''
            size_hint: (0.8,0.1)
            halign: 'left'

        Label:
            id: result_6
            pos_hint:{'center_x':0.5,'center_y':0.3}
            text: ''
            size_hint: (0.8,0.1)

        Label:
            id: result_7
            pos_hint:{'center_x':0.5,'center_y':0.2}
            text: ''
            size_hint: (0.8,0.1)
            halign: 'left'

        Label:
            id: result_8
            pos_hint:{'center_x':0.5,'center_y':0.1}
            text: ''
            size_hint: (0.8,0.1)
            halign: 'left'


        Label:
            id: result_9
            pos_hint:{'center_x':0.5,'center_y':0.05}
            text: ''
            size_hint: (0.8,0.1)
            halign: 'left'

        Label:
            id: result_10
            pos_hint:{'center_x':0.5,'center_y':0.04}
            text: ''
            size_hint: (0.8,0.1)
            halign: 'left'


<Recommendation>:

    name: 'recommendation'
    size_hint: (1, 0.115)
    BoxLayout:
        orientation: 'horizontal'

        Button:
            text: 'Meat'
            size_hint: (0.5,0.9)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.manager.current = 'meat_category'
        Button:
            text: 'Seafood'
            size_hint: (0.5,0.9)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.seafood()

        Button:
            text: 'Vegetable'
            size_hint: (0.5,0.9)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.vegetable()

        Button:
            text: 'Fruit'
            size_hint: (0.5,0.9)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.fruit()



        Button:
            text: 'Drinks'
            size_hint: (0.5,0.9)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.drinks()

        Button:
            text: 'Dessert'
            size_hint: (0.5,0.9)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.dessert()

        Button:
            text: 'Back'
            size_hint: (0.5,0.9)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.manager.current = 'main_screen'


<MainScreen>:
    canvas.before:
        Color:
            rgba: 0, 0, 102, 0.2
        Rectangle:
            pos: self.pos
            size: self.size
    name: 'main_screen'
    BoxLayout:
        orientation: 'vertical'
        RecipeSearchBar:
        RecommendationLayout:
        BoxLayout:
            orientation: 'horizontal'
            Button:
                canvas.before:
                    Color:
                        rgba: 0, 0, 0, 1
                    Line:
                        width: 2
                        rectangle: self.x, self.y, self.width, self.height
                text: 'Settings'
                size_hint: (.5, .5)
                background_normal: ''
                background_color: 102, 102, 153, 0.4
                on_release: root.manager.current = 'settings_screen'


            Button:
                canvas.before:
                    Color:
                        rgba: 0, 0, 0, 1
                    Line:
                        width: 2
                        rectangle: self.x, self.y, self.width, self.height
                text: 'Recommendation'
                size_hint: (.5, .5)
                background_normal: ''
                background_color: 102, 102, 153, 0.4
                on_press: root.manager.current = 'recommendation'


            Button:
                canvas.before:
                    Color:
                        rgba: 0, 0, 0, 1
                    Line:
                        width: 2
                        rectangle: self.x, self.y, self.width, self.height
                text: 'Quit'
                size_hint: (.5, .5)
                background_normal: ''
                background_color: 102, 102, 153, 0.4
                on_press: app.stop()

            Button:
                canvas.before:
                    Color:
                        rgba: 0, 0, 0, 1
                    Line:
                        width: 2
                        rectangle: self.x, self.y, self.width, self.height
                text: 'Logout'
                size_hint: (.5, .5)
                background_normal: ''
                background_color: 102, 102, 153, 0.4
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
            diet_button = Button(text=i, size_hint_y=None, height =35, background_normal='', background_color=[102, 102, 153, 0.4])
            diet_button.bind(on_release=lambda diet_button: drop_down.select(diet_button.text))
            drop_down.add_widget(diet_button)
        #main_button = Button(text='Diet', size_hint=(None, None), height=40)
        #main_button.bind(on_release=drop_down.open)
        self.bind(on_release=drop_down.open)
        drop_down.bind(on_select=lambda instance, x: setattr(self, 'text', x))

class RecommendationLayout(GridLayout):
    pass

class RecipeSearchBar(BoxLayout):

    def get_query(self,query):

        self.query = query.lower()

    def start_search(self):

        database_result = recipeCollect.find({"search_query": self.query}).limit(10)
        
        self.result = database_result

       
        
        if database_result.count() != 0:
            for count,i in enumerate(database_result):

                new_text = f"{count+1}. {i['recipe_name']}, {i['calories']} Cal"
                
                exec(f'self.ids.result_{count+1}.text = "{new_text}"')

            self.ids.text_input.text = ''


        else:
        
            result = search(self.query)
            self.result = result

            ten_results = result[:10]

            for count,i in enumerate(ten_results):

                new_text = f"{count+1}. {i['recipe_name']}, {i['calories']} Cal"

                exec(f'self.ids.result_{count+1}.text = "{new_text}"')

            if recipeCollect != None:
                recipeCollect.insert_many(result)



            self.ids.text_input.text = ''

class Recommendation(Screen):




    def meat(self):

        print('Meat')


    def seafood(self):

        print('Seafood')


    def vegetable(self):

        print('Vegetable')


    def fruit(self):

        print('Fruit')


    def drinks(self):

        print('Drinks')


    def dessert(self):

        print('Dessert')


class MeatCategory(Screen):

    def start_search(self,query):

        query = query.lower()
        
        database_result = recipeCollect.find({"search_query": query}).limit(10)
        
        self.result = database_result

        if database_result.count() != 0:
            for count,i in enumerate(database_result):

                new_text = f"{count+1}. {i['recipe_name']}, {i['calories']} Cal"
                
                exec(f'self.ids.result_{count+1}.text = "{new_text}"')



        else:
        
            result = search(query)
            self.result = result


            ten_results = result[:10]

            for count,i in enumerate(ten_results):

                new_text = f"{count+1}. {i['recipe_name']}, {i['calories']} Cal"

                exec(f'self.ids.result_{count+1}.text = "{new_text}"')

                
            
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
        self.sm.add_widget(SettingsScreen(name='settings_screen'))
        self.sm.add_widget(ProfileScreen(name='profile_screen'))
        self.sm.add_widget(RecommendationPreferenceScreen(name='recommendation_preference_screen'))
        self.sm.add_widget(AboutScreen(name='about_screen'))
        self.sm.add_widget(Recommendation(name='recommendation'))
        self.sm.add_widget(MeatCategory(name='meat_category'))

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
