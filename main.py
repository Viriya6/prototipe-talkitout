import kivy
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, RoundedRectangle
from kivy.clock import Clock
from kivy.animation import Animation
import json
fonts = "assets/font/andalemono.ttf"

# Window.size = (450, 800)  # Set the window size
Window.size = (360, 640)

class LoginPage(FloatLayout):
    def __init__(self, switch_to_signup, switch_to_home, home_page, **kwargs):
        super().__init__(**kwargs)
        self.switch_to_signup = switch_to_signup
        self.switch_to_home = switch_to_home
        self.home_page = home_page

        # Add background image
        self.add_widget(Image(source="assets/background.jpg", allow_stretch=True, keep_ratio=False))
        self.add_widget(Image(source="assets/logo.png", size_hint=(0.55, 0.55), pos_hint={"x": 0, "y": 0.68}))
        self.add_widget(Image(source="assets/logo_td.png", size_hint=(0.13, 0.13), pos_hint={"x": 0.8, "y": 0.88}))

        # Sliding Header (Images)
        self.header_images = [
            "assets/header/header1.jpg",
            "assets/header/header2.png",
            "assets/header/header3.jpg"
        ]
        self.current_header_index = 0
        self.header_image = Image(
            source=self.header_images[self.current_header_index],
            size_hint=(1, 0.3),
            pos_hint={"x": 0, "y": 0.611}
        )
        self.add_widget(self.header_image)

        # Schedule the header to slide every 3 seconds
        Clock.schedule_interval(self.slide_header, 5)

        with self.canvas:
            Color(0.23, 0.5, 1.10, 0.5)  # Set color (RGBA)
            RoundedRectangle(pos=(50, 50), size=(350, 500), radius=[20])  # Rounded rectangle

        # Username
        self.add_widget(Label(text="Username:", font_name=fonts , size_hint=(0.3, 0.1), pos_hint={"x": 0.12, "y": 0.48}))
        self.username_input = TextInput(hint_text="Enter Username" , font_name=fonts,size_hint=(0.65, 0.05), pos_hint={"x": 0.17, "y": 0.46})
        self.add_widget(self.username_input)

        # Password
        self.add_widget(Label(text="Password:", font_name=fonts, size_hint=(0.3, 0.1), pos_hint={"x": 0.12, "y": 0.36}))
        self.password_input = TextInput(hint_text="Enter Password", font_name=fonts, password=True, size_hint=(0.65, 0.05), pos_hint={"x": 0.17, "y": 0.34})
        self.add_widget(self.password_input)

        # error input
        self.error_label = Label(text="", color=(1, 0, 0, 1), size_hint=(0.6, 0.05), pos_hint={"x": 0.15, "y": 0.3})
        self.add_widget(self.error_label)

        # Login Button
        self.login_button = Button(size_hint=(0.26, 0.13), pos_hint={"x": 0.52, "y": 0.12}, background_normal="assets/home_button.png")
        self.login_button.bind(on_press=self.login)
        self.add_widget(self.login_button)

        # Sign Up Button
        self.signup_button = Button(size_hint=(0.26, 0.13), pos_hint={"x": 0.22, "y": 0.12}, background_normal="assets/signup_button.png")
        self.signup_button.bind(on_press=self.switch_to_signup)
        self.add_widget(self.signup_button)

    def slide_header(self, dt):
        # Animate the current header sliding out
        anim_out = Animation(pos_hint={"x": -1, "y": 0.611}, duration=0.2)
        anim_out.bind(on_complete=self.update_header)
        anim_out.start(self.header_image)

    def update_header(self, *args):
        # Update the header image and reset its position
        self.current_header_index = (self.current_header_index + 1) % len(self.header_images)
        self.header_image.source = self.header_images[self.current_header_index]
        self.header_image.pos_hint = {"x": 1, "y": 0.611}

        # Animate the new header sliding in
        anim_in = Animation(pos_hint={"x": 0, "y": 0.611}, duration=0.2)
        anim_in.start(self.header_image)

    def login(self, instance):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()

        self.error_label.text = ""

        if not username or not password:
            self.error_label.text = "Invalid username or password!"
            return

        # Load user data from file
        try:
            with open("users.json", "r") as file:
                users = json.load(file)
        except FileNotFoundError:
            self.error_label.text = "No users found. Please sign up first."
            return
        except json.JSONDecodeError:
            self.error_label.text = "Error reading user data. Please try again later."
            return

        # Validate credentials
        if username in users and users[username]["password"] == password:
            print(f"Login successful! Welcome, {username}.")
            self.home_page.update_welcome_message(username)  # Update the welcome message
            self.switch_to_home()  # Navigate to the home page
        else:
            self.error_label.text = "Invalid username or password!"

        # Clear input fields
        self.username_input.text = ""
        self.password_input.text = ""


class SignUpPage(FloatLayout):
    def __init__(self, switch_to_home, switch_to_login, **kwargs):
        super().__init__(**kwargs)
        self.switch_to_home = switch_to_home
        self.switch_to_login = switch_to_login

        # Add background image
        self.add_widget(Image(source="assets/background.jpg", allow_stretch=True, keep_ratio=False))
        self.add_widget(Image(source="assets/logo.png", size_hint=(0.55, 0.55), pos_hint={"x": 0, "y": 0.68}))
        self.add_widget(Image(source="assets/logo_td.png", size_hint=(0.13, 0.13), pos_hint={"x": 0.8, "y": 0.88}))

        # Sliding Header (Images)
        self.header_images = [
            "assets/header/header1.jpg",
            "assets/header/header2.png",
            "assets/header/header3.jpg"
        ]
        self.current_header_index = 0
        self.header_image = Image(
            source=self.header_images[self.current_header_index],
            size_hint=(1, 0.3),
            pos_hint={"x": 0, "y": 0.611}
        )
        self.add_widget(self.header_image)

        # Schedule the header to slide every 3 seconds
        Clock.schedule_interval(self.slide_header, 5)

        with self.canvas:
            Color(0.23, 0.5, 1.10, 0.5)  # Set color (RGBA)
            RoundedRectangle(pos=(50, 50), size=(350, 500), radius=[20])  # Rounded rectangle

        # Username
        self.add_widget(Label(text="Username:", font_name=fonts, size_hint=(0.3, 0.1), pos_hint={"x": 0.1, "y": 0.55}))
        self.username_input = TextInput(hint_text="Input username", font_name=fonts, size_hint=(0.65, 0.05), pos_hint={"x": 0.17, "y": 0.53})
        self.add_widget(self.username_input)

        self.username_error_label = Label(text="", font_name=fonts, color=(1, 0, 0, 1), size_hint=(0.6, 0.05), pos_hint={"x": 0.12, "y": 0.49})
        self.add_widget(self.username_error_label)

        # Email
        self.add_widget(Label(text="Email:", font_name=fonts, size_hint=(0.3, 0.1), pos_hint={"x": 0.06, "y": 0.44}))
        self.email_input = TextInput(hint_text="Input Email", size_hint=(0.65, 0.05), font_name=fonts, pos_hint={"x": 0.17, "y": 0.42})
        self.add_widget(self.email_input)

        self.email_error_label = Label(text="", font_name=fonts, color=(1, 0, 0, 1), size_hint=(0.6, 0.05), pos_hint={"x": 0.12, "y": 0.38})
        self.add_widget(self.email_error_label)

        # Password
        self.add_widget(Label(text="Password:", font_name=fonts, size_hint=(0.3, 0.1), pos_hint={"x": 0.1, "y": 0.32}))
        self.password_input = TextInput(hint_text="Input password", password=True, size_hint=(0.65, 0.05), pos_hint={"x": 0.17, "y": 0.299})
        self.add_widget(self.password_input)

        self.password_error_label = Label(text="", font_name=fonts, color=(1, 0, 0, 1), size_hint=(0.6, 0.05), pos_hint={"x": 0.19, "y": 0.26})
        self.add_widget(self.password_error_label)

        # Birthdate Label
        self.add_widget(Label(text="Birthdate:", font_name=fonts, size_hint=(0.3, 0.12), pos_hint={"x": 0.1, "y": 0.2}))

        # Birthdate Inputs (Month, Day, Year)
        self.birth_month = TextInput(hint_text="month", font_name=fonts, size_hint=(0.2, 0.05), pos_hint={"x": 0.17, "y": 0.19})
        self.add_widget(self.birth_month)

        self.birth_day = TextInput(hint_text="day", font_name=fonts, size_hint=(0.2, 0.05), pos_hint={"x": 0.4, "y": 0.19})
        self.add_widget(self.birth_day)

        self.birth_year = TextInput(hint_text="year", font_name=fonts, size_hint=(0.2, 0.05), pos_hint={"x": 0.63, "y": 0.19})
        self.add_widget(self.birth_year)

        self.error_birthdate_label = Label(text="", font_name=fonts, color=(1, 0, 0, 1), size_hint=(0.6, 0.05), pos_hint={"x": 0.17, "y": 0.15})
        self.add_widget(self.error_birthdate_label)

        # Sign Up Button
        self.sign_up_button = Button(size_hint=(0.26, 0.13), pos_hint={"x": 0.52, "y": 0.05}, background_normal="assets/home_button.png")
        self.sign_up_button.bind(on_press=self.sign_up)
        self.add_widget(self.sign_up_button)

        # Login Button
        self.login_button = Button(size_hint=(0.26, 0.13), pos_hint={"x": 0.22, "y": 0.05}, background_normal="assets/login_button.png")
        self.login_button.bind(on_press=self.switch_to_login)
        self.add_widget(self.login_button)

    def slide_header(self, dt):
        # Animate the current header sliding out
        anim_out = Animation(pos_hint={"x": -1, "y": 0.611}, duration=0.2)
        anim_out.bind(on_complete=self.update_header)
        anim_out.start(self.header_image)

    def update_header(self, *args):
        # Update the header image and reset its position
        self.current_header_index = (self.current_header_index + 1) % len(self.header_images)
        self.header_image.source = self.header_images[self.current_header_index]
        self.header_image.pos_hint = {"x": 1, "y": 0.611}

        # Animate the new header sliding in
        anim_in = Animation(pos_hint={"x": 0, "y": 0.611}, duration=0.2)
        anim_in.start(self.header_image)

    def sign_up(self, instance):
        username = self.username_input.text.strip()
        email = self.email_input.text.strip()
        password = self.password_input.text.strip()
        birth_month = self.birth_month.text.strip()
        birth_day = self.birth_day.text.strip()
        birth_year = self.birth_year.text.strip()

        self.email_error_label.text = ""
        self.password_error_label.text = ""
        self.error_birthdate_label.text = ""
        self.username_error_label.text = ""

        # Username validation
        if username == "":
            self.username_error_label.text = "Username cannot be empty!"
            return

        # Validate email
        if "@" not in email:
            self.email_error_label.text = "Invalid email address!"
            return

        # Password validation
        if len(password) < 6:
            self.password_error_label.text = "Password must be at least 6 characters long!"
            return

        # Birthdate validation
        try:
            birth_month = int(birth_month)
            birth_day = int(birth_day)
            birth_year = int(birth_year)
            if not (1 <= birth_month <= 12) or not (1 <= birth_day <= 31) or not (1900 <= birth_year <= 2023):
                self.error_birthdate_label.text = "Invalid birthdate!"
                return
        except ValueError:
            self.error_birthdate_label.text = "Birthdate must be numbers!"
            return

        # Load existing users or create a new file
        try:
            with open("users.json", "r") as file:
                users = json.load(file)
        except FileNotFoundError:
            users = {}

        # Check if username already exists
        if username in users:
            self.username_error_label.text = "Username already exists. Please choose a different username."
            return

        # Save new user
        users[username] = {
            "email": email,
            "password": password,
            "birthdate": f"{birth_month}/{birth_day}/{birth_year}"
        }
        with open("users.json", "w") as file:
            json.dump(users, file)

        if not username or not email or not password or not birth_month or not birth_day or not birth_year:
            print("All fields (username, email, password, and birthdate) are required!")
            return

        print(f"Sign Up successful! Welcome, {username}.")
        self.switch_to_home()


class HomePage(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Add background image
        self.add_widget(Image(source="assets/background.jpg", allow_stretch=True, keep_ratio=False))
        self.add_widget(Image(source="assets/logo.png", size_hint=(0.55, 0.55), pos_hint={"x": 0, "y": 0.68}))
        self.add_widget(Image(source="assets/logo_td.png", size_hint=(0.13, 0.13), pos_hint={"x": 0.8, "y": 0.88}))

        # Sliding Header (Images)
        self.header_images = [
            "assets/header/header1.jpg",
            "assets/header/header2.png",
            "assets/header/header3.jpg"
        ]
        self.current_header_index = 0
        self.header_image = Image(
            source=self.header_images[self.current_header_index],
            size_hint=(1, 0.3),
            pos_hint={"x": 0, "y": 0.611}
        )
        self.add_widget(self.header_image)

        # Schedule the header to slide every 3 seconds
        Clock.schedule_interval(self.slide_header, 5)

        # User profile background
        with self.canvas:
            Color(0.23, 0.5, 1.10, 1)
            RoundedRectangle(pos=(50, 400), size=(350, 150), radius=[20])  # Rounded rectangle

        self.add_widget(Image(source="assets/profile.png", size_hint=(0.2, 0.2), pos_hint={"x": 0.17, "y": 0.5}))

        # Welcome label
        self.welcome_label = Label(text="Welcome!", size_hint=(0.6, 0.1), pos_hint={"x": 0.25, "y": 0.6})
        self.add_widget(self.welcome_label)

    def slide_header(self, dt):
        # Animate the current header sliding out
        anim_out = Animation(pos_hint={"x": -1, "y": 0.611}, duration=0.2)
        anim_out.bind(on_complete=self.update_header)
        anim_out.start(self.header_image)

    def update_header(self, *args):
        # Update the header image and reset its position
        self.current_header_index = (self.current_header_index + 1) % len(self.header_images)
        self.header_image.source = self.header_images[self.current_header_index]
        self.header_image.pos_hint = {"x": 1, "y": 0.611}

        # Animate the new header sliding in
        anim_in = Animation(pos_hint={"x": 0, "y": 0.611}, duration=0.2)
        anim_in.start(self.header_image)

    def update_welcome_message(self, username):
        """Update the welcome message with the logged-in user's name."""
        self.welcome_label.text = f"Welcome, {username}!"

class MyApp(App):
    def build(self):
        self.icon = "assets/icon.png"  # Set the app icon
        self.title = "TalkitOut"  # Set the app title
        self.home_page = HomePage() 

        self.screen_manager = ScreenManager()

        # Login Page
        self.login_screen = Screen(name="Login")
        self.login_screen.add_widget(LoginPage(self.switch_to_signup, self.switch_to_home, self.home_page))
        self.screen_manager.add_widget(self.login_screen)

        # Sign Up Page
        self.sign_up_screen = Screen(name="SignUp")
        self.sign_up_screen.add_widget(SignUpPage(self.switch_to_home, self.switch_to_login))
        self.screen_manager.add_widget(self.sign_up_screen)

        # Home Page
        self.home_screen = Screen(name="Home")
        self.home_screen.add_widget(self.home_page)
        self.screen_manager.add_widget(self.home_screen)

        return self.screen_manager

    def switch_to_signup(self, instance=None):
        self.screen_manager.current = "SignUp"

    def switch_to_login(self, instance=None):
        self.screen_manager.current = "Login"

    def switch_to_home(self, instance=None):
        self.screen_manager.current = "Home"


if __name__ == "__main__":
    MyApp().run()