from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFillRoundFlatButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.progressbar import MDProgressBar
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.animation import Animation
from functools import partial
from kivy.properties import NumericProperty, ObjectProperty, StringProperty
from kivy.core.window import Window
import re
import json
import os
from hashlib import sha256


class DatabaseManager:
    def __init__(self):
        self.db_file = "users_db.json"
        self.load_database()

    def load_database(self):
        """Load database from file or create new one"""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r') as f:
                    self.users = json.load(f)
            except:
                self.users = {}
        else:
            self.users = {}
        self.save_database()

    def save_database(self):
        """Save database to file"""
        with open(self.db_file, 'w') as f:
            json.dump(self.users, f, indent=4)

    def hash_password(self, password):
        """Hash password for security"""
        return sha256(password.encode()).hexdigest()

    def create_user(self, user_data):
        """Create new user account"""
        email = user_data['email']
        
        # Check if user already exists
        if email in self.users:
            return False, "User already exists"
        
        # Hash the password
        user_data['password'] = self.hash_password(user_data['password'])
        
        # Add user to database
        self.users[email] = user_data
        self.save_database()
        return True, "User created successfully"

    def verify_login(self, email, password):
        """Verify user login credentials"""
        if email not in self.users:
            return False, "User not found"
        
        hashed_password = self.hash_password(password)
        if self.users[email]['password'] == hashed_password:
            return True, "Login successful"
        else:
            return False, "Incorrect password"

    def user_exists(self, email):
        """Check if user exists"""
        return email in self.users

    def get_user_data(self, email):
        """Get user data by email"""
        return self.users.get(email, {})


class LoginScreen(Screen):
    def __init__(self, app=None, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.build_ui()

    def build_ui(self):
        """Build the login screen UI"""
        # Main container
        main_layout = MDBoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(20),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        # Logo section
        logo_card = MDCard(
            size_hint=(None, None),
            size=(dp(100), dp(100)),
            pos_hint={"center_x": 0.5},
            elevation=3,
            padding=dp(10),
            radius=[dp(50),],
            md_bg_color=(0, 0, 0, 1)
        )
        mr_label = MDLabel(
            text="MR",
            halign="center",
            valign="center",
            theme_text_color="Custom",
            text_color=(0.5, 0.5, 0.5, 1),
            font_style="H4",
            bold=True
        )
        logo_card.add_widget(mr_label)
        main_layout.add_widget(logo_card)

        # App name label
        app_name_label = MDLabel(
            text="MR Trade",
            halign="center",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            font_style="H5",
            size_hint_y=None,
            height=dp(40),
            bold=True,
        )
        main_layout.add_widget(app_name_label)

        # Welcome text
        welcome_label = MDLabel(
            text="Welcome Back",
            halign="center",
            theme_text_color="Custom",
            text_color=(0.3, 0.3, 0.3, 1),
            font_style="H6",
            size_hint_y=None,
            height=dp(30)
        )
        main_layout.add_widget(welcome_label)
        main_layout.add_widget(MDBoxLayout(size_hint_y=0.05))

        # Login form card
        form_card = MDCard(
            orientation="vertical",
            padding=dp(25),
            spacing=dp(20),
            size_hint=(0.85, None),
            height=dp(280),
            pos_hint={"center_x": 0.5},
            elevation=4,
            radius=[dp(15),],
            md_bg_color=(0.98, 0.98, 0.98, 1)
        )

        # Email field
        self.email_field = MDTextField(
            hint_text="Email Address",
            mode="rectangle",
            size_hint_x=1,
            height=dp(60),
            icon_left="email",
            font_size=dp(16),
            line_color_focus=(0, 0, 0, 1),
        )
        form_card.add_widget(self.email_field)

        # Password field
        self.password_field = MDTextField(
            hint_text="Password",
            mode="rectangle",
            size_hint_x=1,
            height=dp(60),
            icon_left="lock",
            password=True,
            font_size=dp(16),
            line_color_focus=(0, 0, 0, 1),
            icon_right="eye-off",
        )
        self.password_field.bind(on_touch_down=self.toggle_password_on_touch)
        form_card.add_widget(self.password_field)

        # Forgot password link
        forgot_label = MDLabel(
            text="Forgot Password?",
            halign="right",
            theme_text_color="Custom",
            text_color=(0.5, 0.5, 0.5, 1),
            font_style="Body2",
            size_hint_y=None,
            height=dp(25),
        )
        forgot_label.bind(on_touch_down=self.forgot_password)
        form_card.add_widget(forgot_label)

        main_layout.add_widget(form_card)
        main_layout.add_widget(MDBoxLayout(size_hint_y=0.05))

        # Login button
        login_button = MDFillRoundFlatButton(
            text="LOGIN",
            size_hint=(None, None),
            width=dp(200),
            height=dp(50),
            pos_hint={"center_x": 0.5},
            md_bg_color=(0, 0, 0, 1),
            text_color=(1, 1, 1, 1),
            font_size=dp(16),
        )
        login_button.bind(on_press=self.login)
        main_layout.add_widget(login_button)

        # Divider
        divider_layout = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(30),
        )
        divider_layout.add_widget(MDBoxLayout())
        divider_layout.add_widget(MDLabel(
            text="or",
            halign="center",
            theme_text_color="Custom",
            text_color=(0.7, 0.7, 0.7, 1),
            size_hint_x=None,
            width=dp(30)
        ))
        divider_layout.add_widget(MDBoxLayout())
        main_layout.add_widget(divider_layout)

        # Create account button
        create_account_button = MDFillRoundFlatButton(
            text="CREATE NEW ACCOUNT",
            size_hint=(None, None),
            width=dp(200),
            height=dp(50),
            pos_hint={"center_x": 0.5},
            md_bg_color=(1, 1, 1, 1),
            text_color=(0, 0, 0, 1),
            font_size=dp(14),
            line_color=(0, 0, 0, 1),
            line_width=dp(1)
        )
        create_account_button.bind(on_press=self.go_to_step1)
        main_layout.add_widget(create_account_button)

        main_layout.add_widget(MDBoxLayout(size_hint_y=0.1))
        self.add_widget(main_layout)

    def toggle_password_on_touch(self, instance, touch):
        """Toggle password visibility when eye icon is clicked"""
        if instance.collide_point(*touch.pos):
            icon_area_width = dp(48)
            icon_x = instance.right - icon_area_width
            if icon_x <= touch.x <= instance.right and instance.y <= touch.y <= instance.top:
                self.toggle_password_visibility(instance)
                return True
        return False

    def toggle_password_visibility(self, instance):
        """Toggle password field visibility"""
        self.password_field.password = not self.password_field.password
        self.password_field.icon_right = "eye" if not self.password_field.password else "eye-off"

    def login(self, instance):
        """Handle login with database verification"""
        email = self.email_field.text.strip()
        password = self.password_field.text
        
        # Reset field errors
        self.email_field.error = False
        self.password_field.error = False
        self.email_field.helper_text = ""
        self.password_field.helper_text = ""

        if not email or not password:
            self.show_error("Please fill all fields")
            return
        
        # Verify credentials with database
        if self.app and self.app.db:
            success, message = self.app.db.verify_login(email, password)
            
            if success:
                # Login successful - navigate to data screen
                self.app.navigate_to('data')
            else:
                # Login failed - show error
                self.show_error(message)

    def show_error(self, message):
        """Show error message without shake animation"""
        self.email_field.error = True
        self.password_field.error = True
        self.email_field.helper_text = message
        self.password_field.helper_text = message

    def forgot_password(self, instance, touch):
        """Handle forgot password - navigate to forgot password screen"""
        if instance.collide_point(*touch.pos):
            if self.app:
                self.app.navigate_to('forgot_password')
            return True
        return False

    def go_to_step1(self, instance):
        """Navigate to step 1"""
        if self.app:
            self.app.navigate_to('step1')


class Step1Screen(Screen):
    def __init__(self, app=None, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.build_ui()

    def build_ui(self):
        """Build step 1 UI"""
        main_layout = MDBoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(25)
        )

        # Progress Steps - Centered horizontally with step 2 at x=0.5
        steps_layout = self.create_progress_steps(1)
        main_layout.add_widget(steps_layout)

        # Title
        title_label = MDLabel(
            text="Create Account",
            halign="center",
            font_style="H4",
            size_hint_y=None,
            height=dp(60),
            bold=True
        )
        main_layout.add_widget(title_label)

        # Subtitle
        subtitle_label = MDLabel(
            text="Personal Information",
            halign="center",
            theme_text_color="Secondary",
            font_style="H6",
            size_hint_y=None,
            height=dp(40)
        )
        main_layout.add_widget(subtitle_label)

        # Form card
        form_card = MDCard(
            orientation="vertical",
            padding=dp(30),
            spacing=dp(25),
            size_hint=(0.9, None),
            height=dp(320),
            pos_hint={"center_x": 0.5},
            elevation=4,
            radius=[dp(20),],
            md_bg_color=(0.98, 0.98, 0.98, 1)
        )

        # Full Name field
        self.full_name_field = MDTextField(
            hint_text="Full Name",
            mode="rectangle",
            size_hint_x=1,
            height=dp(60),
            icon_left="account",
            font_size=dp(16),
            line_color_focus=(0, 0, 0, 1),
        )
        form_card.add_widget(self.full_name_field)

        # Username field
        self.username_field = MDTextField(
            hint_text="Username",
            mode="rectangle",
            size_hint_x=1,
            height=dp(60),
            icon_left="account-circle",
            font_size=dp(16),
            line_color_focus=(0, 0, 0, 1),
        )
        form_card.add_widget(self.username_field)

        main_layout.add_widget(form_card)
        main_layout.add_widget(MDBoxLayout(size_hint_y=0.1))

        # Buttons layout - Centered and vertical
        buttons_layout = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(120),
            spacing=dp(15),
            pos_hint={"center_x": 0.5}
        )

        # Continue button
        continue_button = MDFillRoundFlatButton(
            text="CONTINUE",
            size_hint=(None, None),
            width=dp(200),
            height=dp(50),
            pos_hint={"center_x": 0.5},
            md_bg_color=(0, 0, 0, 1),
            text_color=(1, 1, 1, 1),
            font_size=dp(16)
        )
        continue_button.bind(on_press=self.go_to_step2)
        buttons_layout.add_widget(continue_button)

        main_layout.add_widget(buttons_layout)
        main_layout.add_widget(MDBoxLayout(size_hint_y=0.1))
        self.add_widget(main_layout)

    def create_progress_steps(self, active_step):
        """Create progress steps indicator with step 2 at center (x=0.5)"""
        # Main container
        main_container = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(80),
            spacing=dp(0)
        )
        
        # Calculate positions to center step 2
        # Add flexible space before steps
        main_container.add_widget(MDBoxLayout(size_hint_x=0.2))
        
        # Steps container with fixed spacing
        steps_container = MDBoxLayout(
            orientation="horizontal",
            size_hint_x=0.6,
            size_hint_y=None,
            height=dp(60),
            spacing=dp(0),
            pos_hint={"center_x": 0.5}
        )

        # Step 1
        step1_active = active_step >= 1
        step1_card = self.create_step(1, step1_active)
        steps_container.add_widget(step1_card)

        # Line between 1-2
        line1_color = (0, 0, 0, 1) if active_step >= 2 else (0.8, 0.8, 0.8, 1)
        line1 = self.create_connecting_line(line1_color)
        steps_container.add_widget(line1)

        # Step 2 - This will be at center
        step2_active = active_step >= 2
        step2_card = self.create_step(2, step2_active)
        steps_container.add_widget(step2_card)

        # Line between 2-3
        line2_color = (0, 0, 0, 1) if active_step >= 3 else (0.8, 0.8, 0.8, 1)
        line2 = self.create_connecting_line(line2_color)
        steps_container.add_widget(line2)

        # Step 3
        step3_active = active_step >= 3
        step3_card = self.create_step(3, step3_active)
        steps_container.add_widget(step3_card)

        main_container.add_widget(steps_container)
        # Add flexible space after steps
        main_container.add_widget(MDBoxLayout(size_hint_x=0.2))
        
        return main_container

    def create_step(self, number, active):
        """Create a step circle - Fully circular"""
        if active:
            step_card = MDCard(
                size_hint=(None, None),
                size=(dp(50), dp(50)),
                elevation=3,
                radius=[dp(25),],  # Fully circular
                md_bg_color=(0, 0, 0, 1)
            )
            text_color = (1, 1, 1, 1)
        else:
            step_card = MDCard(
                size_hint=(None, None),
                size=(dp(50), dp(50)),
                elevation=0,
                radius=[dp(25),],  # Fully circular
                md_bg_color=(0.8, 0.8, 0.8, 1)
            )
            text_color = (0.5, 0.5, 0.5, 1)

        step_label = MDLabel(
            text=str(number),
            halign="center",
            valign="center",
            theme_text_color="Custom",
            text_color=text_color,
            bold=True,
            font_style="H6"
        )
        step_card.add_widget(step_label)
        return step_card

    def create_connecting_line(self, color):
        """Create connecting line between steps"""
        line = MDBoxLayout(
            size_hint=(None, None),
            size=(dp(60), dp(4)),
            md_bg_color=color
        )
        return line

    def go_to_step2(self, instance):
        if self.app and self.full_name_field.text.strip() and self.username_field.text.strip():
            # Save data
            self.app.update_user_data('full_name', self.full_name_field.text)
            self.app.update_user_data('username', self.username_field.text)
            self.app.navigate_to('step2')


class Step2Screen(Screen):
    def __init__(self, app=None, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.build_ui()

    def build_ui(self):
        """Build step 2 UI"""
        main_layout = MDBoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(25)
        )

        # Progress Steps - Centered horizontally with step 2 at x=0.5
        steps_layout = self.create_progress_steps(2)
        main_layout.add_widget(steps_layout)

        # Title
        title_label = MDLabel(
            text="Create Account",
            halign="center",
            font_style="H4",
            size_hint_y=None,
            height=dp(60),
            bold=True
        )
        main_layout.add_widget(title_label)

        # Subtitle
        subtitle_label = MDLabel(
            text="Contact Information",
            halign="center",
            theme_text_color="Secondary",
            font_style="H6",
            size_hint_y=None,
            height=dp(40)
        )
        main_layout.add_widget(subtitle_label)

        # Form card
        form_card = MDCard(
            orientation="vertical",
            padding=dp(30),
            spacing=dp(25),
            size_hint=(0.9, None),
            height=dp(380),
            pos_hint={"center_x": 0.5},
            elevation=4,
            radius=[dp(20),],
            md_bg_color=(0.98, 0.98, 0.98, 1)
        )

        # Email field
        self.email_field = MDTextField(
            hint_text="Email Address",
            mode="rectangle",
            size_hint_x=1,
            height=dp(60),
            icon_left="email",
            font_size=dp(16),
            line_color_focus=(0, 0, 0, 1),
        )
        form_card.add_widget(self.email_field)

        # Phone field - numbers only with numeric keyboard
        self.phone_field = MDTextField(
            hint_text="Phone Number",
            mode="rectangle",
            size_hint_x=1,
            height=dp(60),
            icon_left="phone",
            font_size=dp(16),
            line_color_focus=(0, 0, 0, 1),
            input_type="number"  # Show numeric keyboard
        )
        form_card.add_widget(self.phone_field)

        # Country field
        self.country_field = MDTextField(
            hint_text="Country",
            mode="rectangle",
            size_hint_x=1,
            height=dp(60),
            icon_left="earth",
            font_size=dp(16),
            line_color_focus=(0, 0, 0, 1),
        )
        form_card.add_widget(self.country_field)

        main_layout.add_widget(form_card)
        main_layout.add_widget(MDBoxLayout(size_hint_y=0.1))

        # Buttons layout - Centered and vertical
        buttons_layout = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(120),
            spacing=dp(15),
            pos_hint={"center_x": 0.5}
        )

        # Continue button
        continue_button = MDFillRoundFlatButton(
            text="CONTINUE",
            size_hint=(None, None),
            width=dp(200),
            height=dp(50),
            pos_hint={"center_x": 0.5},
            md_bg_color=(0, 0, 0, 1),
            text_color=(1, 1, 1, 1),
            font_size=dp(16)
        )
        continue_button.bind(on_press=self.go_to_step3)
        buttons_layout.add_widget(continue_button)

        main_layout.add_widget(buttons_layout)
        main_layout.add_widget(MDBoxLayout(size_hint_y=0.1))
        self.add_widget(main_layout)

    def create_progress_steps(self, active_step):
        """Create progress steps indicator with step 2 at center (x=0.5)"""
        # Main container
        main_container = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(80),
            spacing=dp(0)
        )
        
        # Calculate positions to center step 2
        # Add flexible space before steps
        main_container.add_widget(MDBoxLayout(size_hint_x=0.2))
        
        # Steps container with fixed spacing
        steps_container = MDBoxLayout(
            orientation="horizontal",
            size_hint_x=0.6,
            size_hint_y=None,
            height=dp(60),
            spacing=dp(0),
            pos_hint={"center_x": 0.5}
        )

        # Step 1
        step1_active = active_step >= 1
        step1_card = self.create_step(1, step1_active)
        steps_container.add_widget(step1_card)

        # Line between 1-2
        line1_color = (0, 0, 0, 1) if active_step >= 2 else (0.8, 0.8, 0.8, 1)
        line1 = self.create_connecting_line(line1_color)
        steps_container.add_widget(line1)

        # Step 2 - This will be at center
        step2_active = active_step >= 2
        step2_card = self.create_step(2, step2_active)
        steps_container.add_widget(step2_card)

        # Line between 2-3
        line2_color = (0, 0, 0, 1) if active_step >= 3 else (0.8, 0.8, 0.8, 1)
        line2 = self.create_connecting_line(line2_color)
        steps_container.add_widget(line2)

        # Step 3
        step3_active = active_step >= 3
        step3_card = self.create_step(3, step3_active)
        steps_container.add_widget(step3_card)

        main_container.add_widget(steps_container)
        # Add flexible space after steps
        main_container.add_widget(MDBoxLayout(size_hint_x=0.2))
        
        return main_container

    def create_step(self, number, active):
        """Create a step circle - Fully circular"""
        if active:
            step_card = MDCard(
                size_hint=(None, None),
                size=(dp(50), dp(50)),
                elevation=3,
                radius=[dp(25),],  # Fully circular
                md_bg_color=(0, 0, 0, 1)
            )
            text_color = (1, 1, 1, 1)
        else:
            step_card = MDCard(
                size_hint=(None, None),
                size=(dp(50), dp(50)),
                elevation=0,
                radius=[dp(25),],  # Fully circular
                md_bg_color=(0.8, 0.8, 0.8, 1)
            )
            text_color = (0.5, 0.5, 0.5, 1)

        step_label = MDLabel(
            text=str(number),
            halign="center",
            valign="center",
            theme_text_color="Custom",
            text_color=text_color,
            bold=True,
            font_style="H6"
        )
        step_card.add_widget(step_label)
        return step_card

    def create_connecting_line(self, color):
        """Create connecting line between steps"""
        line = MDBoxLayout(
            size_hint=(None, None),
            size=(dp(60), dp(4)),
            md_bg_color=color
        )
        return line

    def go_to_step3(self, instance):
        if self.app and self.email_field.text.strip() and self.phone_field.text.strip():
            # Save data
            self.app.update_user_data('email', self.email_field.text)
            self.app.update_user_data('phone', self.phone_field.text)
            self.app.update_user_data('country', self.country_field.text)
            self.app.navigate_to('step3')


class Step3Screen(Screen):
    def __init__(self, app=None, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.build_ui()

    def build_ui(self):
        """Build step 3 UI"""
        main_layout = MDBoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(25)
        )

        # Progress Steps - Centered horizontally with step 2 at x=0.5
        steps_layout = self.create_progress_steps(3)
        main_layout.add_widget(steps_layout)

        # Title
        title_label = MDLabel(
            text="Create Account",
            halign="center",
            font_style="H4",
            size_hint_y=None,
            height=dp(60),
            bold=True
        )
        main_layout.add_widget(title_label)

        # Subtitle
        subtitle_label = MDLabel(
            text="Security Settings",
            halign="center",
            theme_text_color="Secondary",
            font_style="H6",
            size_hint_y=None,
            height=dp(40)
        )
        main_layout.add_widget(subtitle_label)

        # Form card
        form_card = MDCard(
            orientation="vertical",
            padding=dp(30),
            spacing=dp(25),
            size_hint=(0.9, None),
            height=dp(380),
            pos_hint={"center_x": 0.5},
            elevation=4,
            radius=[dp(20),],
            md_bg_color=(0.98, 0.98, 0.98, 1)
        )

        # Password field
        self.password_field = MDTextField(
            hint_text="Password",
            mode="rectangle",
            size_hint_x=1,
            height=dp(60),
            icon_left="lock",
            password=True,
            font_size=dp(16),
            line_color_focus=(0, 0, 0, 1),
            icon_right="eye-off",
        )
        self.password_field.bind(text=self.check_password_strength)
        self.password_field.bind(on_touch_down=self.toggle_password_visibility)
        form_card.add_widget(self.password_field)

        # Password strength bar - Circular edges
        self.strength_bar = MDProgressBar(
            value=0,
            size_hint_y=None,
            height=dp(12),
            radius=[dp(6),],  # Circular edges
        )
        form_card.add_widget(self.strength_bar)

        # Confirm password field
        self.confirm_password_field = MDTextField(
            hint_text="Confirm Password",
            mode="rectangle",
            size_hint_x=1,
            height=dp(60),
            icon_left="lock-check",
            password=True,
            font_size=dp(16),
            line_color_focus=(0, 0, 0, 1),
            icon_right="eye-off",
        )
        self.confirm_password_field.bind(on_touch_down=self.toggle_confirm_password_visibility)
        form_card.add_widget(self.confirm_password_field)

        main_layout.add_widget(form_card)
        main_layout.add_widget(MDBoxLayout(size_hint_y=0.1))

        # Buttons layout - Centered and vertical
        buttons_layout = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(120),
            spacing=dp(15),
            pos_hint={"center_x": 0.5}
        )

        # Create account button
        create_account_button = MDFillRoundFlatButton(
            text="CREATE ACCOUNT",
            size_hint=(None, None),
            width=dp(200),
            height=dp(50),
            pos_hint={"center_x": 0.5},
            md_bg_color=(0, 0, 0, 1),
            text_color=(1, 1, 1, 1),
            font_size=dp(16)
        )
        create_account_button.bind(on_press=self.create_account)
        buttons_layout.add_widget(create_account_button)

        main_layout.add_widget(buttons_layout)
        main_layout.add_widget(MDBoxLayout(size_hint_y=0.1))
        self.add_widget(main_layout)

    def toggle_password_visibility(self, instance, touch):
        """Toggle password visibility when eye icon is clicked"""
        if instance.collide_point(*touch.pos):
            icon_area_width = dp(48)
            icon_x = instance.right - icon_area_width
            if icon_x <= touch.x <= instance.right and instance.y <= touch.y <= instance.top:
                self.password_field.password = not self.password_field.password
                self.password_field.icon_right = "eye" if not self.password_field.password else "eye-off"
                return True
        return False

    def toggle_confirm_password_visibility(self, instance, touch):
        """Toggle confirm password visibility when eye icon is clicked"""
        if instance.collide_point(*touch.pos):
            icon_area_width = dp(48)
            icon_x = instance.right - icon_area_width
            if icon_x <= touch.x <= instance.right and instance.y <= touch.y <= instance.top:
                self.confirm_password_field.password = not self.confirm_password_field.password
                self.confirm_password_field.icon_right = "eye" if not self.confirm_password_field.password else "eye-off"
                return True
        return False

    def create_progress_steps(self, active_step):
        """Create progress steps indicator with step 2 at center (x=0.5)"""
        # Main container
        main_container = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(80),
            spacing=dp(0)
        )
        
        # Calculate positions to center step 2
        # Add flexible space before steps
        main_container.add_widget(MDBoxLayout(size_hint_x=0.2))
        
        # Steps container with fixed spacing
        steps_container = MDBoxLayout(
            orientation="horizontal",
            size_hint_x=0.6,
            size_hint_y=None,
            height=dp(60),
            spacing=dp(0),
            pos_hint={"center_x": 0.5}
        )

        # Step 1
        step1_active = active_step >= 1
        step1_card = self.create_step(1, step1_active)
        steps_container.add_widget(step1_card)

        # Line between 1-2
        line1_color = (0, 0, 0, 1) if active_step >= 2 else (0.8, 0.8, 0.8, 1)
        line1 = self.create_connecting_line(line1_color)
        steps_container.add_widget(line1)

        # Step 2 - This will be at center
        step2_active = active_step >= 2
        step2_card = self.create_step(2, step2_active)
        steps_container.add_widget(step2_card)

        # Line between 2-3
        line2_color = (0, 0, 0, 1) if active_step >= 3 else (0.8, 0.8, 0.8, 1)
        line2 = self.create_connecting_line(line2_color)
        steps_container.add_widget(line2)

        # Step 3
        step3_active = active_step >= 3
        step3_card = self.create_step(3, step3_active)
        steps_container.add_widget(step3_card)

        main_container.add_widget(steps_container)
        # Add flexible space after steps
        main_container.add_widget(MDBoxLayout(size_hint_x=0.2))
        
        return main_container

    def create_step(self, number, active):
        """Create a step circle - Fully circular"""
        if active:
            step_card = MDCard(
                size_hint=(None, None),
                size=(dp(50), dp(50)),
                elevation=3,
                radius=[dp(25),],  # Fully circular
                md_bg_color=(0, 0, 0, 1)
            )
            text_color = (1, 1, 1, 1)
        else:
            step_card = MDCard(
                size_hint=(None, None),
                size=(dp(50), dp(50)),
                elevation=0,
                radius=[dp(25),],  # Fully circular
                md_bg_color=(0.8, 0.8, 0.8, 1)
            )
            text_color = (0.5, 0.5, 0.5, 1)

        step_label = MDLabel(
            text=str(number),
            halign="center",
            valign="center",
            theme_text_color="Custom",
            text_color=text_color,
            bold=True,
            font_style="H6"
        )
        step_card.add_widget(step_label)
        return step_card

    def create_connecting_line(self, color):
        """Create connecting line between steps"""
        line = MDBoxLayout(
            size_hint=(None, None),
            size=(dp(60), dp(4)),
            md_bg_color=color
        )
        return line

    def check_password_strength(self, instance, value):
        """Check password strength and update progress bar"""
        strength = 0
        color = (0.8, 0.8, 0.8, 1)  # Default gray

        if len(value) >= 8:
            strength += 25
        if re.search(r"[A-Z]", value):
            strength += 25
        if re.search(r"[a-z]", value):
            strength += 25
        if re.search(r"[0-9!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", value):
            strength += 25

        self.strength_bar.value = strength

        # Update progress bar color based on strength
        if strength <= 25:
            color = (1, 0, 0, 1)  # Red
        elif strength <= 50:
            color = (1, 0.5, 0, 1)  # Orange
        elif strength <= 75:
            color = (0, 0.5, 1, 1)  # Blue
        else:
            color = (0, 0.8, 0, 1)  # Green

        self.strength_bar.md_bg_color = color

    def create_account(self, instance):
        """Final account creation and save to database"""
        password = self.password_field.text
        confirm_password = self.confirm_password_field.text

        if password != confirm_password:
            print("Passwords don't match!")
            return

        if self.app:
            # Save password to user data
            self.app.update_user_data('password', password)
            
            # Get complete user data
            user_data = self.app.get_user_data()
            
            # Save user to database
            if self.app.db:
                success, message = self.app.db.create_user(user_data)
                
                if success:
                    print("Account created successfully!")
                    print("User data saved to database")
                    
                    # Navigate to success screen
                    self.app.navigate_to('success')
                else:
                    print(f"Error: {message}")


class SuccessScreen(Screen):
    def __init__(self, app=None, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.build_ui()

    def build_ui(self):
        """Build success screen UI"""
        main_layout = MDBoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(30),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        # Success icon
        success_icon = MDLabel(
            text="✓",
            halign="center",
            theme_text_color="Custom",
            text_color=(0, 0.8, 0, 1),
            font_style="H1",
            size_hint_y=None,
            height=dp(100),
            bold=True
        )
        main_layout.add_widget(success_icon)

        # Success message
        success_label = MDLabel(
            text="Congratulations!",
            halign="center",
            font_style="H3",
            size_hint_y=None,
            height=dp(60),
            bold=True
        )
        main_layout.add_widget(success_label)

        # Sub message
        sub_label = MDLabel(
            text="Your account has been created successfully",
            halign="center",
            theme_text_color="Secondary",
            font_style="H6",
            size_hint_y=None,
            height=dp(40)
        )
        main_layout.add_widget(sub_label)

        main_layout.add_widget(MDBoxLayout(size_hint_y=0.2))

        # Continue button
        continue_button = MDFillRoundFlatButton(
            text="CONTINUE",
            size_hint=(None, None),
            width=dp(200),
            height=dp(50),
            pos_hint={"center_x": 0.5},
            md_bg_color=(0, 0, 0, 1),
            text_color=(1, 1, 1, 1),
            font_size=dp(16)
        )
        continue_button.bind(on_press=self.go_to_data)
        main_layout.add_widget(continue_button)

        self.add_widget(main_layout)

    def go_to_data(self, instance):
        """Navigate to data screen"""
        if self.app:
            self.app.navigate_to('data')


class ForgotPasswordScreen(Screen):
    def __init__(self, app=None, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.build_ui()

    def build_ui(self):
        """Build forgot password screen UI"""
        main_layout = MDBoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(25),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        # Logo section
        logo_card = MDCard(
            size_hint=(None, None),
            size=(dp(80), dp(80)),
            pos_hint={"center_x": 0.5},
            elevation=2,
            padding=dp(10),
            radius=[dp(40),],
            md_bg_color=(0, 0, 0, 1)
        )
        mr_label = MDLabel(
            text="MR",
            halign="center",
            valign="center",
            theme_text_color="Custom",
            text_color=(0.5, 0.5, 0.5, 1),
            font_style="H5",
            bold=True
        )
        logo_card.add_widget(mr_label)
        main_layout.add_widget(logo_card)

        # Title
        title_label = MDLabel(
            text="Reset Password",
            halign="center",
            font_style="H4",
            size_hint_y=None,
            height=dp(60),
            bold=True
        )
        main_layout.add_widget(title_label)

        # Instruction text
        instruction_label = MDLabel(
            text="Enter your email address and we'll send you a link to reset your password",
            halign="center",
            theme_text_color="Secondary",
            font_style="Body1",
            size_hint_y=None,
            height=dp(60)
        )
        main_layout.add_widget(instruction_label)

        # Form card
        form_card = MDCard(
            orientation="vertical",
            padding=dp(30),
            spacing=dp(25),
            size_hint=(0.85, None),
            height=dp(200),
            pos_hint={"center_x": 0.5},
            elevation=4,
            radius=[dp(15),],
            md_bg_color=(0.98, 0.98, 0.98, 1)
        )

        # Email field
        self.email_field = MDTextField(
            hint_text="Email Address",
            mode="rectangle",
            size_hint_x=1,
            height=dp(60),
            icon_left="email",
            font_size=dp(16),
            line_color_focus=(0, 0, 0, 1),
        )
        form_card.add_widget(self.email_field)

        main_layout.add_widget(form_card)
        main_layout.add_widget(MDBoxLayout(size_hint_y=0.1))

        # Send reset button
        send_button = MDFillRoundFlatButton(
            text="SEND RESET LINK",
            size_hint=(None, None),
            width=dp(200),
            height=dp(50),
            pos_hint={"center_x": 0.5},
            md_bg_color=(0, 0, 0, 1),
            text_color=(1, 1, 1, 1),
            font_size=dp(16)
        )
        send_button.bind(on_press=self.send_reset_link)
        main_layout.add_widget(send_button)

        main_layout.add_widget(MDBoxLayout(size_hint_y=0.2))
        self.add_widget(main_layout)

    def send_reset_link(self, instance):
        """Handle sending reset password link with database check"""
        email = self.email_field.text.strip()
        
        if not email:
            self.show_error("Please enter your email address")
            return
        
        if "@" not in email:
            self.show_error("Please enter a valid email address")
            return
        
        # Check if user exists in database
        if self.app and self.app.db:
            if self.app.db.user_exists(email):
                # Simulate sending reset link
                print(f"Reset password link sent to: {email}")
                print(f"Success: Reset link sent to {email}")
                
                # Go back to login after success
                self.app.navigate_to('login')
            else:
                self.show_error("Email not found in our system")

    def show_error(self, message):
        """Show error message"""
        self.email_field.error = True
        self.email_field.helper_text = message


class DataScreen(Screen):
    def __init__(self, app=None, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.build_ui()

    def build_ui(self):
        """Build data screen UI"""
        main_layout = MDBoxLayout(orientation="vertical")
        
        # Header
        header = MDLabel(
            text="Welcome to MR Trade!",
            halign="center",
            valign="center",
            font_style="H4",
            size_hint_y=None,
            height=dp(100)
        )
        main_layout.add_widget(header)
        
        self.add_widget(main_layout)


class MRTradeApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_data = {}
        self.screen_manager = None
        self.db = DatabaseManager()  # Initialize database

    def build(self):
        """Build the application UI"""
        self.theme_cls.primary_palette = "Gray"
        self.theme_cls.primary_hue = "900"
        self.theme_cls.theme_style = "Light"

        # Create screen manager with fast transition
        self.screen_manager = ScreenManager()
        self.screen_manager.transition = SlideTransition(duration=0.05)

        # Add all screens
        self.screen_manager.add_widget(LoginScreen(name='login', app=self))
        self.screen_manager.add_widget(DataScreen(name='data', app=self))
        self.screen_manager.add_widget(Step1Screen(name='step1', app=self))
        self.screen_manager.add_widget(Step2Screen(name='step2', app=self))
        self.screen_manager.add_widget(Step3Screen(name='step3', app=self))
        self.screen_manager.add_widget(SuccessScreen(name='success', app=self))
        self.screen_manager.add_widget(ForgotPasswordScreen(name='forgot_password', app=self))

        # Bind back button for Android
        Window.bind(on_keyboard=self.on_back_button)

        return self.screen_manager

    def on_back_button(self, window, key, *args):
        """Handle back button press on Android"""
        if key == 27:  # 27 is the keycode for Android back button
            return self.go_back()
        return False

    def go_back(self):
        """Navigate back to previous screen"""
        current_screen = self.screen_manager.current
        
        # Define screen navigation order
        screen_order = ['login', 'step1', 'step2', 'step3', 'success', 'forgot_password', 'data']
        
        try:
            current_index = screen_order.index(current_screen)
            
            if current_index > 0:
                # Go to previous screen with fast transition
                previous_screen = screen_order[current_index - 1]
                self.screen_manager.transition = SlideTransition(duration=0.05)
                self.screen_manager.current = previous_screen
                return True  # Event handled
            else:
                # If on login screen, show exit confirmation or do nothing
                return True  # Event handled
                
        except ValueError:
            # If current screen not in list, go to login
            self.screen_manager.transition = SlideTransition(duration=0.05)
            self.screen_manager.current = 'login'
            return True  # Event handled

    def navigate_to(self, screen_name):
        """Navigate to specific screen with fast transition"""
        self.screen_manager.transition = SlideTransition(duration=0.05)
        self.screen_manager.current = screen_name

    def update_user_data(self, key, value):
        """Update user data dictionary"""
        self.user_data[key] = value

    def get_user_data(self):
        """Get all user data"""
        return self.user_data.copy()


if __name__ == "__main__":
    MRTradeApp().run()
       