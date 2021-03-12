# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.storage.jsonstore import JsonStore
from kivy.uix.image import AsyncImage
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty, \
    NumericProperty, ListProperty, OptionProperty

from kivymd.bottomsheet import MDListBottomSheet, MDGridBottomSheet
from kivymd.button import MDIconButton
from kivymd.date_picker import MDDatePicker
from kivymd.dialog import MDDialog
from kivymd.label import MDLabel
from kivymd.list import ILeftBody, ILeftBodyTouch, IRightBodyTouch, BaseListItem
from kivymd.material_resources import DEVICE_TYPE
from kivymd.navigationdrawer import MDNavigationDrawer, NavigationDrawerHeaderBase
from kivymd.selectioncontrols import MDCheckbox
from kivymd.snackbar import Snackbar
from kivymd.theming import ThemeManager
from kivymd.time_picker import MDTimePicker
from kivymd.grid import SmartTileWithLabel
from kivymd.list import OneLineAvatarIconListItem

from basic_search import search
from bmi import get_bmi
from data import food_data
from webscraper import webscrape_recipe


from pymongo import MongoClient,errors

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

main_widget_kv = '''
#:import Toolbar kivymd.toolbar.Toolbar
#:import ThemeManager kivymd.theming.ThemeManager
#:import MDNavigationDrawer kivymd.navigationdrawer.MDNavigationDrawer
#:import NavigationLayout kivymd.navigationdrawer.NavigationLayout
#:import NavigationDrawerDivider kivymd.navigationdrawer.NavigationDrawerDivider
#:import NavigationDrawerToolbar kivymd.navigationdrawer.NavigationDrawerToolbar
#:import NavigationDrawerSubheader kivymd.navigationdrawer.NavigationDrawerSubheader
#:import MDCheckbox kivymd.selectioncontrols.MDCheckbox
#:import MDSwitch kivymd.selectioncontrols.MDSwitch
#:import MDList kivymd.list.MDList
#:import OneLineListItem kivymd.list.OneLineListItem
#:import TwoLineListItem kivymd.list.TwoLineListItem
#:import ThreeLineListItem kivymd.list.ThreeLineListItem
#:import OneLineAvatarListItem kivymd.list.OneLineAvatarListItem
#:import OneLineIconListItem kivymd.list.OneLineIconListItem
#:import OneLineAvatarIconListItem kivymd.list.OneLineAvatarIconListItem
#:import MDTextField kivymd.textfields.MDTextField
#:import MDSpinner kivymd.spinner.MDSpinner
#:import MDCard kivymd.card.MDCard
#:import MDSeparator kivymd.card.MDSeparator
#:import MDDropdownMenu kivymd.menu.MDDropdownMenu
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:import colors kivymd.color_definitions.colors
#:import SmartTile kivymd.grid.SmartTile
#:import MDSlider kivymd.slider.MDSlider
#:import MDTabbedPanel kivymd.tabs.MDTabbedPanel
#:import MDTab kivymd.tabs.MDTab
#:import MDProgressBar kivymd.progressbar.MDProgressBar
#:import MDAccordion kivymd.accordion.MDAccordion
#:import MDAccordionItem kivymd.accordion.MDAccordionItem
#:import MDAccordionSubItem kivymd.accordion.MDAccordionSubItem
#:import MDThemePicker kivymd.theme_picker.MDThemePicker
#:import MDBottomNavigation kivymd.tabs.MDBottomNavigation
#:import MDBottomNavigationItem kivymd.tabs.MDBottomNavigationItem
NavigationLayout:
    id: nav_layout
    MDNavigationDrawer:
        id: nav_drawer
        NavigationDrawerToolbar:
            title: "Navigation"
        NavigationDrawerIconButton:
            icon: 'checkbox-blank-circle'
            text: "Main"
            on_release: app.root.ids.scr_mngr.current = 'main_page'
        NavigationDrawerIconButton:
            icon: 'checkbox-blank-circle'
            text: "Search"
            on_release: app.root.ids.scr_mngr.current = 'search'
        NavigationDrawerIconButton:
            icon: 'checkbox-blank-circle'
            text: "Recommend"
            on_release: app.root.ids.scr_mngr.current = 'recommend1'
        NavigationDrawerIconButton:
            icon: 'checkbox-blank-circle'
            text: "Faviourite recipe"
            on_release: app.root.ids.scr_mngr.current = 'fav'
    BoxLayout:
        orientation: 'vertical'
        ScreenManager:
            id: scr_mngr
            Screen:
                name: 'log_in'
                BoxLayout:
                    orientation: 'vertical'
                    Toolbar:
                        id: toolbar
                        title: 'Rexable'
                        md_bg_color: app.theme_cls.primary_color
                        background_palette: 'Primary'
                        background_hue: '500'
                        left_action_items: []
                        right_action_items: []
                    ScrollView:
                        do_scroll_y: False
                        BoxLayout:
                            orientation: 'vertical'
                            size_hint_y: None
                            height: self.minimum_height
                            padding: dp(48)
                            spacing: 30
                            MDTextField:
                                hint_text: "Username"
                                id:username
                            MDTextField:
                                hint_text: "Password"
                                id:password
                            MDRaisedButton:
                                text: "          Sign in          "
                                opposite_colors: True
                                size_hint: None, None
                                size: 4 * dp(32), dp(32)
                                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                                on_release: app.log_in()
                            MDRaisedButton:
                                text: "Create account"
                                opposite_colors: True
                                size_hint: None, None
                                size: 4 * dp(32), dp(32)
                                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                                on_release: app.change_screen('create_account')
            Screen:
                name: 'allergy'
                BoxLayout:
                    orientation: 'vertical'
                    Toolbar:
                        id: toolbar
                        title: 'Rexable'
                        md_bg_color: app.theme_cls.primary_color
                        background_palette: 'Primary'
                        background_hue: '500'
                        left_action_items: [['menu', lambda x: app.root.toggle_nav_drawer()]]
                        right_action_items: [['dots-vertical', lambda x: app.show_bottom_sheet()]]

                    ScrollView:
                        do_scroll_x: False
                        BoxLayout:
                            id:al
                            orientation: 'vertical'
                            size_hint_y: None
                            height: self.minimum_height
                            padding: dp(48)
                            spacing: 10    
                            OneLineAvatarIconListItem:
                                text: "alcohol-free"
                                RightCheckbox:
                            OneLineAvatarIconListItem:
                                text: "celery-free"
                                RightCheckbox:
                            OneLineAvatarIconListItem:
                                text: "crustacean-free"
                                RightCheckbox:
                            OneLineAvatarIconListItem:
                                text: "dairy-free"
                                RightCheckbox:
                            OneLineAvatarIconListItem:
                                text: "egg-free"
                                RightCheckbox:
                            OneLineAvatarIconListItem:
                                text: "fish-free"
                                RightCheckbox:
                            OneLineAvatarIconListItem:
                                text: "fodmap-free"
                                RightCheckbox:
                            OneLineAvatarIconListItem:
                                text: "gluten-free"
                                RightCheckbox:
                            OneLineAvatarIconListItem:
                                text: "lupine-free"
                                RightCheckbox:
                            OneLineAvatarIconListItem:
                                text: "mustard-free"
                                RightCheckbox:
                            OneLineAvatarIconListItem:
                                text: "peanut-free"
                                RightCheckbox:
                            OneLineAvatarIconListItem:
                                text: "red-meat-free"
                                RightCheckbox:
                            OneLineAvatarIconListItem:
                                text: "mustard-free"
                                RightCheckbox:
                            OneLineAvatarIconListItem:
                                text: "sesame-free"
                                RightCheckbox:
                            OneLineAvatarIconListItem:
                                text: "tree-nut-free"
                                RightCheckbox:
                            OneLineAvatarIconListItem:
                                text: "wheat-free"
                                RightCheckbox:
                    MDRaisedButton:
                        text: "Save"
                        opposite_colors: True
                        size_hint: None, None
                        size: 4 * dp(32), dp(32)
                        pos_hint: {'center_x': 0.5, 'center_y': 0.8}
                        on_release: app.save_al()

            Screen:
                name: 'get_bmi_data'
                BoxLayout:
                    orientation: 'vertical'
                    Toolbar:
                        id: toolbar
                        title: 'Rexable'
                        md_bg_color: app.theme_cls.primary_color
                        background_palette: 'Primary'
                        background_hue: '500'
                        left_action_items: [['menu', lambda x: app.root.toggle_nav_drawer()]]
                        right_action_items: [['dots-vertical', lambda x: app.show_bottom_sheet()]]

                    ScrollView:
                        do_scroll_x: False
                        BoxLayout:
                            orientation: 'vertical'
                            size_hint_y: None
                            height: self.minimum_height
                            padding: dp(48)
                            spacing: 10 

                            MDTextField:
                                hint_text: "Enter your age"
                                id:age_text
                            MDTextField:
                                hint_text: "Enter your height"
                                id:height_text
                            MDTextField:
                                hint_text: "Enter your weight"
                                id:weight_text                                

                            BoxLayout:
                                height: self.minimum_height
                                MDLabel:
                                    text_size: self.size
                                    text: "Gender"
                                MDCheckbox:
                                    id:            male
                                    group:        'gender'
                                    size_hint:    None, None
                                    size:        dp(48), dp(48)
                                    pos_hint:    {'center_x': 0.25, 'center_y': 0.5}
                                MDLabel:
                                    text: "Male"
                                MDCheckbox:
                                    group:        'gender'
                                    size_hint:    None, None
                                    size:        dp(48), dp(48)
                                    pos_hint:    {'center_x': 0.25, 'center_y': 0.5}
                                MDLabel:
                                    text: "Female"
                            MDLabel:
                            MDRaisedButton:
                                text: "next"
                                opposite_colors: True
                                size_hint: None, None
                                size: 4 * dp(32), dp(32)
                                pos_hint: {'center_x': 0.5, 'center_y': 1.5}
                                on_release: app.cal_bmi()

            Screen:
                name: 'main_page'
                BoxLayout:
                    orientation: 'vertical'
                    Toolbar:
                        id: toolbar
                        title: 'Rexable'
                        md_bg_color: app.theme_cls.primary_color
                        background_palette: 'Primary'
                        background_hue: '500'
                        left_action_items: [['menu', lambda x: app.root.toggle_nav_drawer()]]
                        right_action_items: [['dots-vertical', lambda x: app.show_bottom_sheet()]]
                    ScrollView:
                        do_scroll_x: False

                        BoxLayout:
                            orientation: 'vertical'
                            size_hint_y: None
                            height: self.minimum_height
                            MDLabel:
                                font_style: 'Display1'
                                theme_text_color: 'Primary'
                                text: "   "
                                halign: 'center'
                                size_hint_y: None
                                height: self.texture_size[1] + dp(4)
                            MDLabel:
                                font_style: 'Display1'
                                theme_text_color: 'Primary'
                                text: "BMI:"
                                halign: 'center'
                                size_hint_y: None
                                height: self.texture_size[1] + dp(4)
                            MDLabel:
                                id:bmi
                                font_style: 'Display1'
                                theme_text_color: 'Primary'
                                text: "1"
                                halign: 'center'
                                size_hint_y: None
                                height: self.texture_size[1] + dp(4)
                            MDLabel:
                                font_style: 'Display1'
                                theme_text_color: 'Primary'
                                text: "Health:"
                                halign: 'center'
                                size_hint_y: None
                                height: self.texture_size[1] + dp(4)
                            MDLabel:
                                id:health
                                font_style: 'Display1'
                                theme_text_color: 'Primary'
                                text: "   "
                                halign: 'center'
                                size_hint_y: None
                                height: self.texture_size[1] + dp(4)
                            MDLabel:
                                font_style: 'Display1'
                                theme_text_color: 'Primary'
                                text: "Healthy bmi range:"
                                halign: 'center'
                                size_hint_y: None
                                height: self.texture_size[1] + dp(4)
                            MDLabel:
                                id:health_bmi
                                font_style: 'Display1'
                                theme_text_color: 'Primary'
                                text: "1"
                                halign: 'center'
                                size_hint_y: None
                                height: self.texture_size[1] + dp(4)


            Screen:
                name: 'search'

                BoxLayout:
                    orientation: 'vertical'
                    Toolbar:
                        id: toolbar
                        title: 'Rexable'
                        md_bg_color: app.theme_cls.primary_color
                        background_palette: 'Primary'
                        background_hue: '500'
                        left_action_items: [['menu', lambda x: app.root.toggle_nav_drawer()]]
                        right_action_items: [['dots-vertical', lambda x: app.show_bottom_sheet()]]
                    BoxLayout:
                        height: self.minimum_height
                        spacing: 30
                        size_hint_y: None
                        height: self.minimum_height
                        padding: dp(20)
                        MDTextField:
                            hint_text: "Search some thing"
                            id:search_text
                        MDRaisedButton:
                            text: "Search"
                            opposite_colors: True
                            size_hint: None, None
                            size: 4 * dp(32), dp(32)
                            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                            on_release: app.search()
                    ScrollView:
                        do_scroll_x: False
                        GridLayout:
                            cols: 3
                            row_default_height: (self.width - self.cols*self.spacing[0])/self.cols
                            row_force_default: True
                            size_hint_y: None
                            height: self.minimum_height
                            padding: dp(4), dp(4)
                            spacing: dp(4)
                            id:gr
  

            Screen:
                name: 'create_account'
                BoxLayout:
                    orientation: 'vertical'
                    Toolbar:
                        id: toolbar
                        title: 'Rexable'
                        md_bg_color: app.theme_cls.primary_color
                        background_palette: 'Primary'
                        background_hue: '500'
                        left_action_items: [['arrow-left', lambda x:app.change_screen('log_in')]]
                        right_action_items: []
                    ScrollView:
                        do_scroll_y: False
                        BoxLayout:
                            orientation: 'vertical'
                            size_hint_y: None
                            height: self.minimum_height
                            padding: dp(48)
                            spacing: 30
                            MDTextField:
                                hint_text: "Username"
                                id:newusername
                            MDTextField:
                                hint_text: "Password"
                                id:newpassword
                            MDRaisedButton:
                                text: "Create account"
                                opposite_colors: True
                                size_hint: None, None
                                size: 4 * dp(32), dp(32)
                                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                                on_release: app.create_account()
            Screen:
                name: 'profile'
                BoxLayout:
                    orientation: 'vertical'
                    Toolbar:
                        id: toolbar
                        title: 'Rexable'
                        md_bg_color: app.theme_cls.primary_color
                        background_palette: 'Primary'
                        background_hue: '500'
                        left_action_items: [['arrow-left', lambda x:app.change_screen('log_in')]]
                        right_action_items: []
                    ScrollView:
                        do_scroll_y: False
                        BoxLayout:
                            orientation: 'vertical'
                            size_hint_y: None
                            height: self.minimum_height
                            padding: dp(48)
                            spacing: 30
                            MDRaisedButton:
                                text: "Manage Allergy"
                                opposite_colors: True
                                size_hint: None, None
                                size: 4 * dp(32), dp(32)
                                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                                on_release: app.change_screen('allergy')

            Screen:
                name: 'recommend1'
                BoxLayout:
                    orientation: 'vertical'
                    Toolbar:
                        id: toolbar
                        title: 'Rexable'
                        md_bg_color: app.theme_cls.primary_color
                        background_palette: 'Primary'
                        background_hue: '500'
                        left_action_items: [['menu', lambda x: app.root.toggle_nav_drawer()]]
                        right_action_items: [['dots-vertical', lambda x: app.show_bottom_sheet()]]
                    OneLineAvatarIconListItem:
                        text: "What you want to eat"
                    ScrollView:
                        do_scroll_x: False
                        BoxLayout:
                            id:reco1
                            orientation: 'vertical'
                            size_hint_y: None
                            height: self.minimum_height
                            padding: dp(48)
                            spacing: 10    

                            OneLineAvatarIconListItem:
                                text: "Proteins"
                                RightCheckbox:
                            OneLineAvatarIconListItem:
                                text: "Fruits"
                                RightCheckbox:
                            OneLineAvatarIconListItem:
                                text: "Vegetables"
                                RightCheckbox:
                            OneLineAvatarIconListItem:
                                text: "Snacks"
                                RightCheckbox:
                            OneLineAvatarIconListItem:
                                text: "Beverages"
                                RightCheckbox:
                    MDRaisedButton:
                        text: "next"
                        opposite_colors: True
                        size_hint: None, None
                        size: 4 * dp(32), dp(32)
                        pos_hint: {'center_x': 0.5, 'center_y': 0.8}
                        on_release: app.recommend1()

            Screen:
                name: 'recommend2'
                BoxLayout:
                    orientation: 'vertical'
                    Toolbar:
                        id: toolbar
                        title: 'Rexable'
                        md_bg_color: app.theme_cls.primary_color
                        background_palette: 'Primary'
                        background_hue: '500'
                        left_action_items: [['menu', lambda x: app.root.toggle_nav_drawer()]]
                        right_action_items: [['dots-vertical', lambda x: app.show_bottom_sheet()]]
                    OneLineAvatarIconListItem:
                        text: "What you want to eat(max 3)"
                    ScrollView:
                        do_scroll_x: False
                        BoxLayout:
                            id:reco2
                            orientation: 'vertical'
                            size_hint_y: None
                            height: self.minimum_height
                            padding: dp(48)
                            spacing: 10    


                    MDRaisedButton:
                        text: "next"
                        opposite_colors: True
                        size_hint: None, None
                        size: 4 * dp(32), dp(32)
                        pos_hint: {'center_x': 0.5, 'center_y': 0.8}
                        on_release: app.recommend2()
            Screen:
                name: 'recommend3'

                BoxLayout:
                    orientation: 'vertical'
                    Toolbar:
                        id: toolbar
                        title: 'Rexable'
                        md_bg_color: app.theme_cls.primary_color
                        background_palette: 'Primary'
                        background_hue: '500'
                        left_action_items: [['menu', lambda x: app.root.toggle_nav_drawer()]]
                        right_action_items: [['dots-vertical', lambda x: app.show_bottom_sheet()]]
                    ScrollView:
                        do_scroll_x: False
                        GridLayout:
                            cols: 3
                            row_default_height: (self.width - self.cols*self.spacing[0])/self.cols
                            row_force_default: True
                            size_hint_y: None
                            height: self.minimum_height
                            padding: dp(4), dp(4)
                            spacing: dp(4)
                            id:reco3
            Screen:
                name: 'fav'

                BoxLayout:
                    orientation: 'vertical'
                    Toolbar:
                        id: toolbar
                        title: 'Rexable'
                        md_bg_color: app.theme_cls.primary_color
                        background_palette: 'Primary'
                        background_hue: '500'
                        left_action_items: [['menu', lambda x: app.root.toggle_nav_drawer()]]
                        right_action_items: [['dots-vertical', lambda x: app.show_bottom_sheet()]]
                    ScrollView:
                        do_scroll_x: False
                        GridLayout:
                            cols: 3
                            row_default_height: (self.width - self.cols*self.spacing[0])/self.cols
                            row_force_default: True
                            size_hint_y: None
                            height: self.minimum_height
                            padding: dp(4), dp(4)
                            spacing: dp(4)
                            id:fav

<SearchTile>
    mipmap: True
    on_release: app.show_search_result(self.text,self.ty)
    ty:''
<CheckboxList>
    RightCheckbox:


''' 

class Rexable(App):
    theme_cls = ThemeManager()
    previous_date = ObjectProperty()
    title = "Rexable"



    def build(self):
        self.logged_in = False
        self.data_dir = self.user_data_dir
        self.store = JsonStore('app_storage.json')
        self.user_login = ["", ""]
        self.allergies = []
        self.allergies_dict = {}
        self.fav = []
        main_widget = Builder.load_string(main_widget_kv)


        return main_widget


    def show_bottom_sheet(self):
        bs = MDListBottomSheet()
        bs.add_item("Profile", lambda x: self.change_screen('profile'),
                    icon='account')
        bs.add_item("Log out", lambda x: self.log_out(), icon='account-off')
        bs.open()

    def change_screen(self,dire):
        self.root.ids.scr_mngr.current = dire


    def on_pause(self):
        return True

    def on_stop(self):
        pass

    def log_in(self):
        self.username = self.root.ids.username.text
        self.password = self.root.ids.password.text       
        content = MDLabel(font_style='Body1',
                          theme_text_color='Secondary',
                          text="Try again",
                          size_hint_y=None,
                          valign='top')
        content.bind(texture_size=content.setter('size'))
        dialog = MDDialog(title="Wrong username or password",
                               content=content,
                               size_hint=(.8, None),
                               height=dp(200),
                               auto_dismiss=False)

        dialog.add_action_button("Dismiss",
                                      action=lambda *x: dialog.dismiss())      
        try:
            self.db = userCollect.find_one({"username": self.username})
            if self.db == None:
               dialog.open()  
            elif self.db["password"] == self.password:
                #this is just a preliminary password/username system; will add hashing and encryption later
                self.store.put('credentials', username = self.username, password = self.password)
                print(self.db['allergies_dict'])
                for child in self.root.ids.al.children:
                    if self.db['allergies_dict'][child.text]:
                        child.ids['_right_container'].children[0].active = True
                self.root.ids.bmi.text = self.db['bmi']
                self.root.ids.health.text = self.db['health']
                self.root.ids.health_bmi.text = self.db['healthy_bmi_range']
                self.fav = self.db['favourite_recipe']
                for i in self.fav:
                    self.root.ids.fav.add_widget(SearchTile(source=i['image_link'], text = i['recipe_name'],ty = 'fav'))
                self.change_screen('main_page')
            else:
                dialog.open()  
        except errors.CollectionInvalid:
            dialog.open()  
 
    def log_out(self):
        self.store.put('credentials', username = "", password = "")
        self.change_screen('log_in')
 
    def create_account(self):
        username = self.root.ids.newusername.text
        password = self.root.ids.newpassword.text
        if userCollect != None:
           the_dict = {"username": username, "password": password,"allergies_dict": {},'bmi':'','health':'','healthy_bmi_range':'','favourite_recipe':[]}

           # "cookingTime": self.cooking_time, "viewedRecipes": dict()}
           userCollect.insert_one(the_dict)
        self.store.put('credentials', username = username, password = password)
        self.username = username
        self.password = password
        # self.change_screen("main_page")
        self.change_screen("get_bmi_data")

    def show_search_result(self,recipe_name,ty):
        recipe_name = recipe_name
        content = MDLabel(font_style='Body1',
          theme_text_color='Secondary',
          text=self.result_text(recipe_name,ty),
          size_hint_y=None,
          valign='top')
        content.bind(texture_size=content.setter('size'))
        dialog = MDDialog(title=recipe_name,
                               content=content,
                               size_hint=(.8, None),
                               height=dp(400),
                               auto_dismiss=False)

        if ty != 'fav':
            dialog.add_action_button("Add to favourite",action=lambda x: [self.add_fav(recipe_name,ty),dialog.dismiss()]) 
        dialog.add_action_button("close",action=lambda x: dialog.dismiss()) 
        dialog.open()

    def result_text(self,recipe_name,ty):
        item = {}
        result = 'Calories \n'
        if ty == 'search':
            item = [i for i in self.search_result if recipe_name == i['recipe_name']][0]
        elif ty == 'recommend':
            item = [i for i in self.recommend_result if recipe_name == i['recipe_name']][0]
        elif ty == 'fav':
            item = [i for i in self.fav if recipe_name == i['recipe_name']][0]
        result += '\n\n'
        result += item['calories']
        result += 'Ingredient \n'
        for u in item['ingredient']:
            result += (u+'\n')
        # print(item)
        # print(webscrape_recipe(item['url']),item['url'])
        return result       

    def add_fav(self,recipe_name,ty):
        result = []
        if ty == 'search':
            result = [i for i in self.search_result if recipe_name == i['recipe_name']]
        elif ty == 'recommend':
            result += [i for i in self.recommend_result if recipe_name == i['recipe_name']]
        self.fav += result
        self.root.ids.fav.add_widget(SearchTile(source=result[0]['image_link'], text = result[0]['recipe_name'],ty = 'fav'))
        res = userCollect.update_one({"username": self.username}, {"$set": {"favourite_recipe": self.fav}})
        

    def search(self):
        data = []
        self.search_result = []
        self.search_result = search(self.root.ids.search_text.text,self.allergies)
        self.root.ids.gr.clear_widgets()

        for i in range(len(self.search_result)):
            self.root.ids.gr.add_widget(SearchTile(source=self.search_result[i]['image_link'], text = self.search_result[i]['recipe_name'], ty = 'search'))


    def save_al(self):
        self.allergies = []
        self.allergies_dict = {}
        for child in self.root.ids.al.children:
            if (child.ids['_right_container'].children[0].active):
                self.allergies_dict[child.text] = True
                self.allergies.append(child.text)
            else:
                self.allergies_dict[child.text] = False

        res = userCollect.update_one({"username": self.username}, {"$set": {"allergies_dict": self.allergies_dict}})

        self.change_screen('main_page')

    def cal_bmi(self):
        result = get_bmi(self.root.ids.age_text.text,self.root.ids.weight_text.text,self.root.ids.height_text.text,True if self.root.ids.male.active else False)
        self.root.ids.bmi.text = str(result[0]['bmi'])[:5]
        self.root.ids.health.text = result[0]['health']
        self.root.ids.health_bmi.text = result[0]['healthy_bmi_range']
        res = userCollect.update_one({"username": self.username}, {"$set": {"bmi": str(result[0]['bmi'])[:5]}})
        res = userCollect.update_one({"username": self.username}, {"$set": {"health": result[0]['health']}})
        res = userCollect.update_one({"username": self.username}, {"$set": {"healthy_bmi_range": result[0]['healthy_bmi_range']}})             
        self.change_screen('allergy')

    def recommend1(self):
        self.food = []
        for child in self.root.ids.reco1.children:
            if (child.ids['_right_container'].children[0].active):
                self.food.append(child.text)

        self.foodlist = []
        _food_data = food_data()
        for i in _food_data:
            if i in self.food:
                self.foodlist += _food_data[i]
        self.root.ids.reco2.clear_widgets()

        for i in range(len(self.foodlist)):
            self.root.ids.reco2.add_widget(CheckboxList(text = self.foodlist[i]))
        self.change_screen('recommend2')

    def recommend2(self):        
        self.recommend_result = []
        self.food_search = []
        self.root.ids.reco3.clear_widgets()
        for child in self.root.ids.reco2.children:
            if (child.ids['_right_container'].children[0].active):
                self.food_search.append(child.text)
        for text in self.food_search:
            self.recommend_result += search(text,self.allergies,3)
        for i in range(len(self.recommend_result)):
            self.root.ids.reco3.add_widget(SearchTile(source=self.recommend_result[i]['image_link'], text = self.recommend_result[i]['recipe_name'],ty = 'recommend'))
        self.change_screen('recommend3')

class SearchTile(SmartTileWithLabel):
    ty = StringProperty()
class RightCheckbox(IRightBodyTouch, MDCheckbox):
    pass
class CheckboxList(OneLineAvatarIconListItem):
    pass


if __name__ == '__main__':
    # x = userCollect.delete_many({})
    Rexable().run()