from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivymd.uix.bottomsheet import MDBottomSheet
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFillRoundFlatButton, MDIconButton, MDRoundFlatButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList, OneLineListItem


class CalculatorScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.history_data = []

        main_layout = MDBoxLayout(
            orientation="vertical",
            padding="10dp",
            spacing="10dp",
        )

        self.display = MDLabel(
            text="0",
            halign="right",
            valign="center",
            font_style="H3",
            theme_text_color="Custom",
            text_color=[0, 0, 0, 1],
            size_hint_y=0.25,
        )
        self.display.bind(size=self.display.setter("text_size"))
        main_layout.add_widget(self.display)

        buttons_grid = MDGridLayout(cols=4, spacing="10dp", size_hint_y=0.75)

        buttons = [
            ("C", self.clear),
            ("%", self.press_button),
            ("/", self.press_button),
            ("*", self.press_button),
            ("7", self.press_button),
            ("8", self.press_button),
            ("9", self.press_button),
            ("-", self.press_button),
            ("4", self.press_button),
            ("5", self.press_button),
            ("6", self.press_button),
            ("+", self.press_button),
            ("1", self.press_button),
            ("2", self.press_button),
            ("3", self.press_button),
            (".", self.press_button),
            ("0", self.press_button),
            ("H", self.open_history),
            ("D", self.delete_one),
            ("=", self.calculate),
        ]

        for text, command in buttons:
            if text == "H":
                btn = MDIconButton(
                    icon="history",
                    size_hint=(1, 1),
                    theme_text_color="Custom",
                    text_color=[0, 0.5, 0.8, 1],
                )
                btn.bind(on_release=command)
                buttons_grid.add_widget(btn)
            elif text == "=":
                btn = MDFillRoundFlatButton(
                    text=text, md_bg_color=[0.5, 0.5, 0.5, 1], size_hint=(1, 1)
                )
                btn.bind(on_release=command)
                buttons_grid.add_widget(btn)
            elif text == "C":
                btn = MDRoundFlatButton(
                    text=text, md_bg_color=[1, 0.3, 0.3, 1], size_hint=(1, 1)
                )
                btn.bind(on_release=command)
                buttons_grid.add_widget(btn)
            elif text == "D":
                btn = MDRoundFlatButton(
                    text=text,
                    size_hint=(1, 1),
                    text_color=[1, 0.5, 0, 1],
                    line_color=[1, 0.5, 0, 1],
                )
                btn.bind(on_release=command)
                buttons_grid.add_widget(btn)
            else:
                btn = MDRoundFlatButton(
                    text=text,
                    size_hint=(1, 1),
                    text_color=[0, 0, 0, 1],
                    line_color=[0.5, 0.5, 0.5, 1],
                )
                btn.bind(on_release=command)
                buttons_grid.add_widget(btn)

        main_layout.add_widget(buttons_grid)
        self.add_widget(main_layout)

        self.bottom_sheet = None

    def press_button(self, button_instance):
        char = button_instance.text
        if self.display.text == "0" and char != ".":
            self.display.text = char
        else:
            self.display.text += char

    def clear(self, button_instance):
        self.display.text = "0"
        self.history_data.clear()

    def delete_one(self, button_instance):
        current_text = self.display.text
        if len(current_text) <= 1 or current_text == "Error":
            self.display.text = "0"
        else:
            self.display.text = current_text[:-1]

    def calculate(self, button_instance):
        expr = self.display.text
        if expr == "0" or expr == "Error":
            return

        if "%" in expr:
            expr = expr.replace("%", "*0.01")

        try:
            result = str(eval(expr))
            if result.endswith(".0"):
                result = result[:-2]

            self.history_data.append(f"{self.display.text} = {result}")
            self.display.text = result
        except Exception:
            self.display.text = "Error"

    def open_history(self, button_instance):
        self.bottom_sheet = MDBottomSheet(size_hint_y=0.45)
        bottom_sheet_layout = MDBoxLayout(orientation="vertical", padding="10dp")
        scroll = ScrollView()
        self.history_list = MDList()

        if not self.history_data:
            self.history_list.add_widget(
                OneLineListItem(text="History is empty")
            )
        else:
            for operation in reversed(self.history_data):
                item = OneLineListItem(text=operation)
                item.bind(on_release=self.recover_result)
                self.history_list.add_widget(item)

        scroll.add_widget(self.history_list)
        bottom_sheet_layout.add_widget(scroll)
        self.bottom_sheet.add_widget(bottom_sheet_layout)
        self.bottom_sheet.open()

    def recover_result(self, item_instance):
        try:
            result = item_instance.text.split(" = ")[1]
            self.display.text = result
        except IndexError:
            pass
        finally:
            if self.bottom_sheet:
                self.bottom_sheet.dismiss()


class CalculatorApp(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Light"
        screen_manager = ScreenManager()
        screen_manager.add_widget(CalculatorScreen(name="calculator"))
        return screen_manager


if __name__ == "__main__":
    CalculatorApp().run()