# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.storage.jsonstore import JsonStore
from kivy.uix.image import AsyncImage

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

from basic_search import search


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
            on_release: app.root.ids.scr_mngr.current = 'main_screen'
        NavigationDrawerIconButton:
            icon: 'checkbox-blank-circle'
            text: "Search"
            on_release: app.root.ids.scr_mngr.current = 'search'

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
                            left_action_items: []
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
                name: 'main_screen'
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
                 
                    RecycleView:
                        id: rv
                        key_viewclass: 'viewclass'
                        key_size: 'height'

                        RecycleGridLayout:
                            cols: 3
                            row_default_height: (self.width - self.cols*self.spacing[0])/self.cols
                            row_force_default: True
                            size_hint_y: None
                            height: self.minimum_height
                            padding: dp(4), dp(4)
                            spacing: dp(4)
            Screen:
                name: 'search'
                MDSpinner:
                    id: spinner
                    size_hint: None, None
                    size: dp(46), dp(46)
                    pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                    active: True
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
                        

                    RecycleView:
                        id: rv
                        key_viewclass: 'viewclass'
                        key_size: 'height'

                        RecycleGridLayout:
                            cols: 3
                            row_default_height: (self.width - self.cols*self.spacing[0])/self.cols
                            row_force_default: True
                            size_hint_y: None
                            height: self.minimum_height
                            padding: dp(4), dp(4)
                            spacing: dp(4)
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
                            left_action_items: []
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


<SearchTile>
    on_release: app.show_search_result(self.text)
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
        main_widget = Builder.load_string(main_widget_kv)
        return main_widget


    def show_bottom_sheet(self):
        bs = MDListBottomSheet()
        bs.add_item("Profile", lambda x: x,
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
            results = userCollect.find_one({"username": self.username})
            if results == None:
               dialog.open()  
            elif results["password"] == self.password:
                #this is just a preliminary password/username system; will add hashing and encryption later
                self.store.put('credentials', username = self.username, password = self.password)
                self.change_screen('search')
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
           the_dict = {"username": username, "password": password}

           # "allergies": self.allergies,
           # "cookingTime": self.cooking_time, "viewedRecipes": dict()}
           userCollect.insert_one(the_dict)
        self.store.put('credentials', username = username, password = password)
        self.change_screen("main_screen")

    def show_search_result(self,recipe_name):
        recipe_name = recipe_name
        content = MDLabel(font_style='Body1',
          theme_text_color='Secondary',
          text="Add later",
          size_hint_y=None,
          valign='top')
        content.bind(texture_size=content.setter('size'))
        dialog = MDDialog(title=recipe_name,
                               content=content,
                               size_hint=(.8, None),
                               height=dp(200),
                               auto_dismiss=False)

        dialog.add_action_button("Add to favourite",action=lambda x: dialog.dismiss()) 
        dialog.add_action_button("close",action=lambda x: dialog.dismiss()) 
        dialog.open()

    def search(self):
        data = []
        result = search(self.root.ids.search_text.text)
        self.root.ids.spiner.active = False
        for i in range(len(result)):
            item = {'viewclass':'SearchTile'}
            item['mipmap']=True
            item['text']=result[i]['recipe_name']
            item['source']=result[i]['image_link']
            data.append(item)
        self.root.ids.rv.data = data

class SearchTile(SmartTileWithLabel):
    pass


if __name__ == '__main__':
    Rexable().run()
