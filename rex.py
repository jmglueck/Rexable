# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.image import Image

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
from basic_search import search
from kivy.uix.image import AsyncImage

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
            text: "Toolbars"
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
                            MDTextField:
                                hint_text: "Password"
                            MDRaisedButton:
                                text: "          Sign in          "
                                opposite_colors: True
                                size_hint: None, None
                                size: 4 * dp(32), dp(32)
                                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                                on_release: app.root.ids.scr_mngr.current = 'search'
                            MDRaisedButton:
                                text: "Create account"
                                opposite_colors: True
                                size_hint: None, None
                                size: 4 * dp(32), dp(32)
                                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                                on_release: app.root.ids.scr_mngr.current = 'create_account'
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
                 
                    RecycleView:
                        id: rv
                        key_viewclass: 'viewclass'
                        key_size: 'height'

                        RecycleBoxLayout:
                            padding: dp(12)
                            default_size: None, dp(48)
                            default_size_hint: 2, None
                            size_hint_y: None
                            height: self.minimum_height
                            orientation: 'vertical'
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
                            MDTextField:
                                hint_text: "Password"
                            MDRaisedButton:
                                text: "Create account"
                                opposite_colors: True
                                size_hint: None, None
                                size: 4 * dp(32), dp(32)
                                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                                on_release: app.create_account()
''' 

class Rexable(App):
    theme_cls = ThemeManager()
    previous_date = ObjectProperty()
    title = "Rexable"



    def build(self):
        main_widget = Builder.load_string(main_widget_kv)


        return main_widget



    def show_example_snackbar(self, snack_type):
        if snack_type == 'simple':
            Snackbar(text="This is a snackbar!").show()
        elif snack_type == 'button':
            Snackbar(text="This is a snackbar", button_text="with a button!", button_callback=lambda *args: 2).show()
        elif snack_type == 'verylong':
            Snackbar(text="This is a very very very very very very very long snackbar!").show()

    def show_example_dialog(self):
        content = MDLabel(font_style='Body1',
                          theme_text_color='Secondary',
                          text="This is a dialog with a title and some text. "
                               "That's pretty awesome right!",
                          size_hint_y=None,
                          valign='top')
        content.bind(texture_size=content.setter('size'))
        self.dialog = MDDialog(title="This is a test dialog",
                               content=content,
                               size_hint=(.8, None),
                               height=dp(200),
                               auto_dismiss=False)

        self.dialog.add_action_button("Dismiss",
                                      action=lambda *x: self.dialog.dismiss())
        self.dialog.open()


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
    def log_out(self):
        self.change_screen('log_in')
    def create_account(self):
        self.change_screen('log_in')
    def search(self):
        data = []
        result = search(self.root.ids.search_text.text)
        for i in range(len(result)):
            item = {'viewclass':'ThreeLineAvatarIconListItem','text':'','secondary_text':''}
            item['text']=result[i]['recipe_name']
            item['secondary_text']=result[i]['calories']
            item['ImageLeftWidget']={'source':result[i]['image_link']}
            data.append(item)
        self.root.ids.rv.data = data




if __name__ == '__main__':
    Rexable().run()
