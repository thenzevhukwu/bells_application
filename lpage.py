from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QHBoxLayout,
    QMessageBox,
    QStackedWidget,
)
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt
import sys


class LandingPage(QWidget):  # Subclass QWidget
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        # Set window properties
        self.setWindowTitle("University Login")  # Removed from QWidget (only for QMainWindow)
        self.setGeometry(100, 100, 1080, 720)

        # Apply background image using stylesheet
        self.setStyleSheet(
            """
            QWidget {
                background-image: url("bells-img.jpg");
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover;
            }
            """
        )

        # Create a dark overlay (semi-transparent QWidget)
        overlay = QWidget(self)
        overlay.setStyleSheet(
            """
            QWidget {
                background-color: rgba(0, 0, 0, 0.5);  /* Black with 50% opacity */
            }
            """
        )
        overlay.setGeometry(self.rect())  # Covers the entire window

        # Create a layout for text and buttons
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Title
        title_label = QLabel("Bells University of Technology\nE-Campus Portal")
        title_label.setFont(QFont("Artifakt Element", 20, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: white;")  # Ensures text is visible over the image
        main_layout.addWidget(title_label)

        # Subtitle
        subtitle_label = QLabel("Only the best is good for Bells")
        subtitle_label.setFont(QFont("Artifakt Element", 16))
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: white;")
        main_layout.addWidget(subtitle_label)

        # Login Button
        login_button = QPushButton("Login")
        login_button.setFont(QFont("Artifakt Element", 14, QFont.Weight.Bold))
        login_button.setStyleSheet(
            """
            QPushButton {
                background-color: #4682b4;  /* Steel Blue */
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #5a9bd3;
            }
            QPushButton:pressed {
                background-color: #3a6591;
            }
            """
        )
        login_button.clicked.connect(self.open_main_login)
        main_layout.addSpacing(50)
        main_layout.addWidget(login_button, alignment=Qt.AlignmentFlag.AlignBottom)

        self.setLayout(main_layout)  # Set the layout for the QWidget

    def resizeEvent(self, event):
        """Ensure overlay and widgets resize with the window."""
        for child in self.findChildren(QWidget):
            child.setGeometry(self.rect())
        super().resizeEvent(event)

    def open_main_login(self):
        # Create an instance of LoginWindow and show it
        self.parent().setCurrentIndex(1)  # Navigate to the login page


class LoginWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Bells University Login Page")
        self.setGeometry(100, 100, 1080, 720)

        # Set the window icon (favicon)
        self.setWindowIcon(QIcon("university_logo.png"))  # Provide the path to your icon file

        self.main_layout = QVBoxLayout()
        self.create_top_layout()
        self.create_login_widgets()
        self.setLayout(self.main_layout)

    def create_top_layout(self):
        self.university_label = QLabel("Bells University Of Technology")
        self.university_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.main_layout.addWidget(self.university_label)

    def create_login_widgets(self):
        self.login_label = QLabel("Login")

        self.username_label = QLabel("Username")
        self.username_input = QLineEdit()

        self.password_label = QLabel("Password")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        # Add the button for toggling password visibility
        self.toggle_password_btn = QPushButton("👁", self)
        self.toggle_password_btn.setStyleSheet("font-size: 12px; background: transparent; border: none;")
        self.toggle_password_btn.clicked.connect(self.toggle_password_visibility)

        # Create a horizontal layout for password input and toggle button
        self.password_layout = QHBoxLayout()
        self.password_layout.addWidget(self.password_input)
        self.password_layout.addWidget(self.toggle_password_btn)

        # Create the login button and create account button
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)

        self.create_account_button = QPushButton("Create Account")
        self.create_account_button.clicked.connect(self.open_create_account_dialog)

        # Create form layout and add widgets
        self.form_layout = QVBoxLayout()
        self.form_layout.addWidget(self.login_label)
        self.form_layout.addWidget(self.username_label)
        self.form_layout.addWidget(self.username_input)
        self.form_layout.addWidget(self.password_label)
        self.form_layout.addLayout(self.password_layout)  # Add password layout with button
        self.form_layout.addWidget(self.login_button)
        self.form_layout.addWidget(self.create_account_button)

        self.main_layout.addLayout(self.form_layout)

    def toggle_password_visibility(self):
        """
        Toggles the visibility of the password input field.
        """
        if self.password_input.echoMode() == QLineEdit.EchoMode.Password:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_password_btn.setText("🙈")  # Change to closed-eye icon
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_password_btn.setText("👁")  # Change back to open-eye icon

    def login(self):
        # Handle login functionality
        pass

    def open_create_account_dialog(self):
        # Open account creation dialog
        pass


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("University Login")
        self.setGeometry(100, 100, 1080, 720)

        # Create a stacked widget and add pages
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.landing_page = LandingPage(self.stacked_widget)
        self.login_page = LoginWindow(self.stacked_widget)

        self.stacked_widget.addWidget(self.landing_page)  # Page 0
        self.stacked_widget.addWidget(self.login_page)    # Page 1


# Main execution of the application
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
