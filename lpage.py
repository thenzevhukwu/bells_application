from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame
)
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bells University of Technology")
        self.setGeometry(100, 100, 1080, 720)

        # Main layout
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

        # Create left (login) and right (info) sections
        self.create_login_section()
        self.create_info_section()

        # Apply styles
        self.setStyleSheet("background-color: white;")

    def create_login_section(self):
        """Create the left login section."""
        login_frame = QFrame()
        login_frame.setStyleSheet("background-color: #e6e6e6;border-radius: 25px;")
        login_layout = QVBoxLayout(login_frame)
        login_layout.setContentsMargins(40, 60, 40, 60)

        # Title
        title = QLabel("Bells University Login Page")
        title.setFont(QFont("Artifakt Element Medium", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: black;")
        login_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignLeft)

        subtitle = QLabel("Log in to access your account.")
        subtitle.setFont(QFont("Artifakt Element Medium", 14))
        subtitle.setStyleSheet("color: black;")
        login_layout.addWidget(subtitle, alignment=Qt.AlignmentFlag.AlignLeft)

        # Username input
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet("""
            padding: 12px;
            font-size: 14px;
            border: 1px solid #ccc;
            border-radius: 20px;
            color: black;
        """)
        login_layout.addWidget(self.username_input)

        # Password input with toggle button inside
        password_frame = QFrame()
        password_layout = QHBoxLayout(password_frame)
        password_layout.setContentsMargins(0, 0, 0, 0)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setStyleSheet("""
            padding: 12px;
            font-size: 14px;
            border: 1px solid #ccc;
            border-radius: 20px;
            color: black;
        """)
        password_layout.addWidget(self.password_input)

        self.toggle_password_btn = QPushButton("👁")
        self.toggle_password_btn.setStyleSheet("""
            font-size: 14px; 
            background: transparent; 
            border: none;
            margin: 0;
        """)
        self.toggle_password_btn.clicked.connect(self.toggle_password_visibility)
        password_layout.addWidget(self.toggle_password_btn, alignment=Qt.AlignmentFlag.AlignRight)

        login_layout.addWidget(password_frame)

        # Login button
        login_button = QPushButton("Log In")
        login_button.setStyleSheet("""
            QPushButton {
                background-color: #002147;  /* Default background color */
                color: white;  /* Text color */
                font-size: 16px; 
                padding: 12px;
                border: none;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: #003366;  /* Slightly lighter blue when hovered */
            }
            QPushButton:pressed {
                background-color: #00060d;  /* Darker blue when clicked */
            }
        """)
        login_layout.addWidget(login_button)

        # Forgot Password Button
        forgot_password_button = QPushButton("Forgot Password?")
        forgot_password_button.setFont(QFont("Artifakt Element", 14, QFont.Weight.Bold))
        forgot_password_button.setStyleSheet("""
            color: #002147;
            font-size: 14px;
            background: transparent;
            border: none;
            text-align: right;
            margin-top: 5px;
            font-weight: bold;
        """)
        forgot_password_button.setCursor(Qt.CursorShape.PointingHandCursor)  # Change cursor to pointer on hover
        forgot_password_button.clicked.connect(self.open_forgot_password_dialog)  # Connect to a method

        login_layout.addWidget(forgot_password_button, alignment=Qt.AlignmentFlag.AlignLeft)

        # Replace the Sign-Up button with the text link
        signup_label = QLabel('Don\'t you have an account? '
                              '<a href="" style="color: #002147;'
                              'font-weight: bold;'
                              'text-decoration: none;'
                              'font-family: Artifakt Element Medium;'
                              '">Sign Up</a>')
        signup_label.setStyleSheet("""
            color: black;
            font-size: 14px;
            margin-top: 10px;
            text-align: center;
        """)
        signup_label.setFont(QFont("Artifakt Element", 14, QFont.Weight.Bold))
        signup_label.setOpenExternalLinks(True)  # Allows the link to be clickable
        signup_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        login_layout.addWidget(signup_label)

        signup_label.linkActivated.connect(self.open_signup_dialog)

        self.main_layout.addWidget(login_frame)

    def open_signup_dialog(self):
        # Handle the sign-up process here
        print("Sign-Up link clicked")

    def open_forgot_password_dialog(self):
        # Handle the "Forgot Password" process here
        print("Forgot Password button clicked")
        # You can display a dialog or open another window

    def toggle_password_visibility(self):
        """Toggles the visibility of the password input field."""
        if self.password_input.echoMode() == QLineEdit.EchoMode.Password:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_password_btn.setText("🙈")  # Change to closed-eye icon
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_password_btn.setText("👁")  # Change back to open-eye icon

    def create_info_section(self):
        """Create the right info section."""
        info_frame = QFrame()
        info_frame.setStyleSheet("background-color: #002147; border-radius: 25px;")
        info_layout = QVBoxLayout(info_frame)
        info_layout.setContentsMargins(40, 60, 40, 60)

        # Heading
        info_heading = QLabel("Revolutionizing Learning")
        info_heading.setFont(QFont("Artifakt Element Medium", 20, QFont.Weight.Bold))
        info_heading.setStyleSheet("color: white; margin-bottom: 10px;")
        info_layout.addWidget(info_heading, alignment=Qt.AlignmentFlag.AlignTop)

        # Subtitle
        info_subtitle = QLabel(
            "Discover a world of opportunities through our cutting-edge platform. "
            "Manage your courses, collaborate with peers, and excel in your academic journey."
        )
        info_subtitle.setFont(QFont("Artifakt Element Medium", 14))
        info_subtitle.setStyleSheet("color: white;")
        info_subtitle.setWordWrap(True)
        info_layout.addWidget(info_subtitle, alignment=Qt.AlignmentFlag.AlignTop)

        # Placeholder image or icon
        placeholder_image = QLabel("🎓")
        placeholder_image.setFont(QFont("Artifakt Element Medium", 100))
        placeholder_image.setStyleSheet("color: white;")
        info_layout.addWidget(placeholder_image, alignment=Qt.AlignmentFlag.AlignCenter)

        # Add the info frame to the main layout
        self.main_layout.addWidget(info_frame)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
