import sys
import sqlite3
import hashlib
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QMessageBox, QDialog, QFormLayout, QTableWidget, QTableWidgetItem, QComboBox, QSpinBox, QHeaderView,
    QHBoxLayout, QScrollArea, QMainWindow, QStackedWidget, QFrame, QGroupBox, QGridLayout, QTextEdit, QCalendarWidget,
    QListWidget, QTabWidget, QProgressBar
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont, QIntValidator
import subprocess

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from pyqtgraph import PlotWidget, BarGraphItem

subprocess.run(['python', 'configure_db.py'])

# Connect to SQLite database
conn = sqlite3.connect('assets/school_database.db')
cursor = conn.cursor()


# Define the database update function
def update_user_management():
    conn = sqlite3.connect('assets/school_database.db')
    cursor = conn.cursor()

    try:
        # Fetch data from the 'general_data' table
        cursor.execute('''
        SELECT username, email, phone_number, role FROM general_data
        ''')
        general_data_rows = cursor.fetchall()

        for row in general_data_rows:
            username, email, phone_number, role = row

            # Check if the record exists in the 'user_management' table
            cursor.execute('''
            SELECT id FROM user_management WHERE username = ?
            ''', (username,))
            record = cursor.fetchone()

            if record:
                # Update the existing record (removed last_active)
                cursor.execute('''
                UPDATE user_management
                SET email = ?, phone_number = ?, role = ?
                WHERE username = ?
                ''', (email, phone_number, role, username))
            else:
                # Insert a new record into the table (removed last_active)
                cursor.execute('''
                INSERT INTO user_management (username, email, phone_number, role, date_added)
                VALUES (?, ?, ?, ?, ?)
                ''', (username, email, phone_number, role, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        # Commit changes to the database
        conn.commit()
        print("User management table updated successfully.")

    except sqlite3.ProgrammingError as e:
        print(f"ProgrammingError: {e}")

    except sqlite3.Error as e:
        print(f"Database error: {e}")

    finally:
        # Ensure the connection is closed
        cursor.close()  # Close the cursor explicitly
        conn.close()  # Close the connection explicitly


# Execute the update function
update_user_management()


# Helper function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Create initial admin and teacher accounts
def create_admin_user():
    # Check if the admin user exists
    cursor.execute("SELECT * FROM general_data WHERE username = ?", ('admin-user',))
    admin = cursor.fetchone()
    if not admin:
        admin_password = hash_password('admin-admin')
        cursor.execute(
            """
            INSERT INTO general_data 
            (name, matric_no, level, department, age, phone_number, username, password, email, role, approved) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            ('Admin User', 'ADMIN001', 0, 'Admin Department', 0, '0000000000',
             'admin-user', admin_password, 'admin@example.com', 'Admin', 1)
        )
        conn.commit()

    # Check if the teacher user exists
    cursor.execute("SELECT * FROM general_data WHERE username = ?", ('Florence',))
    teacher = cursor.fetchone()
    if not teacher:
        teacher_password = hash_password('fshaw')
        cursor.execute(
            """
            INSERT INTO general_data 
            (name, matric_no, level, department, age, phone_number, username, password, email, role, approved) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            ("Florence Shaw", "M12345", 300, "Computer Science", 21, "123-456-7890",
             "Florence", teacher_password, "florence123@gmail.com", "Teacher", 1)
        )
        conn.commit()

    # Check if the student user exists
    cursor.execute("SELECT * FROM general_data WHERE username = ?", ('John',))
    student = cursor.fetchone()
    if not student:
        student_password = hash_password('fshaw')
        cursor.execute(
            """
            INSERT INTO general_data 
            (name, matric_no, level, department, age, phone_number, username, password, email, role, approved) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            ("John Doe", "2022/12578", 200, "Computer Engineering", 17, "123-456-7890",
             "John", student_password, "john123@gmail.com", "Student", 1)
        )
        conn.commit()


# Call the function to create admin and teacher users
create_admin_user()


# Retrieve a student's details
def get_student_biodata(username):
    cursor.execute(
        "SELECT matric_no, name, level, department, email, phone_number FROM general_data WHERE username = ?",
        (username,))
    return cursor.fetchone()


class LandingPage(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        # Set window properties
        self.setWindowTitle("University Login")
        self.setGeometry(100, 100, 1080, 720)

        # Create a central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Set the stylesheet dynamically using the resolved image path
        self.setStyleSheet(
            f"""
        QMainWindow {{
            background-image: url("assets/bells-img.jpg");  /* Convert backslashes to forward slashes */
            background-repeat: no-repeat;
            background-position: center;
            background-size: 100% 100%; /* Ensure image covers entire window */
        }}
        """
        )

        # Create a dark overlay (semi-transparent QWidget)
        self.overlay = QWidget(self.centralWidget())
        self.overlay.setObjectName("overlay")
        self.overlay.setStyleSheet(
            """
            QWidget#overlay {
                background-color: rgba(0, 0, 0, 0.5);  /* Black with 50% opacity */
            }
            """
        )
        self.overlay.setGeometry(self.rect())  # Initially covers the entire window

        # Create a layout for text and buttons
        main_layout = QVBoxLayout()
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

        # Add the layout to the central widget
        central_widget.setLayout(main_layout)

    def resizeEvent(self, event):
        """Ensure the overlay resizes with the window without affecting other widgets."""
        overlay = self.findChild(QWidget, "overlay")
        if overlay:
            overlay.setGeometry(self.rect())  # Resize only the overlay to cover the window
        super().resizeEvent(event)

    def open_main_login(self):
        # Navigate to next window
        if self.parent():
            self.parent().setCurrentIndex(1)


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
        login_button.clicked.connect(self.login)  # Connect the login functionality
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

        # Sign-Up Button
        signup_button = QPushButton("Don't have an account? Sign Up")
        signup_button.setFont(QFont("Artifakt Element", 14, QFont.Weight.Bold))
        signup_button.setStyleSheet("""
            color: #002147;
            font-size: 14px;
            background: transparent;
            border: none;
            text-align: center;
            margin-top: 10px;
            font-weight: bold;
        """)
        signup_button.setCursor(Qt.CursorShape.PointingHandCursor)  # Change cursor to pointer on hover
        signup_button.clicked.connect(self.open_signup_dialog)  # Connect to the sign-up dialog
        login_layout.addWidget(signup_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addWidget(login_frame)

        self.main_layout.addWidget(login_frame)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        hashed_password = hash_password(password)  # Ensure you define the hash_password function
        cursor.execute(
            "SELECT * FROM general_data WHERE username = ? AND password = ?",
            (username, hashed_password)
        )
        user = cursor.fetchone()

        if user and user[10]:  # Account approved (column approved is at index 8)
            if user[11] == 'Admin':  # Role column is at index 9
                self.open_admin_panel()
            elif user[11] == 'Teacher':
                teacher_data = {
                    'username': user[8],  # Assuming user[7] is the username
                    'name': user[1],  # Assuming user[0] is the name
                    'matric_no': user[2],   # Assuming user[2] is the matric number
                    'department': user[4],  # Assuming user[3] is the department
                    'age': user[5],  # Assuming user[5] is the age
                    'phone_number': user[6],  # Assuming user[5] is the phone number
                    'email': user[7],  # Assuming user[7] is the email
                }
                self.open_teacher_dashboard(teacher_data)
            else:
                student_data = {
                    'name': user[1],  # Assuming user[0] is the name
                    'matric_no': user[2],  # Assuming user[1] is the matric number
                    'level': user[3],  # Assuming user[2] is the level
                    'department': user[4],  # Assuming user[3] is the department
                    'age': user[5],  # Assuming user[5] is the age
                    'phone_number': user[6],  # Assuming user[5] is the phone number
                    'email': user[7],  # Assuming user[7] is the email
                }
                self.open_student_dashboard(student_data)
        else:
            QMessageBox.warning(self, 'Error', 'Invalid credentials or account not approved')

    def open_admin_panel(self):
        dialog = AdminPanel()
        dialog.exec()

    def open_student_dashboard(self, student_data):
        dashboard = StudentDashboard(student_data)
        dashboard.exec()

    def open_teacher_dashboard(self, teacher_data):
        dashboard = TeacherDashboard(teacher_data)
        dashboard.exec()

    def open_forgot_password_dialog(self):
        forgot_password_dialog = ForgotPasswordDialog(self)  # Pass the parent for modality
        forgot_password_dialog.exec()  # Show the dialog modally

    def open_signup_dialog(self):
        """Opens the sign-up dialog."""
        signup_dialog = CreateAccountDialog(self)  # Instantiate the dialog
        signup_dialog.exec()  # Show the dialog modally

    def toggle_password_visibility(self):
        if self.password_input.echoMode() == QLineEdit.EchoMode.Password:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_password_btn.setText("🙈")
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_password_btn.setText("👁")

    def create_info_section(self):
        info_frame = QFrame()
        info_frame.setStyleSheet("background-color: #002147; border-radius: 25px;")
        info_layout = QVBoxLayout(info_frame)
        info_layout.setContentsMargins(40, 60, 40, 60)

        info_heading = QLabel("Revolutionizing Learning")
        info_heading.setFont(QFont("Artifakt Element Medium", 20, QFont.Weight.Bold))
        info_heading.setStyleSheet("color: white; margin-bottom: 10px;")
        info_layout.addWidget(info_heading, alignment=Qt.AlignmentFlag.AlignTop)

        info_subtitle = QLabel(
            "Discover a world of opportunities through our cutting-edge platform. "
            "Manage your courses, collaborate with peers, and excel in your academic journey."
        )
        info_subtitle.setFont(QFont("Artifakt Element Medium", 14))
        info_subtitle.setStyleSheet("color: white;")
        info_subtitle.setWordWrap(True)
        info_layout.addWidget(info_subtitle, alignment=Qt.AlignmentFlag.AlignTop)

        placeholder_image = QLabel("🎓")
        placeholder_image.setFont(QFont("Artifakt Element Medium", 100))
        placeholder_image.setStyleSheet("color: white;")
        info_layout.addWidget(placeholder_image, alignment=Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addWidget(info_frame)


class ForgotPasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Forgot Password")
        self.resize(400, 300)

        # Layout
        layout = QVBoxLayout()

        # Instruction
        instruction_label = QLabel(
            "Enter your username and answer the security question to reset your password."
        )
        instruction_label.setWordWrap(True)
        layout.addWidget(instruction_label)

        # Username input
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)

        # Security question (e.g., predefined question for simplicity)
        self.security_question_label = QLabel("What is your favorite color?")
        layout.addWidget(self.security_question_label)

        # Answer input
        self.answer_input = QLineEdit(self)
        self.answer_input.setPlaceholderText("Answer")
        layout.addWidget(self.answer_input)

        # New password input
        self.new_password_input = QLineEdit(self)
        self.new_password_input.setPlaceholderText("New Password")
        self.new_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.new_password_input)

        # Confirm password input
        self.confirm_password_input = QLineEdit(self)
        self.confirm_password_input.setPlaceholderText("Confirm New Password")
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.confirm_password_input)

        # Reset password button
        self.reset_password_button = QPushButton("Reset Password")
        self.reset_password_button.clicked.connect(self.reset_password)
        layout.addWidget(self.reset_password_button)

        # Set layout
        self.setLayout(layout)

    def reset_password(self):
        username = self.username_input.text()
        answer = self.answer_input.text()
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()

        # Validation
        if not username or not answer or not new_password or not confirm_password:
            QMessageBox.warning(self, "Error", "All fields are required.")
            return

        if new_password != confirm_password:
            QMessageBox.warning(self, "Error", "Passwords do not match.")
            return

        try:
            cursor.execute("SELECT security_answer FROM general_data WHERE username = ?", (username,))
            result = cursor.fetchone()

            if result and result[0].lower() == answer.lower():  # Case-insensitive comparison
                hashed_password = hash_password(new_password)
                cursor.execute(
                    "UPDATE general_data SET password = ? WHERE username = ?",
                    (hashed_password, username),
                )
                conn.commit()
                QMessageBox.information(self, "Success", "Password has been reset successfully.")
                self.accept()
            else:
                QMessageBox.warning(self, "Error", "Invalid username or security answer.")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error: {e}")
        finally:
            conn.close()


class CreateAccountDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Dialog window properties
        self.setWindowTitle("Create Account")

        # Form layout
        form_layout = QFormLayout()

        # Name input
        self.name_input = QLineEdit(self)
        form_layout.addRow("Name:", self.name_input)

        # Matric Number input
        self.matric_input = QLineEdit(self)
        form_layout.addRow("Matric Number:", self.matric_input)

        # Department input
        self.department_input = QLineEdit(self)
        form_layout.addRow("Department:", self.department_input)

        # Level input
        self.level_input = QLineEdit(self)
        form_layout.addRow("Level:", self.level_input)

        # Age Input
        self.age_input = QLineEdit(self)
        form_layout.addRow("Age:", self.age_input)

        # Add Phone number
        self.phone_number = QLineEdit(self)
        form_layout.addRow("Phone number:", self.phone_number)

        # Add Email
        self.email = QLineEdit(self)
        form_layout.addRow("Email:", self.email)

        # Username input
        self.username_input = QLineEdit(self)
        form_layout.addRow("Username:", self.username_input)

        # Password input (set to password mode)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("Password:", self.password_input)

        # Role dropdown
        self.role_input = QComboBox(self)
        self.role_input.addItems(["Student", "Admin", "Teacher"])
        form_layout.addRow("Role:", self.role_input)

        # Submit button
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.save_to_database)
        form_layout.addWidget(self.submit_button)

        # Set layout
        self.setLayout(form_layout)

    def save_to_database(self):
        # Collect input data
        name = self.name_input.text()
        matric_no = self.matric_input.text()
        level = self.level_input.text()
        department = self.department_input.text()
        age = self.age_input.text()  # Example fixed age value
        phone_number = self.phone_number.text()  # Example fixed phone number
        email = self.email.text()
        username = self.username_input.text()
        password = self.password_input.text()
        approved = False  # Example approval status
        role = self.role_input.currentText()

        # Validation
        if not all([name, matric_no, department, level, role]):
            QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        hashed_password = hash_password(password)

        try:
            cursor.execute('''
            INSERT INTO general_data (name, matric_no, level, department, age, phone_number, email, username, password, approved, role)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, matric_no, level, department, age, phone_number, email, username, hashed_password, approved, role))
            conn.commit()
            QMessageBox.information(self, "Success", "Wait for Account Approval")
            self.accept()
        except sqlite3.IntegrityError as e:
            QMessageBox.warning(self, "Database Error", f"Error: {e}")
        finally:
            conn.close()


class AdminPanel(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("University Admin Panel")
        self.setGeometry(100, 100, 1080, 720)

        # Database connection
        self.conn = sqlite3.connect("assets/school_database.db")

        # White background for the dialog
        self.setStyleSheet("""
            QWidget {
                background-color: white; 
                color: black;
            }
        """)

        # Main layout
        main_layout = QHBoxLayout(self)

        # Sidebar
        self.sidebar = self.create_sidebar()
        main_layout.addWidget(self.sidebar)

        # Content area
        self.content_area = QStackedWidget()
        main_layout.addWidget(self.content_area, 1)

        # Add modules to the content area
        self.add_modules()

    def create_sidebar(self):
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Navigation items
        nav_items = [
            ("Dashboard", self.show_dashboard),
            ("User Management", self.show_user_management),
            ("Programs and Courses", self.show_program_course_management),
            ("Attendance", self.show_attendance_management),
            ("Analytics", self.show_analytics),
            ("Notifications", self.show_notifications),
            ("Logout", self.logout),
        ]

        self.sidebar_buttons = []
        for item_name, callback in nav_items:
            button = QPushButton(item_name)
            button.setFont(QFont("Artifakt Element Medium", 12))
            button.setStyleSheet("""
                QPushButton {
                    padding: 10px 20px;  /* Add padding around the text */ 
                    border-radius: 5px; /* Optional: Add rounded corners */
                    background-color: #002147;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #024ca1;  /* Optional: Add hover effect */
                }
            """)
            button.clicked.connect(callback)
            self.sidebar_buttons.append(button)
            sidebar_layout.addWidget(button)

        return sidebar

    def add_modules(self):
        # Create instances of all modules
        self.dashboard = DashboardAnalytics(self.conn)
        self.user_management = UserManagementModule(self.conn)
        self.program_course_management = ProgramCourseManagement(self.conn)
        self.attendance_management = AttendanceAnalytics(self.conn)
        self.notifications = Notifications()
        self.analytics = Analytics(self.conn)

        # Add modules to the content area
        self.content_area.addWidget(self.dashboard)
        self.content_area.addWidget(self.user_management)
        self.content_area.addWidget(self.program_course_management)
        self.content_area.addWidget(self.attendance_management)
        self.content_area.addWidget(self.analytics)
        self.content_area.addWidget(self.notifications)

    # Navigation functions
    def show_dashboard(self):
        self.content_area.setCurrentWidget(self.dashboard)

    def show_user_management(self):
        self.content_area.setCurrentWidget(self.user_management)

    def show_program_course_management(self):
        self.content_area.setCurrentWidget(self.program_course_management)

    def show_attendance_management(self):
        self.content_area.setCurrentWidget(self.attendance_management)

    def show_analytics(self):
        self.content_area.setCurrentWidget(self.analytics)

    def show_notifications(self):
        self.content_area.setCurrentWidget(self.notifications)

    def logout(self):
        reply = QMessageBox.question(self, "Logout", "Are you sure you want to logout?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.conn.close()
            self.close()


class DashboardAnalytics(QWidget):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn

        # Create a QFormLayout
        form_layout = QFormLayout()

        # Reduce spacing between rows
        form_layout.setHorizontalSpacing(10)
        form_layout.setVerticalSpacing(5)

        # Header
        header = QLabel("Dashboard Overview")
        header.setFont(QFont("Artifakt Element", 20, QFont.Weight.Bold))
        header.setStyleSheet("margin: 5px 0px;")  # Reduce top and bottom margin
        form_layout.addRow(header)  # Add the header as the first row

        # Add metrics to the form
        metrics = self.get_dashboard_metrics()
        for metric_name, value in metrics.items():
            metric_label = QLabel(metric_name)
            metric_label.setFont(QFont("Artifakt Element", 12))

            value_label = QLabel(value)
            value_label.setFont(QFont("Artifakt Element", 12))

            form_layout.addRow(metric_label, value_label)

        # Set the layout for the widget
        self.setLayout(form_layout)

    def get_dashboard_metrics(self):
        # Fetch data for dashboard metrics
        cursor = self.conn.cursor()
        metrics = {}

        cursor.execute("SELECT COUNT(*) FROM general_data WHERE role='Student'")
        metrics["Total Students"] = str(cursor.fetchone()[0])

        cursor.execute("SELECT COUNT(*) FROM general_data WHERE role='Teacher'")
        metrics["Total Teachers"] = str(cursor.fetchone()[0])

        cursor.execute("SELECT COUNT(*) FROM Courses")
        metrics["Total Courses"] = str(cursor.fetchone()[0])

        cursor.execute("""
            SELECT AVG(Attendance.status = 'Present') * 100 FROM Attendance
        """)
        attendance_rate = cursor.fetchone()[0]
        metrics["Attendance Rate"] = f"{attendance_rate:.2f}%" if attendance_rate else "N/A"

        return metrics



class UserManagementModule(QWidget):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        layout = QVBoxLayout(self)

        # Header
        header_label = QLabel("User Management")
        header_label.setFont(QFont("Artifakt Element", 20))
        header_label.setStyleSheet("margin: 10px;")
        header_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(header_label)

        # Horizontal Button Bar
        button_bar = QHBoxLayout()

        self.add_user_button = QPushButton("Add User")
        self.add_user_button.clicked.connect(self.add_user)
        self.add_user_button.setStyleSheet(
            "color: white; background-color: #002147; padding: 6px 12px; border-radius: 4px;"
        )
        button_bar.addWidget(self.add_user_button)

        self.delete_user_button = QPushButton("Delete User")
        self.delete_user_button.clicked.connect(self.delete_user)
        self.delete_user_button.setStyleSheet(
            "color: white; background-color: #002147; padding: 6px 12px; border-radius: 4px;"
        )
        button_bar.addWidget(self.delete_user_button)

        self.approve_user_button = QPushButton("Approve User")
        self.approve_user_button.clicked.connect(self.approve_user)
        self.approve_user_button.setStyleSheet(
            "color: white; background-color: #002147; padding: 6px 12px; border-radius: 4px;"
        )
        button_bar.addWidget(self.approve_user_button)

        layout.addLayout(button_bar)

        # Table Setup
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(6)
        self.users_table.setHorizontalHeaderLabels(["Name", "Email", "Role", "Last Active", "Date Added", "Actions"])
        self.users_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.users_table.setAlternatingRowColors(True)

        # Apply the same styling as the courses table
        self.users_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #D5D8DC;
                gridline-color: #D5D8DC;
                font-family: 'Artifakt Element Medium';
            }
            QTableWidget::item {
                padding: 10px;
            }
            QHeaderView::section {
                background-color: #ECF0F1;
                font-weight: bold;
                font-size: 12px;
                padding: 5px;
                border: 1px solid #BDC3C7;
            }
            QTableWidget::item:selected {
                background-color: #D6EAF8;
            }
            QTableWidget::item {
                background-color: #F9F9F9;
            }
            QTableWidget::item:alternate {
                background-color: #002147;
                color: #F9F9F9;
            }
        """)

        layout.addWidget(self.users_table)

        self.populate_users_table()

    def populate_users_table(self):
        cursor = self.conn.cursor()

        # Fetch user data from the database
        cursor.execute("SELECT username, email, role, last_active, date_added FROM user_management")
        rows = cursor.fetchall()

        self.users_table.setRowCount(len(rows))  # Set row count based on the number of users

        for row_idx, row_data in enumerate(rows):
            self.users_table.setRowHeight(row_idx, 40)
            # Name and Email
            name_item = QTableWidgetItem(row_data[0])
            email_item = QTableWidgetItem(row_data[1])

            # Role with style
            role_label = QLabel(row_data[2])
            if row_data[2] == "Admin":
                role_label.setStyleSheet("color: white; background-color: #1976D2;"
                                         "padding: 4px 8px; border-radius: 4px;")
            elif row_data[2] == "Student":
                role_label.setStyleSheet("color: black; background-color: #C8E6C9;"
                                         "padding: 4px 8px; border-radius: 4px;")
            elif row_data[2] == "Teacher":
                role_label.setStyleSheet("color: white; background-color: #FF8A65;"
                                         "padding: 4px 8px; border-radius: 4px;")
            role_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Last Active and Date Added
            last_active_item = QTableWidgetItem(row_data[3] or "Never")
            date_added_item = QTableWidgetItem(row_data[4])

            # Action buttons (e.g., Edit)
            action_layout = QHBoxLayout()
            edit_button = QPushButton("Edit")
            edit_button.setIcon(QIcon.fromTheme("edit"))
            edit_button.setStyleSheet("color: #4CAF50; padding: 2px;")
            edit_button.clicked.connect(lambda _, username=row_data[0]: self.update_last_active(username))
            action_layout.addWidget(edit_button, alignment=Qt.AlignmentFlag.AlignCenter)

            # Insert values into table cells
            self.users_table.setItem(row_idx, 0, name_item)
            self.users_table.setItem(row_idx, 1, email_item)
            self.users_table.setCellWidget(row_idx, 2, role_label)
            self.users_table.setItem(row_idx, 3, last_active_item)
            self.users_table.setItem(row_idx, 4, date_added_item)
            self.users_table.setCellWidget(row_idx, 5, edit_button)

    def add_user(self):
        dialog = AddUserDialog()
        if dialog.exec():
            self.populate_users_table()

    def delete_user(self):
        dialog = DeleteUserDialog()
        if dialog.exec():
            self.populate_users_table()

    def approve_user(self):
        dialog = ApproveUserDialog()
        if dialog.exec():
            self.populate_users_table()


class ApproveUserDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Approve User by Matric Number")
        self.setGeometry(200, 200, 400, 300)
        layout = QFormLayout()

        # Matric number input field
        self.matric_number_input = QLineEdit()
        layout.addRow("Matric Number to Approve:", self.matric_number_input)

        # Approve button
        self.approve_button = QPushButton("Approve User")
        self.approve_button.clicked.connect(self.approve_user_in_db)
        layout.addRow(self.approve_button)
        self.setLayout(layout)

    def approve_user_in_db(self):
        matric_number = self.matric_number_input.text()

        # Ensure matric number is provided
        if not matric_number:
            QMessageBox.warning(self, "Error", "Matric number is required.")
            return

        # Database connection (assuming `conn` and `cursor` are pre-defined globally)
        try:
            # Attempt to approve user in the database
            cursor.execute("UPDATE general_data SET approved = 1 WHERE matric_no = ?", (matric_number,))
            conn.commit()  # Commit the change to the database

            # Check if any rows were affected (user found and updated)
            if cursor.rowcount == 0:
                QMessageBox.warning(self, "Error", "User not found.")
            else:
                QMessageBox.information(self, "Success", "User approved successfully.")
                self.accept()  # Close the dialog upon successful approval

        except sqlite3.Error as e:
            # Display database error if any occurs
            QMessageBox.warning(self, "Error", f"Database error: {e}")


# Dialog for adding a user
class AddUserDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add User")
        self.setGeometry(200, 200, 400, 300)
        layout = QFormLayout()

        # Input fields
        self.name_input = QLineEdit()
        self.matric_no_input = QLineEdit()
        self.department_input = QLineEdit()
        self.level_input = QComboBox(self)
        self.level_input.addItems(["100", "200", "300", "400", "500"])
        self.age_input = QLineEdit()
        self.age_input.setValidator(QIntValidator(12, 75, self))  # Age restricted to 12-75
        self.phone_number_input = QLineEdit()
        self.email_input = QLineEdit()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.role_input = QComboBox(self)
        self.role_input.addItems(["Student", "Teacher", "Admin"])

        # Add input fields to layout
        layout.addRow("Name:", self.name_input)
        layout.addRow("Matric No:", self.matric_no_input)
        layout.addRow("Department:", self.department_input)
        layout.addRow("Level:", self.level_input)
        layout.addRow("Age:", self.age_input)
        layout.addRow("Phone Number:", self.phone_number_input)
        layout.addRow("Email:", self.email_input)
        layout.addRow("Username:", self.username_input)
        layout.addRow("Password:", self.password_input)
        layout.addRow("Role:", self.role_input)

        # Add button
        self.add_button = QPushButton("Add User")
        self.add_button.clicked.connect(self.add_user_to_db)
        layout.addRow(self.add_button)

        self.setLayout(layout)

    def add_user_to_db(self):
        # Collect input values
        name = self.name_input.text()
        matric_no = self.matric_no_input.text()
        department = self.department_input.text()
        level = self.level_input.currentText()
        age = self.age_input.text()
        phone_number = self.phone_number_input.text()
        email = self.email_input.text()
        username = self.username_input.text()
        password = self.password_input.text()
        role = self.role_input.currentText()

        # Validate required fields
        if not all([name, matric_no, department, level, age, phone_number, email, username, password, role]):
            QMessageBox.warning(self, "Error", "All fields are required.")
            return

        # Validate age as an integer
        try:
            age = int(age)
        except ValueError:
            QMessageBox.warning(self, "Error", "Age must be a valid integer.")
            return

        # Hash the password
        hashed_password = hash_password(password)

        try:
            # Check for existing username or email
            cursor.execute("SELECT * FROM general_data WHERE username = ? OR email = ?", (username, email))
            existing_user = cursor.fetchone()
            if existing_user:
                QMessageBox.warning(self, "Error", "Username or email already exists.")
                return

            # Insert the new user into the database
            cursor.execute(
                "INSERT INTO general_data "
                "(name, matric_no, level, department, age, phone_number, email, username, password, approved, role) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (name, matric_no, level, department, age, phone_number, email, username, hashed_password, 1, role)
                # Automatically approve for admin
            )
            conn.commit()

            QMessageBox.information(self, "Success", "User added successfully.")
            self.accept()

        except sqlite3.Error as e:
            QMessageBox.warning(self, "Error", f"Database error: {e}")


# Dialog for deleting a user
class DeleteUserDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete User")
        self.setGeometry(200, 200, 400, 200)
        layout = QFormLayout()

        self.username_input = QLineEdit()
        layout.addRow("Username to Delete:", self.username_input)

        self.delete_button = QPushButton("Delete User")
        self.delete_button.clicked.connect(self.delete_user_from_db)
        layout.addRow(self.delete_button)
        self.setLayout(layout)

    def delete_user_from_db(self):
        username = self.username_input.text()
        if not username:
            QMessageBox.warning(self, "Error", "Username is required.")
            return

        try:
            cursor.execute("DELETE FROM general_data WHERE username = ?", (username,))
            conn.commit()
            if cursor.rowcount == 0:
                QMessageBox.warning(self, "Error", "User not found.")
            else:
                QMessageBox.information(self, "Success", "User deleted successfully.")
                self.accept()
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Error", f"Database error: {e}")


class ProgramCourseManagement(QWidget):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Header
        header_label = QLabel("Program and Course Management")
        header_label.setFont(QFont("Artifakt Element Medium", 20))
        header_label.setStyleSheet("color: #2C3E50; margin-bottom: 20px;")
        layout.addWidget(header_label)

        # Sorting Options
        sort_layout = QHBoxLayout()
        sort_label = QLabel("Sort by:")
        sort_label.setFont(QFont("Artifakt Element Medium", 12))
        sort_label.setStyleSheet("margin-right: 10px;")

        self.sort_criteria = QComboBox()
        self.sort_criteria.addItems(["Department", "Level", "Course Unit"])
        self.sort_order = QComboBox()
        self.sort_order.addItems(["Ascending", "Descending"])

        sort_button = QPushButton("Sort")
        sort_button.setStyleSheet("""
            QPushButton {
                background-color: #002147;
                color: white;
                font-weight: bold;
                padding: 5px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #024CA1;
            }
        """)
        sort_button.clicked.connect(self.sort_table)

        sort_layout.addWidget(sort_label)
        sort_layout.addWidget(self.sort_criteria)
        sort_layout.addWidget(self.sort_order)
        sort_layout.addWidget(sort_button)

        layout.addLayout(sort_layout)

        # Courses Table
        self.courses_table = QTableWidget()
        self.courses_table.setColumnCount(7)
        self.courses_table.setHorizontalHeaderLabels([
            "Course Code", "Course Name", "Course Unit",
            "Department", "Session", "Semester", "Level"
        ])
        self.courses_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.courses_table.setAlternatingRowColors(True)
        self.courses_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #D5D8DC;
                gridline-color: #D5D8DC;
                font-family: 'Artifakt Element Medium';
            }
            QTableWidget::item {
                padding: 10px;
            }
            QHeaderView::section {
                background-color: #ECF0F1;
                font-weight: bold;
                font-size: 12px;
                padding: 5px;
                border: 1px solid #BDC3C7;
            }
            QTableWidget::item:selected {
                background-color: #D6EAF8;
            }
            QTableWidget::item {
                background-color: #F9F9F9;
            }
            QTableWidget::item:alternate {
                background-color: #002147;
                color: #F9F9F9;
            }
        """)
        layout.addWidget(self.courses_table)

        self.populate_courses_table()

        # Add course Button
        add_course_button = QPushButton("Add Course")
        add_course_button.setStyleSheet("""
            QPushButton {
                background-color: #002147; 
                color: white; 
                color: white;
                font-weight: bold;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #024CA1;
            }
        """)
        add_course_button.clicked.connect(self.open_add_course_dialog)
        layout.addWidget(add_course_button)

        # Save Changes Button
        save_button = QPushButton("Save Changes")
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #002147; 
                color: white; 
                color: white;
                font-weight: bold;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #024CA1;
            }
        """)
        save_button.clicked.connect(self.save_changes)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def populate_courses_table(self):
        """Populate the table with data from the database."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT course_code, course_name, course_unit, department, session, semester, level FROM Courses")
        rows = cursor.fetchall()

        self.courses_table.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable)
                self.courses_table.setItem(row_idx, col_idx, item)

    def sort_table(self):
        """Sort the table based on selected criteria and order."""
        criteria = self.sort_criteria.currentText()
        order = self.sort_order.currentText()

        # Mapping column index based on criteria
        column_mapping = {"Department": 3, "Level": 6, "Course Unit": 2}
        column_index = column_mapping[criteria]

        # Get all rows and their data
        rows = []
        for row in range(self.courses_table.rowCount()):
            row_data = [
                self.courses_table.item(row, col).text()
                for col in range(self.courses_table.columnCount())
            ]
            rows.append(row_data)

        # Sort rows based on selected criteria and order
        rows.sort(key=lambda x: x[column_index], reverse=(order == "Descending"))

        # Re-populate the table with sorted data
        self.courses_table.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable)
                self.courses_table.setItem(row_idx, col_idx, item)

    def save_changes(self):
        """Save changes from the table to the database."""
        try:
            cursor = self.conn.cursor()
            for row in range(self.courses_table.rowCount()):
                updated_values = []
                for col in range(self.courses_table.columnCount()):
                    updated_values.append(self.courses_table.item(row, col).text())

                update_query = """
                    UPDATE Courses
                    SET course_name = ?, course_unit = ?, department = ?, session = ?, semester = ?, level = ?
                    WHERE course_code = ?
                """
                # Reorder the updated values to match the query
                cursor.execute(update_query, (*updated_values[1:], updated_values[0]))

            self.conn.commit()
            QMessageBox.information(self, "Info", "Changes saved successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while saving changes: {e}")

    def open_add_course_dialog(self):
        # Open the AddCourseDialog
        dialog = AddCourseDialog()
        dialog.exec()


# Dialog for adding a course
class AddCourseDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Courses for Department and Level")
        self.setGeometry(200, 200, 600, 600)

        # Connect to the database
        try:
            self.conn = sqlite3.connect("assets/school_database.db")  # Replace with actual path
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"Could not connect to database: {e}")
            self.close()

        # Main layout
        self.layout = QVBoxLayout()

        # Level Selection Field
        self.level_input = QComboBox()
        self.level_input.addItems(["100L", "200L", "300L", "400L", "500L"])

        # Department Selection Field
        self.department_input = QComboBox()
        self.department_input.addItems([
            "Biochemistry", "Industrial Chemistry", "Microbiology", "Applied Mathematics", "Statistics",
            "Biotechnology", "Computer Science", "Information Technology", "Mechanical Engineering",
            "Mechatronics Engineering", "Civil Engineering", "Biomedical Engineering",
            "Telecommunication Engineering", "Electrical/Electronics Engineering",
            "Agricultural and Bioresources Engineering", "Human Resources Management", "Accounting",
            "Economics", "Marketing", "Business Computing", "International Business",
            "Project Management Tech", "Transport Management and Logistics", "Food Technology",
            "Nutrition and Dietetics"
        ])

        # Session and Semester Fields
        self.session_input = QLineEdit()
        self.semester_input = QComboBox()
        self.semester_input.addItems(["1st Semester", "2nd Semester"])

        self.layout.addWidget(QLabel("Department:"))
        self.layout.addWidget(self.department_input)
        self.layout.addWidget(QLabel("Level:"))
        self.layout.addWidget(self.level_input)
        self.layout.addWidget(QLabel("Session (e.g., 2023/2024):"))
        self.layout.addWidget(self.session_input)
        self.layout.addWidget(QLabel("Semester:"))
        self.layout.addWidget(self.semester_input)

        # Courses container layout
        self.courses_layout = QVBoxLayout()
        self.course_inputs = []

        # Scroll area for course fields
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_widget.setLayout(self.courses_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        self.layout.addWidget(scroll_area)

        # Button to add more courses dynamically
        self.add_more_button = QPushButton("Add More Courses")
        self.add_more_button.clicked.connect(self.add_course_fields)
        self.layout.addWidget(self.add_more_button)

        # Save Button
        self.add_button = QPushButton("Save Courses")
        self.add_button.clicked.connect(self.add_courses_to_db)
        self.layout.addWidget(self.add_button)

        self.setLayout(self.layout)

        # Add initial course fields
        for _ in range(1):  # Add three rows by default
            self.add_course_fields()

    def add_course_fields(self):
        # Dynamic addition of course rows
        course_layout = QHBoxLayout()
        course_name = QLineEdit()
        course_code = QLineEdit()
        course_unit = QSpinBox()
        course_unit.setRange(1, 6)  # Assuming course units range from 1 to 6

        course_layout.addWidget(QLabel("Course Code:"))
        course_layout.addWidget(course_code)
        course_layout.addWidget(QLabel(f"Course Name:"))
        course_layout.addWidget(course_name)
        course_layout.addWidget(QLabel("Units:"))
        course_layout.addWidget(course_unit)

        # Store inputs for later retrieval
        self.course_inputs.append((course_name, course_code, course_unit))
        self.courses_layout.addLayout(course_layout)

    def add_courses_to_db(self):
        department = self.department_input.currentText().strip()
        level = self.level_input.currentText().strip()
        session = self.session_input.text().strip()
        semester = self.semester_input.currentText().strip()

        # Validate required fields
        if not department or not level or not session or not semester:
            QMessageBox.warning(self, "Error", "All fields (Department, Level, Session, and Semester) are required.")
            return

        # Gather course information
        courses = []
        for course_name_input, course_code_input, course_unit_input in self.course_inputs:
            course_name = course_name_input.text().strip()
            course_code = course_code_input.text().strip()
            course_unit = course_unit_input.value()

            if course_name and course_code:
                courses.append((department, level, session, semester, course_name, course_code, course_unit))

        if not courses:
            QMessageBox.warning(self, "Error", "At least one course with valid details is required.")
            return

        try:
            # Insert courses into the database
            query = '''
                INSERT INTO Courses (department, level, session, semester, course_name, course_code, course_unit)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            '''
            self.cursor.executemany(query, courses)  # Insert multiple rows at once
            self.conn.commit()

            QMessageBox.information(self, "Success", "Courses added successfully.")
            self.accept()

        except sqlite3.Error as e:
            QMessageBox.warning(self, "Error", f"Database error: {e}")

    def closeEvent(self, event):
        # Close database connection when dialog is closed
        if self.conn:
            self.conn.close()


class AttendanceAnalytics(QWidget):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        layout = QVBoxLayout(self)

        # Header
        header = QLabel("Attendance Analytics")
        header.setFont(QFont("Artifakt Element Medium", 20))
        layout.addWidget(header)

        # Attendance Table
        self.attendance_table = QTableWidget()
        self.attendance_table.setColumnCount(6)
        self.attendance_table.setHorizontalHeaderLabels([
            "Matric No.", "Course", "Level", "Department", "Date", "Status"
        ])
        layout.addWidget(self.attendance_table)

        self.populate_attendance_table()

    def populate_attendance_table(self):
        cursor = self.conn.cursor()

        # Query to retrieve attendance data with course name, level, and department
        query = """
        SELECT 
            Attendance.matric_no, 
            Courses.course_name, 
            general_data.level, 
            general_data.department, 
            Attendance.date, 
            Attendance.status
        FROM Attendance
        INNER JOIN general_data ON Attendance.matric_no = general_data.matric_no
        INNER JOIN Courses ON Attendance.course_code = Courses.course_code
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        self.attendance_table.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, value in enumerate(row_data):
                self.attendance_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))


class Analytics(QWidget):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        layout = QVBoxLayout(self)

        # Header
        header = QLabel("Analytics Overview")
        header.setFont(QFont("Artifakt Element Medium", 20))
        layout.addWidget(header)

        # Subheader
        subheader = QLabel("Key Metrics and Visualizations")
        subheader.setFont(QFont("Arial", 14))
        layout.addWidget(subheader)

        # Metrics Grid
        metrics_grid = QGridLayout()
        layout.addLayout(metrics_grid)

        metrics = self.get_analytics_metrics()
        for i, (metric_name, value) in enumerate(metrics.items()):
            group = QGroupBox(metric_name)
            group_layout = QVBoxLayout(group)
            value_label = QLabel(value)
            value_label.setFont(QFont("Arial", 12))
            value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            group_layout.addWidget(value_label)
            metrics_grid.addWidget(group, i // 2, i % 2)

        # Visualization area
        visualizations_group = QGroupBox("Performance Overview")
        visualizations_layout = QVBoxLayout(visualizations_group)

        # Attendance Rate Chart
        attendance_chart = self.create_attendance_chart()
        visualizations_layout.addWidget(attendance_chart)

        # Grades Distribution Chart
        grades_chart_pie, grades_chart_bar = self.create_grades_chart()  # Unpack the tuple

        # Add each chart to the visualizations layout
        visualizations_layout.addWidget(grades_chart_pie)  # Add the Matplotlib pie chart
        visualizations_layout.addWidget(grades_chart_bar)  # Add the PyQtGraph bar chart

        layout.addWidget(visualizations_group)  # Add the visualization group to the main layout

    def get_analytics_metrics(self):
        cursor = self.conn.cursor()
        metrics = {}

        cursor.execute("SELECT COUNT(*) FROM general_data WHERE role='Student'")
        metrics["Total Students"] = str(cursor.fetchone()[0])

        cursor.execute("SELECT COUNT(*) FROM general_data WHERE role='Teacher'")
        metrics["Total Teachers"] = str(cursor.fetchone()[0])

        cursor.execute("SELECT COUNT(*) FROM Courses")
        metrics["Total Courses"] = str(cursor.fetchone()[0])

        cursor.execute("""
            SELECT AVG(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) * 100 FROM Attendance
        """)
        attendance_rate = cursor.fetchone()[0]
        metrics["Attendance Rate"] = f"{attendance_rate:.2f}%" if attendance_rate else "N/A"

        return metrics

    def create_attendance_chart(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT date, 
                   COUNT(CASE WHEN status = 'Present' THEN 1 END) AS present_count,
                   COUNT(CASE WHEN status = 'Absent' THEN 1 END) AS absent_count
            FROM Attendance
            GROUP BY date
        """)
        data = cursor.fetchall()
        dates, present, absent = zip(*data) if data else ([], [], [])

        # Create a matplotlib chart
        figure = Figure(figsize=(6, 3))
        canvas = FigureCanvasQTAgg(figure)
        ax = figure.add_subplot(111)
        ax.plot(dates, present, label="Present", marker="o")
        ax.plot(dates, absent, label="Absent", marker="x", linestyle="--")
        ax.set_title("Attendance Trend")
        ax.set_xlabel("Dates")
        ax.set_ylabel("Count")
        ax.legend()
        ax.grid(True)

        return canvas

    def create_grades_chart(self):
        # Query the database to count the number of students per grade
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT grade, COUNT(*)
            FROM student_grades
            GROUP BY grade
        """)
        data = cursor.fetchall()

        # Extract grades and counts
        grades, counts = zip(*data) if data else ([], [])

        # Matplotlib: Pie Chart for Grade Distribution
        pie_figure = Figure(figsize=(6, 3))  # Figure for pie chart
        pie_canvas = FigureCanvasQTAgg(pie_figure)
        pie_ax = pie_figure.add_subplot(111)
        pie_ax.pie(
            counts,
            labels=grades,
            autopct="%1.1f%%",
            startangle=90,
            colors=["#4CAF50", "#2196F3", "#FFC107", "#FF5722", "#E91E63", "#9C27B0"]
        )
        pie_ax.set_title("Grades Distribution (Pie Chart)")

        # PyQtGraph: Bar Chart for Grade Distribution
        bar_widget = PlotWidget(title="Grades Distribution (Bar Chart)")
        bar_widget.setBackground("w")
        bar_widget.setLabel("bottom", "Grades")
        bar_widget.setLabel("left", "Number of Students")
        bar_widget.showGrid(x=True, y=True, alpha=0.3)

        # Generate bar chart data
        x = list(range(len(grades)))  # X-axis positions
        bar_item = BarGraphItem(
            x=x,
            height=counts,
            width=0.5,
            brush="#2196F3"  # Bar color
        )
        bar_widget.addItem(bar_item)

        # Set X-axis ticks to grade labels
        bar_widget.getPlotItem().getAxis("bottom").setTicks([list(zip(x, grades))])

        return pie_canvas, bar_widget


class Notifications(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # Header
        header = QLabel("Notifications")
        header.setFont(QFont("Arial", 20))
        layout.addWidget(header)

        # Example placeholder
        layout.addWidget(QLabel("No new notifications."))


class StudentDashboard(QDialog):
    def __init__(self, student_data):
        super().__init__()
        self.setWindowTitle(f"{student_data['name']} - Teacher Dashboard")
        self.setGeometry(200, 200, 500, 400)

        layout = QVBoxLayout()

        # Display student information
        self.student_data = student_data
        name_label = QLabel(f"Name: {self.student_data['name']}")
        matric_no_label = QLabel(f"Matric Number: {self.student_data['matric_no']}")
        level_label = QLabel(f"Level: {self.student_data['level']}")
        department_label = QLabel(f"Department: {self.student_data['department']}")
        phone_label = QLabel(f"Phone Number: {self.student_data['phone_number']}")

        # Add student info labels to the layout
        layout.addWidget(name_label)
        layout.addWidget(matric_no_label)
        layout.addWidget(level_label)
        layout.addWidget(department_label)
        layout.addWidget(phone_label)

        # Add action buttons
        self.course_registration_button = QPushButton("Register Courses")
        self.course_registration_button.clicked.connect(self.register_courses)

        self.hostel_registration_button = QPushButton("Hostel Registration")
        self.hostel_registration_button.clicked.connect(self.register_hostel)

        self.print_result_button = QPushButton("Print Result")
        self.print_result_button.clicked.connect(self.print_result)

        self.id_card_request_button = QPushButton("ID Card Request Form")
        self.id_card_request_button.clicked.connect(self.request_id_card)

        # Add buttons to the layout
        layout.addWidget(self.course_registration_button)
        layout.addWidget(self.hostel_registration_button)
        layout.addWidget(self.print_result_button)
        layout.addWidget(self.id_card_request_button)

        self.setLayout(layout)

    def register_courses(self):
        """
        Opens the Register Courses dialog window.
        """
        self.new_window = RegisterCoursesPage()  # Instantiate RegisterCoursesPage
        self.new_window.setModal(True)  # Makes the dialog modal
        self.new_window.exec()  # Opens the dialog modally

    def register_hostel(self):
        """
        Opens the Hostel Registration dialog window.
        """
        self.new_window = HostelRegistrationPage()  # Instantiate HostelRegistrationPage
        self.new_window.setModal(True)  # Makes the dialog modal
        self.new_window.exec()  # Opens the dialog modally

    def print_result(self):
        """
        Displays a placeholder message for printing results.
        """
        QMessageBox.information(self, "Print Result", "Result printing window opened.")

    def request_id_card(self):
        """
        Displays a placeholder message for ID card requests.
        """
        QMessageBox.information(self, "ID Card Request", "ID Card request form opened.")


class RegisterCoursesPage(QDialog):
    def __init__(self):
        super().__init__()

        # Window Properties
        self.setWindowTitle("Register Courses Page")
        self.setGeometry(300, 100, 700, 500)

        # Main Layout
        self.main_layout = QVBoxLayout()

        # Title Section
        title_label = QLabel("Register Courses")
        title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Instruction Box
        instruction_label = QLabel(
            "You are to select an available session as appropriate. Please note that once registration "
            "is closed for a particular session/semester, that session/semester would not be available "
            "for selection. Once a session/semester has been selected and you have passed all necessary "
            "checks, you can click on any of the tabs 'Course Registration', 'Additional Courses' or "
            "'View Enrolled Courses' to view, register or delete courses for the semester."
        )
        instruction_label.setStyleSheet("background-color: #008040; color: white; padding: 10px;")
        instruction_label.setWordWrap(True)

        # Session Dropdown
        session_label = QLabel("SELECT REGISTRATION SESSION:")
        session_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))

        self.session_dropdown = QComboBox()
        self.session_dropdown.addItems(["-- Select Session --", "2022/2023", "2023/2024", "2024/2025"])
        self.session_dropdown.currentIndexChanged.connect(self.on_session_selected)

        # Layout for the session dropdown
        session_layout = QHBoxLayout()
        session_layout.addWidget(session_label)
        session_layout.addWidget(self.session_dropdown)
        session_layout.addStretch()

        # Add Widgets to Main Layout
        self.main_layout.addWidget(title_label)
        self.main_layout.addWidget(instruction_label)
        self.main_layout.addLayout(session_layout)

        # Placeholder for Level and Department dropdowns
        self.dynamic_dropdown_layout = QVBoxLayout()
        self.main_layout.addLayout(self.dynamic_dropdown_layout)

        # Set Layout
        self.setLayout(self.main_layout)

    def on_session_selected(self, index):
        """
        Triggered when a session is selected. Dynamically adds dropdowns for Level and Department.
        """
        # Remove existing widgets from dynamic layout
        self.clear_layout(self.dynamic_dropdown_layout)

        # Check if a valid session is selected
        if index > 0:
            # Level Dropdown
            level_label = QLabel("SELECT LEVEL:")
            level_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))

            self.level_dropdown = QComboBox()
            self.level_dropdown.addItems(
                ["-- Select Level --", "100 Level", "200 Level", "300 Level", "400 Level", "500 Level"])

            # Department Dropdown
            department_label = QLabel("SELECT DEPARTMENT:")
            department_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))

            self.department_dropdown = QComboBox()
            self.department_dropdown.addItems(
                ["-- Select Department --", "Computer Science", "Electrical Engineering", "Mechanical Engineering",
                 "Civil Engineering", "Mechatronic Engineering "])

            # Save Button
            save_button = QPushButton("Proceed")
            save_button.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            save_button.setStyleSheet("background-color: red; color: white; border-radius: 5px; padding: 5px;")
            save_button.setFixedWidth(100)
            save_button.clicked.connect(self.proceed_action)

            # Add widgets to dynamic layout
            self.dynamic_dropdown_layout.addWidget(level_label)
            self.dynamic_dropdown_layout.addWidget(self.level_dropdown)
            self.dynamic_dropdown_layout.addWidget(department_label)
            self.dynamic_dropdown_layout.addWidget(self.department_dropdown)
            self.dynamic_dropdown_layout.addWidget(save_button)

    def proceed_action(self):
        """
        Placeholder for the action when 'Proceed' is clicked.
        """
        level = self.level_dropdown.currentText()
        department = self.department_dropdown.currentText()
        print(f"Selected Level: {level}, Selected Department: {department}")

    def clear_layout(self, layout):
        """
        Clears all widgets from a given layout.
        """
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()


class HostelRegistrationPage(QDialog):
    def __init__(self):
        super().__init__()

        # Window properties
        self.setWindowTitle("Hostel Registration Page")
        self.setGeometry(300, 100, 600, 400)

        # Main Layout
        main_layout = QVBoxLayout()

        # Section 1: Title
        title_label = QLabel("Please choose your Hostel below:")
        title_label.setFont(QFont("Arial", 12))
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Section 2: Dropdown Selection
        dropdown_layout = QHBoxLayout()
        select_label = QLabel("SELECT YOUR HOSTEL:")
        select_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))

        self.hostel_dropdown = QComboBox()
        self.hostel_dropdown.addItems(["-- Select Hostel --", "Hostel A", "Hostel B", "Hostel C", "Hostel D"])
        self.hostel_dropdown.setFixedWidth(150)

        dropdown_layout.addWidget(select_label)
        dropdown_layout.addWidget(self.hostel_dropdown)
        dropdown_layout.addStretch()

        # Section 3: Text Input
        info_label = QLabel("STATE ANY IMPORTANT INFORMATION BELOW:")
        info_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))

        self.info_text = QTextEdit()
        self.info_text.setPlaceholderText(
            "e.g. Your Phone Type, Laptop, Valuables etc. you are bringing along with you "
            "or other information worth knowing. Note: This will appear on your Hostel "
            "Registration form."
        )
        self.info_text.setFixedHeight(100)

        # Section 4: Save Button
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        save_button.setStyleSheet(
            "QPushButton {"
            "background-color: red; color: white; border: 2px solid black; border-radius: 5px;"
            "padding: 5px;"
            "}"
            "QPushButton:hover {"
            "background-color: darkred;"
            "}"
        )
        save_button.setFixedWidth(70)
        button_layout.addStretch()
        button_layout.addWidget(save_button)

        # Add widgets to main layout
        main_layout.addWidget(title_label)
        main_layout.addLayout(dropdown_layout)
        main_layout.addWidget(info_label)
        main_layout.addWidget(self.info_text)
        main_layout.addLayout(button_layout)

        # Set the main layout
        self.setLayout(main_layout)


class TeacherDashboard(QDialog):
    def __init__(self, teacher_data):
        super().__init__()
        self.teacher_data = teacher_data  # Store teacher data
        self.setWindowTitle("Teacher Dashboard")
        self.setGeometry(100, 100, 1200, 800)
        self.init_ui()

    def init_ui(self):
        # Main Layout
        main_layout = QHBoxLayout(self)

        # Left Navigation Menu
        nav_menu = QVBoxLayout()

        # Display Teacher Information Dynamically
        name = QLabel(f"{self.teacher_data['name']}")
        department = QLabel(f"{self.teacher_data['department']}")

        # Customize font size and styling individually
        name.setAlignment(Qt.AlignmentFlag.AlignLeft)
        name.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 2px;")  # Larger font size for the name

        department.setAlignment(Qt.AlignmentFlag.AlignLeft)
        department.setStyleSheet("font-size: 12px; font-weight: normal; margin-bottom: 5px;")  # Smaller font size for the department

        # Add the labels to the navigation menu
        nav_menu.addWidget(name)
        nav_menu.addWidget(department)

        print(self.teacher_data)

        # Add Navigation Buttons
        self.pages = QStackedWidget()  # Stacked widget to hold all pages
        buttons = [
            ("Home", self.create_home_page),
            ("Messages", self.create_messages_page),
            ("Schedule", self.create_schedule_page),
            ("Online Course", self.create_online_course_page),
            ("Assignment", self.create_assignment_page),
            ("Discussion", self.create_discussion_page),
            ("Announcement", self.create_announcement_page),
            ("Settings", self.create_settings_page),
        ]

        for btn_text, page_creator in buttons:
            btn = QPushButton(btn_text)
            btn.setStyleSheet("padding: 10px; text-align: left;")
            btn.clicked.connect(page_creator)
            nav_menu.addWidget(btn)

        # Logout Button
        logout_btn = QPushButton("Logout")
        logout_btn.setStyleSheet("padding: 10px; text-align: left;")
        logout_btn.clicked.connect(self.logout)
        nav_menu.addWidget(logout_btn)

        nav_menu.addStretch()

        # Add Left Navigation and Content to Main Layout
        main_layout.addLayout(nav_menu, 1)
        main_layout.addWidget(self.pages, 4)

        # Initialize the first page
        self.create_home_page()

    def create_home_page(self):
        """Create the Home Page using QFormLayout."""
        page = QWidget()
        layout = QFormLayout(page)

        # Set spacing and margins
        layout.setSpacing(5)
        layout.setContentsMargins(10, 10, 10, 10)

        # Teacher Details Section
        teacher_details_label = QLabel(f"Welcome {self.teacher_data.get('username', 'N/A')}")
        teacher_details_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        teacher_details_label.setFont(QFont("Artifakt Element", 20, QFont.Weight.Bold))
        layout.addRow(teacher_details_label)  # Empty label for alignment

        # Teacher Information
        name_label = QLabel(f"Name: {self.teacher_data.get('name', 'N/A')}")
        name_label.setFont(QFont("Artifakt Element", 14))
        name_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addRow(name_label)

        department_label = QLabel(f"Department: {self.teacher_data.get('department', 'N/A')}")
        department_label.setFont(QFont("Artifakt Element", 14))
        department_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addRow(department_label)

        id_label = QLabel(f"Teacher ID: {self.teacher_data.get('matric_no', 'N/A')}")
        id_label.setFont(QFont("Artifakt Element", 14))
        id_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addRow(id_label)

        email_label = QLabel(f"Email: {self.teacher_data.get('email', 'N/A')}")
        email_label.setFont(QFont("Artifakt Element", 14))
        email_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addRow(email_label)

        phone_label = QLabel(f"Phone: {self.teacher_data.get('phone_number', 'N/A')}")
        phone_label.setFont(QFont("Artifakt Element", 14))
        phone_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addRow(phone_label)

        # Set the page as the current widget
        self.pages.addWidget(page)
        self.pages.setCurrentWidget(page)

    def create_messages_page(self):
        """Create the Messages Page."""
        page = QWidget()
        layout = QVBoxLayout(page)

        label = QLabel("Messages Page")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 18px; font-weight: bold;")

        messages_list = QListWidget()
        messages_list.addItems([
            "Mark: Sorry, I can't attend...",
            "James: Hello sir, I need help...",
            "Toby: Haha sorry can't learn...",
        ])

        layout.addWidget(label)
        layout.addWidget(messages_list)
        self.pages.addWidget(page)
        self.pages.setCurrentWidget(page)

    def create_schedule_page(self):
        """Create the Schedule Page."""
        page = QWidget()
        layout = QVBoxLayout(page)

        label = QLabel("Schedule Page")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 18px; font-weight: bold;")

        calendar = QCalendarWidget()
        calendar.setGridVisible(True)

        layout.addWidget(label)
        layout.addWidget(calendar)
        self.pages.addWidget(page)
        self.pages.setCurrentWidget(page)

    def create_online_course_page(self):
        """Create the Online Course Page."""
        page = QWidget()
        layout = QVBoxLayout(page)

        label = QLabel("Online Course Page")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 18px; font-weight: bold;")

        layout.addWidget(label)
        self.pages.addWidget(page)
        self.pages.setCurrentWidget(page)

    def create_assignment_page(self):
        """Create the Assignment Page."""
        page = QWidget()
        layout = QVBoxLayout(page)

        label = QLabel("Assignment Page")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 18px; font-weight: bold;")

        progress = QProgressBar()
        progress.setValue(60)

        layout.addWidget(label)
        layout.addWidget(progress)
        self.pages.addWidget(page)
        self.pages.setCurrentWidget(page)

    def create_discussion_page(self):
        """Create the Discussion Page."""
        page = QWidget()
        layout = QVBoxLayout(page)

        label = QLabel("Discussion Page")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 18px; font-weight: bold;")

        layout.addWidget(label)
        self.pages.addWidget(page)
        self.pages.setCurrentWidget(page)

    def create_announcement_page(self):
        """Create the Announcement Page."""
        page = QWidget()
        layout = QVBoxLayout(page)

        label = QLabel("Announcement Page")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 18px; font-weight: bold;")

        layout.addWidget(label)
        self.pages.addWidget(page)
        self.pages.setCurrentWidget(page)

    def create_settings_page(self):
        """Create the Settings Page."""
        page = QWidget()
        layout = QVBoxLayout(page)

        label = QLabel("Settings Page")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 18px; font-weight: bold;")

        layout.addWidget(label)
        self.pages.addWidget(page)
        self.pages.setCurrentWidget(page)

    def logout(self):
        """Logout Functionality."""
        self.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("University Login")
        self.setGeometry(100, 100, 1080, 720)

        # Create a stacked widget and add pages
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.landing_page = LandingPage()
        self.login_page = LoginWindow()

        self.stacked_widget.addWidget(self.landing_page)  # Page 0
        self.stacked_widget.addWidget(self.login_page)  # Page 1


# Main execution of the application
app = QApplication(sys.argv)
app.setWindowIcon(QIcon('assets/university_logo.png'))  # Replace with your favicon path
window = MainWindow()
window.show()
sys.exit(app.exec())
