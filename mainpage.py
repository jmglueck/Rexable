from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.lang import Builder
from kivy.uix.dropdown import DropDown
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.gridlayout import GridLayout
from kivy.storage.jsonstore import JsonStore
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.loader import Loader
from pymongo import MongoClient,errors
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
            spacing: 20

            ClickableLabel:
                id: result_1
                pos_hint:{'center_x':0.5,'center_y':0.7}

            ClickableLabel:
                id: result_2
                pos_hint:{'center_x':0.5,'center_y':0.7}
                text: ''
                halign: 'left'



            ClickableLabel:
                id: result_3
                pos_hint:{'center_x':0.5,'center_y':0.7}
                text: ''
                halign: 'left'


            ClickableLabel:
                id: result_4
                pos_hint:{'center_x':0.5,'center_y':0.6}
                text: ''
                halign: 'left'

            ClickableLabel:
                id: result_5
                pos_hint:{'center_x':0.5,'center_y':0.5}
                text: ''
                halign: 'left'

            ClickableLabel:
                id: result_6
                pos_hint:{'center_x':0.5,'center_y':0.4}
                text: ''

            ClickableLabel:
                id: result_7
                pos_hint:{'center_x':0.5,'center_y':0.3}
                text: ''
                halign: 'left'

            ClickableLabel:
                id: result_8
                pos_hint:{'center_x':0.5,'center_y':0.2}
                text: ''
                halign: 'left'


            ClickableLabel:
                id: result_9
                pos_hint:{'center_x':0.5,'center_y':0.1}
                text: ''
                halign: 'left'

            ClickableLabel:
                id: result_10
                pos_hint:{'center_x':0.5,'center_y':0.0}
                text: ''
                halign: 'left'

<ClickableLabel@ButtonBehavior+Label>:
    text: ''
    halign: 'left'
    on_press: app.goto_recipe_screen(self.data)

<MeatCategory>
    name: 'meat_category'
    canvas.before:
        Color:
            rgba: 0, 0, 102, 0.2
        Rectangle:
            pos: self.pos
            size: self.size

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
            text: 'Search More'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.manager.current = 'main_screen'


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
            AsyncImage:
                id: img_1
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}
                
            AsyncImage:
                id: img_2
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}



            AsyncImage:
                id: img_3
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}


            AsyncImage:
                id: img_4
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}


            AsyncImage:
                id: img_5
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}


            AsyncImage:
                id: img_6
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}



            AsyncImage:
                id: img_7
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}


            AsyncImage:
                id: img_8
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}



            AsyncImage:
                id: img_9
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}


            AsyncImage:
                id: img_10
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}

    BoxLayout:
        orientation: 'vertical'
        spacing: 25
        size_hint: (0.6, 0.65)
        pos_hint:{'center_x': 0.6, 'center_y': 0.4}
        ClickableLabel:
            id: result_1
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'
        ClickableLabel:
            id: result_2
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'

        ClickableLabel:
            id: result_3
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'
        ClickableLabel:
            id: result_4
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'
        ClickableLabel:
            id: result_5
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'
        ClickableLabel:
            id: result_6
            text: ''
            size_hint: (0.8,0.5)
        ClickableLabel:
            id: result_7
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'
        ClickableLabel:
            id: result_8
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'
        ClickableLabel:
            id: result_9
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'
        ClickableLabel:
            id: result_10
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'



<SeafoodCategory>
    name: 'seafood_category'
    canvas.before:
        Color:
            rgba: 0, 0, 102, 0.2
        Rectangle:
            pos: self.pos
            size: self.size

    size_hint: (1, 1)


    BoxLayout:
        orientation: 'horizontal'

        Button:
            text: 'Crab'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('crab')

        Button:
            text: 'Fish'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('fish')

        Button:
            text: 'Shrimp'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('shrimp')

        Button:
            text: 'Lobster'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('lobster')
        Button:
            text: 'Scallop'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('scallop')


        Button:
            text: 'Search More'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.manager.current = 'main_screen'



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
            AsyncImage:
                id: img_1
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}
                
            AsyncImage:
                id: img_2
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}



            AsyncImage:
                id: img_3
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}


            AsyncImage:
                id: img_4
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}


            AsyncImage:
                id: img_5
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}


            AsyncImage:
                id: img_6
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}



            AsyncImage:
                id: img_7
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}


            AsyncImage:
                id: img_8
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}



            AsyncImage:
                id: img_9
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}


            AsyncImage:
                id: img_10
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}



    BoxLayout:
        orientation: 'vertical'
        spacing: 25
        size_hint: (0.6, 0.65)
        pos_hint:{'center_x': 0.6, 'center_y': 0.4}
        ClickableLabel:
            id: result_1
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'
        ClickableLabel:
            id: result_2
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'

        ClickableLabel:
            id: result_3
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'
        ClickableLabel:
            id: result_4
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'
        ClickableLabel:
            id: result_5
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'
        ClickableLabel:
            id: result_6
            text: ''
            size_hint: (0.8,0.5)
        ClickableLabel:
            id: result_7
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'
        ClickableLabel:
            id: result_8
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'
        ClickableLabel:
            id: result_9
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'
        ClickableLabel:
            id: result_10
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'





<VegetableCategory>
    name: 'vegetable_category'
    canvas.before:
        Color:
            rgba: 0, 0, 102, 0.2
        Rectangle:
            pos: self.pos
            size: self.size

    size_hint: (1, 1)


    BoxLayout:
        orientation: 'horizontal'

        Button:
            text: 'Salad'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('salad')
            
        Button:
            text: 'Bean'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('bean')

        Button:
            text: 'Broccoli'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('broccoli')


        Button:
            text: 'Carrot'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('carrot')

        Button:
            text: 'Cauliflower'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('cauliflower')
        Button:
            text: 'Cucumber'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('cucumber')


        Button:
            text: 'Eggplant'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('eggplant')

        Button:
            text: 'Mushroom'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('mushroom')

            
        Button:
            text: 'Potato'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('Potato')


        Button:
            text: 'Search More'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.manager.current = 'main_screen'


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
            AsyncImage:
                id: img_1
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}
                
            AsyncImage:
                id: img_2
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}



            AsyncImage:
                id: img_3
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}


            AsyncImage:
                id: img_4
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}


            AsyncImage:
                id: img_5
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}


            AsyncImage:
                id: img_6
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}



            AsyncImage:
                id: img_7
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}


            AsyncImage:
                id: img_8
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}



            AsyncImage:
                id: img_9
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}


            AsyncImage:
                id: img_10
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}



    BoxLayout:
        orientation: 'vertical'
        spacing: 25
        size_hint: (0.6, 0.65)
        pos_hint:{'center_x': 0.6, 'center_y': 0.4}
        ClickableLabel:
            id: result_1
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'
        ClickableLabel:
            id: result_2
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'

        ClickableLabel:
            id: result_3
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'
        ClickableLabel:
            id: result_4
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'
        ClickableLabel:
            id: result_5
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'
        ClickableLabel:
            id: result_6
            text: ''
            size_hint: (0.8,0.5)
        ClickableLabel:
            id: result_7
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'
        ClickableLabel:
            id: result_8
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'
        ClickableLabel:
            id: result_9
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'
        ClickableLabel:
            id: result_10
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'







<FruitCategory>
    name: 'fruit_category'
    canvas.before:
        Color:
            rgba: 0, 0, 102, 0.2
        Rectangle:
            pos: self.pos
            size: self.size

    size_hint: (1, 1)


    BoxLayout:
        orientation: 'horizontal'

        Button:
            text: 'Apple'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('apple')


        Button:
            text: 'Avocado'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('avocado')

        Button:
            text: 'Banana'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('banana')

        Button:
            text: 'Blueberry'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('blueberry')


        Button:
            text: 'Cherry'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('cherry')

        Button:
            text: 'Coconut'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('coconut')
            
        Button:
            text: 'Dragonfruit'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('dragonfruit')


        Button:
            text: 'Grape'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('grape')

        Button:
            text: 'Plum'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('plum')

            
        Button:
            text: 'Lemon'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('lemon')



        Button:
            text: 'Mango'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('mango')

        Button:
            text: 'Watermelon'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('watermelon')

            
        Button:
            text: 'Orange'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('orange')


        Button:
            text: 'Peach'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('peach')

            
        Button:
            text: 'Pineapple'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('pineapple')


        Button:
            text: 'Search More'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.manager.current = 'main_screen'


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
            AsyncImage:
                id: img_1
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}
                
            AsyncImage:
                id: img_2
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}



            AsyncImage:
                id: img_3
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}


            AsyncImage:
                id: img_4
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}


            AsyncImage:
                id: img_5
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}


            AsyncImage:
                id: img_6
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}



            AsyncImage:
                id: img_7
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}


            AsyncImage:
                id: img_8
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}



            AsyncImage:
                id: img_9
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}


            AsyncImage:
                id: img_10
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}




    BoxLayout:
        orientation: 'vertical'
        spacing: 25
        size_hint: (0.6, 0.65)
        pos_hint:{'center_x': 0.6, 'center_y': 0.4}
        ClickableLabel:
            id: result_1
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'
        ClickableLabel:
            id: result_2
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'

        ClickableLabel:
            id: result_3
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'
        ClickableLabel:
            id: result_4
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'
        ClickableLabel:
            id: result_5
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'
        ClickableLabel:
            id: result_6
            text: ''
            size_hint: (0.8,0.5)
        ClickableLabel:
            id: result_7
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'
        ClickableLabel:
            id: result_8
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'
        ClickableLabel:
            id: result_9
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'
        ClickableLabel:
            id: result_10
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'





<DrinksCategory>
    name: 'drinks_category'
    canvas.before:
        Color:
            rgba: 0, 0, 102, 0.2
        Rectangle:
            pos: self.pos
            size: self.size

    size_hint: (1, 1)


    BoxLayout:
        orientation: 'horizontal'

        Button:
            text: 'Beer'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('beer')


        Button:
            text: 'Cocktails'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('cocktails')

        Button:
            text: 'Wine'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('wine')

        Button:
            text: 'Hot Chocolate'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('Hot Chocolate')


        Button:
            text: 'Coffee'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('Coffee')

        Button:
            text: 'Milk'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('Milk')
            
        Button:
            text: 'Tea'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('Tea')



        Button:
            text: 'Apple Juice'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('apple juice')

            

        Button:
            text: 'Orange Juice'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('orange juice')

        Button:
            text: 'Lemonade'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('lemonade')


        Button:
            text: 'Soda'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('Soda')


        Button:
            text: 'Search More'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.manager.current = 'main_screen'


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
            AsyncImage:
                id: img_1
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}
                
            AsyncImage:
                id: img_2
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}



            AsyncImage:
                id: img_3
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}


            AsyncImage:
                id: img_4
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}


            AsyncImage:
                id: img_5
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}


            AsyncImage:
                id: img_6
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}



            AsyncImage:
                id: img_7
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}


            AsyncImage:
                id: img_8
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}



            AsyncImage:
                id: img_9
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}


            AsyncImage:
                id: img_10
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}




    BoxLayout:
        orientation: 'vertical'
        spacing: 25
        size_hint: (0.6, 0.65)
        pos_hint:{'center_x': 0.6, 'center_y': 0.4}
        ClickableLabel:
            id: result_1
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'
        ClickableLabel:
            id: result_2
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'

        ClickableLabel:
            id: result_3
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'
        ClickableLabel:
            id: result_4
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'
        ClickableLabel:
            id: result_5
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'
        ClickableLabel:
            id: result_6
            text: ''
            size_hint: (0.8,0.5)
        ClickableLabel:
            id: result_7
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'
        ClickableLabel:
            id: result_8
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'
        ClickableLabel:
            id: result_9
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'
        ClickableLabel:
            id: result_10
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'




<DessertCategory>
    name: 'dessert_category'
    canvas.before:
        Color:
            rgba: 0, 0, 102, 0.2
        Rectangle:
            pos: self.pos
            size: self.size

    size_hint: (1, 1)


    BoxLayout:
        orientation: 'horizontal'

        Button:
            text: 'Cake'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('cake')


        Button:
            text: 'Candy'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('candy')

        Button:
            text: 'Cookie'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('cookie')

        Button:
            text: 'Custard'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('custard')


        Button:
            text: 'Donut'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('donut')

        Button:
            text: 'Ice Cream'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('ice cream')
            
        Button:
            text: 'Pastry'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('pastry')



        Button:
            text: 'Pie'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('pie')

            

        Button:
            text: 'Pudding'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.start_search('pudding')

      
        Button:
            text: 'Search More'
            pos_hint:{'center_x':0,'center_y':1}
            text_size: self.width - dp(10), self.height - dp(10)
            size_hint: (0.3,0.2)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.manager.current = 'main_screen'


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
            AsyncImage:
                id: img_1
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}
                
            AsyncImage:
                id: img_2
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}



            AsyncImage:
                id: img_3
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}


            AsyncImage:
                id: img_4
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}


            AsyncImage:
                id: img_5
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}


            AsyncImage:
                id: img_6
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}



            AsyncImage:
                id: img_7
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}


            AsyncImage:
                id: img_8
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}



            AsyncImage:
                id: img_9
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}


            AsyncImage:
                id: img_10
                source: ''
                pos_hint:{'center_x':0.7,'center_y':0.7}



    BoxLayout:
        orientation: 'vertical'
        spacing: 25
        size_hint: (0.6, 0.65)
        pos_hint:{'center_x': 0.6, 'center_y': 0.4}
        ClickableLabel:
            id: result_1
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'
        ClickableLabel:
            id: result_2
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'

        ClickableLabel:
            id: result_3
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'
        ClickableLabel:
            id: result_4
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'
        ClickableLabel:
            id: result_5
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'
        ClickableLabel:
            id: result_6
            text: ''
            size_hint: (0.8,0.5)
        ClickableLabel:
            id: result_7
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'
        ClickableLabel:
            id: result_8
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'
        ClickableLabel:
            id: result_9
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'
        ClickableLabel:
            id: result_10
            text: ''
            size_hint: (0.8,0.5)
            halign: 'left'



<Recommendation>:

    name: 'recommendation'
    size_hint: (1, 0.115)
    canvas.before:
        Color:
            rgba: 0, 0, 102, 0.2
        Rectangle:
            pos: self.pos
            size: self.size
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
            on_release: root.manager.current = 'seafood_category'

        Button:
            text: 'Vegetable'
            size_hint: (0.5,0.9)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.manager.current = 'vegetable_category'

        Button:
            text: 'Fruit'
            size_hint: (0.5,0.9)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.manager.current = 'fruit_category'

        Button:
            text: 'Drinks'
            size_hint: (0.5,0.9)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.manager.current = 'drinks_category'

        Button:
            text: 'Dessert'
            size_hint: (0.5,0.9)
            background_normal: ''
            background_color: 102, 102, 153, 0.4
            on_release: root.manager.current = 'dessert_category'

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

<RecipeScreen>:
    name: 'recipe_screen'
    id: recipe_screen

""")

class ClickableLabel(ButtonBehavior, Label):
    def __init__(self):
        ButtonBehavior.__init__(self)
        Label.__init__(self)
        self.data = {}


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
                img_link = i["image_link"]
                exec(f'self.ids.result_{count+1}.text = "{new_text}"')
                exec(f'self.ids.result_{count+1}.data = i')
                #exec(f'self.ids.img_{count+1}.source = "{img_link}"')
                
            self.ids.text_input.text = ''


        else:
        
            result = search(self.query)
            self.result = result

            ten_results = result[:10]

            for count,i in enumerate(ten_results):

                new_text = f"{count+1}. {i['recipe_name']}, {i['calories']} Cal"
                img_link = i["image_link"]
                exec(f'self.ids.result_{count+1}.text = "{new_text}"')
                exec(f'self.ids.result_{count+1}.data = i')
                #exec(f'self.ids.img_{count+1}.source = "{img_link}"')

            if recipeCollect != None and result !=[]:
                print(result)
                recipeCollect.insert_many(result)
            else:
                self.ids.result_1.text = 'No Result'


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
                img_link = i["image_link"]
                exec(f'self.ids.result_{count+1}.text = "{new_text}"')
                exec(f'self.ids.img_{count+1}.source = "{img_link}"')

        else:
        
            result = search(query)
            self.result = result


            ten_results = result[:10]

            for count,i in enumerate(ten_results):

                new_text = f"{count+1}. {i['recipe_name']}, {i['calories']} Cal"
                img_link = i["image_link"]
                exec(f'self.ids.result_{count+1}.text = "{new_text}"')
                exec(f'self.ids.img_{count+1}.source = "{img_link}"')
            
            if recipeCollect != None and result !=[]:
                recipeCollect.insert_many(result)
            else:
                self.ids.result_1.text = 'No Result'
                

class SeafoodCategory(Screen):

    def start_search(self,query):

        query = query.lower()
        
        database_result = recipeCollect.find({"search_query": query}).limit(10)
        
        self.result = database_result

        if database_result.count() != 0:
            for count,i in enumerate(database_result):

                new_text = f"{count+1}. {i['recipe_name']}, {i['calories']} Cal"
                img_link = i["image_link"]
                exec(f'self.ids.result_{count+1}.text = "{new_text}"')
                exec(f'self.ids.img_{count+1}.source = "{img_link}"')

        else:
        
            result = search(query)
            self.result = result


            ten_results = result[:10]

            for count,i in enumerate(ten_results):

                new_text = f"{count+1}. {i['recipe_name']}, {i['calories']} Cal"
                img_link = i["image_link"]
                exec(f'self.ids.result_{count+1}.text = "{new_text}"')
                exec(f'self.ids.img_{count+1}.source = "{img_link}"')
            
            if recipeCollect != None and result !=[]:
                recipeCollect.insert_many(result)
            else:
                self.ids.result_1.text = 'No Result'


class VegetableCategory(Screen):

    def start_search(self,query):

        query = query.lower()
        
        database_result = recipeCollect.find({"search_query": query}).limit(10)
        
        self.result = database_result

        if database_result.count() != 0:
            for count,i in enumerate(database_result):

                new_text = f"{count+1}. {i['recipe_name']}, {i['calories']} Cal"
                img_link = i["image_link"]
                exec(f'self.ids.result_{count+1}.text = "{new_text}"')
                exec(f'self.ids.img_{count+1}.source = "{img_link}"')

        else:
        
            result = search(query)
            self.result = result


            ten_results = result[:10]

            for count,i in enumerate(ten_results):

                new_text = f"{count+1}. {i['recipe_name']}, {i['calories']} Cal"
                img_link = i["image_link"]
                exec(f'self.ids.result_{count+1}.text = "{new_text}"')
                exec(f'self.ids.img_{count+1}.source = "{img_link}"')
            
            if recipeCollect != None and result !=[]:
                recipeCollect.insert_many(result)
            else:
                self.ids.result_1.text = 'No Result'


class FruitCategory(Screen):

    def start_search(self,query):

        query = query.lower()
        
        database_result = recipeCollect.find({"search_query": query}).limit(10)
        
        self.result = database_result

        if database_result.count() != 0:
            for count,i in enumerate(database_result):

                new_text = f"{count+1}. {i['recipe_name']}, {i['calories']} Cal"
                img_link = i["image_link"]
                exec(f'self.ids.result_{count+1}.text = "{new_text}"')
                exec(f'self.ids.img_{count+1}.source = "{img_link}"')

        else:
        
            result = search(query)
            self.result = result


            ten_results = result[:10]

            for count,i in enumerate(ten_results):

                new_text = f"{count+1}. {i['recipe_name']}, {i['calories']} Cal"
                img_link = i["image_link"]
                exec(f'self.ids.result_{count+1}.text = "{new_text}"')
                exec(f'self.ids.img_{count+1}.source = "{img_link}"')
            
            if recipeCollect != None and result !=[]:
                recipeCollect.insert_many(result)
            else:
                self.ids.result_1.text = 'No Result'


class DrinksCategory(Screen):

    def start_search(self,query):

        query = query.lower()
        
        database_result = recipeCollect.find({"search_query": query}).limit(10)
        
        self.result = database_result

        if database_result.count() != 0:
            for count,i in enumerate(database_result):

                new_text = f"{count+1}. {i['recipe_name']}, {i['calories']} Cal"
                img_link = i["image_link"]
                exec(f'self.ids.result_{count+1}.text = "{new_text}"')
                exec(f'self.ids.img_{count+1}.source = "{img_link}"')

        else:
        
            result = search(query)
            self.result = result


            ten_results = result[:10]

            for count,i in enumerate(ten_results):

                new_text = f"{count+1}. {i['recipe_name']}, {i['calories']} Cal"
                img_link = i["image_link"]
                exec(f'self.ids.result_{count+1}.text = "{new_text}"')
                exec(f'self.ids.img_{count+1}.source = "{img_link}"')
            
            if recipeCollect != None and result !=[]:
                recipeCollect.insert_many(result)
            else:
                self.ids.result_1.text = 'No Result'
                

class DessertCategory(Screen):

    def start_search(self,query):

        query = query.lower()
        
        database_result = recipeCollect.find({"search_query": query}).limit(10)
        
        self.result = database_result

        if database_result.count() != 0:
            for count,i in enumerate(database_result):

                new_text = f"{count+1}. {i['recipe_name']}, {i['calories']} Cal"
                img_link = i["image_link"]
                exec(f'self.ids.result_{count+1}.text = "{new_text}"')
                exec(f'self.ids.img_{count+1}.source = "{img_link}"')

        else:
        
            result = search(query)
            self.result = result


            ten_results = result[:10]

            for count,i in enumerate(ten_results):

                new_text = f"{count+1}. {i['recipe_name']}, {i['calories']} Cal"
                img_link = i["image_link"]
                exec(f'self.ids.result_{count+1}.text = "{new_text}"')
                exec(f'self.ids.img_{count+1}.source = "{img_link}"')
            
            if recipeCollect != None and result !=[]:
                recipeCollect.insert_many(result)
            else:
                self.ids.result_1.text = 'No Result'

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


class RecipeScreen(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        app = App.get_running_app()
        self.data = app.data
        self.data = app.data
        self.name = 'recipe_screen'
        boxlayout = BoxLayout()
        label = Label(text=self.data["recipe_name"])
        boxlayout.add_widget(label)
        self.add_widget(boxlayout)


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
        self.data = {"recipe_name": "test"}


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
        self.sm.add_widget(SeafoodCategory(name='seafood_category'))
        self.sm.add_widget(VegetableCategory(name='vegetable_category'))
        self.sm.add_widget(FruitCategory(name='fruit_category'))
        self.sm.add_widget(DrinksCategory(name='drinks_category'))
        self.sm.add_widget(DessertCategory(name='dessert_category'))
        self.sm.add_widget(RecipeScreen())


        
    
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
    
    def goto_recipe_screen(self, the_data):
        self.sm.current = 'recipe_screen'
        self.data = the_data

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
