from abc import ABC, abstractmethod
from kivy.metrics import dp
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
import psycopg2
from kivymd.uix.button import MDFillRoundFlatButton, MDRaisedButton
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.dialog import MDDialog
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast


class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    pass


class Cart(Screen, Widget):

    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        Widget.__init__(self, **kwargs)

    def open_table(self):
        data_tables = MDDataTable(
            size_hint=(0.5, 0.5),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            check=True,
            rows_num=10,
            column_data=[
                ("Name", dp(70)),
                ("Type", dp(30)),
                ("price", dp(30)),
            ],
            row_data=[
                ("House of gucci", "Crime", "11$"),
                ("Girls on buy", "Drama", "13$"),
                ("resident_evil", "Horror", "18$"),
                ("dune", "Sci-fi", "7$"),
                ("Eternals", "Action", "12.1$")
            ],
        )
        data_tables.bind(on_check_press=self.checked)
        data_tables.bind(on_row_press=self.row_checked)
        data_tables.ids.container.add_widget(
            Widget(size_hint_y=None, height="5dp")
        )
        data_tables.ids.container.add_widget(
            MDRaisedButton(
                text="CLOSE",
                pos_hint={"right": 1},
                on_release=lambda x: self.remove_widget(data_tables),
            )
        )
        self.add_widget(data_tables)

    # Function for check presses
    def checked(self, instance_table, current_row):
        print(instance_table, current_row)

    # Function for row presses
    def row_checked(self, instance_table, instance_row):
        print(instance_table, instance_row)

    connector = psycopg2.connect(
        host="ec2-54-204-128-96.compute-1.amazonaws.com",
        database="d6pe5ebhna25ge",
        user="lrgsxikpfzffcy",
        password="611d90eca150eaabe8d0f37910400dcb1aefae46da685e024c266d6c498f038f",
        port="5432"
    )
    pass


class Latest(Screen, Widget):
    pass


class MainScreen(Screen, Widget):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        Widget.__init__(self, **kwargs)


class CreateAccScreen(Screen, Widget):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        Widget.__init__(self, **kwargs)

    dialog = None

    def show_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                text="invalid Email adress",
                button=MDFillRoundFlatButton(text="ok", pos_hint={"center_x": 0.5, "bottom": 0.9}))
        self.dialog.open()

    def create(self):
        connector = psycopg2.connect(
            host="ec2-54-204-128-96.compute-1.amazonaws.com",
            database="d6pe5ebhna25ge",
            user="lrgsxikpfzffcy",
            password="611d90eca150eaabe8d0f37910400dcb1aefae46da685e024c266d6c498f038f",
            port="5432"
        )
        # create cursor
        username = self.ids.create_username.text
        password = self.ids.create_password.text
        email = self.ids.create_email.text
        cursor = connector.cursor()

        if "@" and "." not in email:
            # connector.commit()
            connector.close()
            return False
        else:
            cursor.execute("INSERT INTO Users ( username, email, password) VALUES(%s, %s, %s)",
                           (username, email, password))

            connector.commit()
            connector.close()
        return True

    def clear(self):
        self.ids.create_username.text = ""
        self.ids.create_password.text = ""
        self.ids.create_email.text = ""


class LoginScreen(Screen, Widget):
    textinput = ObjectProperty(None)

    def __init__(self, **kwargs):
        Widget.__init__(self, **kwargs)
        Screen.__init__(self, **kwargs)

    def on_press_cancel(self):

        pass

    def login(self):

        email = self.ids.email.text
        password = self.ids.password.text
        connector = psycopg2.connect(
            host="ec2-54-204-128-96.compute-1.amazonaws.com",
            database="d6pe5ebhna25ge",
            user="lrgsxikpfzffcy",
            password="611d90eca150eaabe8d0f37910400dcb1aefae46da685e024c266d6c498f038f",
            port="5432"
        )
        cursor = connector.cursor()
        cursor.execute(f"SELECT email,password FROM Users WHERE email='{email}' AND password ='{password}'")

        validate = cursor.fetchone()

        print(validate)
        if validate is None:
            return False
        else:
            return True

        # print(validate)
        # for rows in validate:
        #     if validate == (email,password):
        #         print("dziala")
        #     else:
        #         print("nie działa")

    def visiblity(self):
        if self.textinput.password == True:
            self.textinput.password = False
        elif self.textinput.password == False:
            self.textinput.password = True


class FilmLaboratory(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.manager_open = False
        self.file_manager = MDFileManager(exit_manager=self.exit_manager, select_path=self.select_path)

    def build(self):
        self.icon = "beztla.png"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.primary_hue = "800"
        self.theme_cls.accent_palette = "Red"
        self.theme_cls.accent_hue = "500"

    connector = psycopg2.connect(
        host="ec2-54-204-128-96.compute-1.amazonaws.com",
        database="d6pe5ebhna25ge",
        user="lrgsxikpfzffcy",
        password="611d90eca150eaabe8d0f37910400dcb1aefae46da685e024c266d6c498f038f",
        port="5432"
    )
    cursor = connector.cursor()

    cursor.execute("""CREATE TABLE if not exists Users
                       (username TEXT,
                        email TEXT,
                        password TEXT);
                          """)
    connector.commit()
    # do zobaczenia jakie sa kolumny
    cursor.execute("SELECT * FROM Users")
    print(cursor.description)
    # do zobaczenia rekordów
    records = cursor.fetchall()
    print(records)

    def on_switch_active(self, checkbox, value):
        if value:
            self.theme_cls.theme_style = "Light"
        else:
            self.theme_cls.theme_style = "Dark"

    def file_manager_open(self):
        self.file_manager.show("C:\\")  # output manager to the screen
        self.manager_open = True

    def select_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        '''

        self.exit_manager()
        toast(path)

    def exit_manager(self, *args):
        """Called when the user reaches the root of the directory tree."""

        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device..'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True


if __name__ == '__main__':
    FilmLaboratory().run()
