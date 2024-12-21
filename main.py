import sys
import sqlite3
import hashlib
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QMessageBox, QDialog, QFormLayout, QTableWidget, QTabWidget, QTableWidgetItem, QComboBox, QSpinBox, QHeaderView,
    QHBoxLayout, QScrollArea, QMainWindow, QStackedWidget, QFrame
)
from PyQt6.QtCore import Qt, pyqtBoundSignal
from PyQt6.QtGui import QFontDatabase, QIcon, QPalette, QColor, QFont
from PyQt6.QtGui import QPixmap

# Connect to SQLite database
conn = sqlite3.connect('school_database.db')
cursor = conn.cursor()


# Helper function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Create initial admin and teacher accounts
def create_admin_user():
    cursor.execute("SELECT * FROM general_data WHERE username = ?", ('admin-user',))
    admin = cursor.fetchone()
    if not admin:
        admin_password = hash_password('admin-admin')
        cursor.execute(
            "INSERT INTO general_data (name, matric_no, level, department, age, phone_number, username, password, role, approved) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ('Admin User', 'ADMIN001', 0, 'Admin Department', 0, '0000000000', 'admin-user', admin_password, 'admin', 1)
        )
        conn.commit()

    cursor.execute("SELECT * FROM general_data WHERE username = ?", ('SANGO',))
    teacher = cursor.fetchone()
    if not teacher:
        teacher_password = hash_password('NOSA')
        cursor.execute(
            "INSERT INTO general_data (name, matric_no, level, department, age, phone_number, username, password, role, approved) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ('Teacher Name', 'TEACH001', 0, 'Teacher Department', 0, '0000000000', 'SANGO', teacher_password, 'teacher',
             1)
        )
        conn.commit()


create_admin_user()


# Retrieve a student's details
def get_student_biodata(username):
    cursor.execute("SELECT matric_no, name, level, department, phone_number FROM general_data WHERE username = ?",
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

        # Apply background image using stylesheet
        self.setStyleSheet(
            """
            QMainWindow {
                background: url("bells-img.jpg");
                background-repeat: no-repeat;
                background-size: cover
                
                
                
            }
            """
        )

        
        

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

        if user and user[8]:  # Account approved (column approved is at index 8)
            if user[9] == 'admin':  # Role column is at index 9
                self.open_admin_panel()
            elif user[9] == 'teacher':
                QMessageBox.information(self, 'Teacher', 'Logged in successfully')
                teacher_data = {
                    'name': user[0],  # Assuming user[0] is the name
                    'username': user[7],  # Assuming user[7] is the username
                    'department': user[3],  # Assuming user[3] is the department
                    'phone_number': user[5],  # Assuming user[5] is the phone number
                }
                self.open_teacher_dashboard(teacher_data)
            else:
                QMessageBox.information(self, 'Student', 'Logged in successfully')
                student_data = {
                    'name': user[0],  # Assuming user[0] is the name
                    'matric_no': user[1],  # Assuming user[1] is the matric number
                    'level': user[2],  # Assuming user[2] is the level
                    'department': user[3],  # Assuming user[3] is the department
                    'phone_number': user[5],  # Assuming user[5] is the phone number
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

        # Simulated validation logic for the security question and username
        # In a real application, fetch data from the database to verify details
        conn = sqlite3.connect("school_database.db")
        cursor = conn.cursor()

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
        matric_number = self.matric_input.text()
        department = self.department_input.text()
        level = self.level_input.text()
        age = self.age_input.text()  # Example fixed age value
        phone_number = self.phone_number.text()  # Example fixed phone number
        username = self.username_input.text()
        password = self.password_input.text()
        approved = False  # Example approval status
        role = self.role_input.currentText()

        # Validation
        if not all([name, matric_number, department, level, role]):
            QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        hashed_password = hash_password(password)

        # Insert data into the existing general_data table
        conn = sqlite3.connect('school_database.db')
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO general_data (name, matric_no, level, department, age, phone_number, username, password, approved, role)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, matric_number, level, department, age, phone_number, username, hashed_password, approved, role))
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
        self.setWindowTitle("Admin Panel")
        self.setGeometry(100, 100, 800, 600)
        self.layout = QVBoxLayout()

        # Initialize buttons for admin options
        self.user_management_button = QPushButton("User Management")
        self.user_management_button.clicked.connect(self.open_user_management)

        self.program_course_management_button = QPushButton("Manage Academic Programs and Courses")
        self.program_course_management_button.clicked.connect(self.open_program_course_management)

        self.logout_button = QPushButton("Logout")
        self.logout_button.clicked.connect(self.logout)

        # Add buttons to layout
        self.layout.addWidget(self.user_management_button)
        self.layout.addWidget(self.program_course_management_button)
        self.layout.addWidget(self.logout_button)
        self.setLayout(self.layout)

    def open_user_management(self):
        dialog = UserManagementDialog()
        dialog.exec()

    def open_program_course_management(self):
        dialog = ProgramCourseManagementDialog()
        dialog.exec()

    def logout(self):
        self.close()
        window.show()


# Dialog for User Management
class UserManagementDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User Management")
        self.setGeometry(150, 150, 500, 400)
        self.layout = QVBoxLayout()

        self.view_profile_button = QPushButton("View Profiles")
        self.view_profile_button.clicked.connect(self.view_profiles)

        self.add_user_button = QPushButton("Add User")
        self.add_user_button.clicked.connect(self.add_user)

        self.delete_user_button = QPushButton("Delete User")
        self.delete_user_button.clicked.connect(self.delete_user)

        self.approve_user_button = QPushButton("Approve User")
        self.approve_user_button.clicked.connect(self.approve_user)

        # Add buttons to layout
        self.layout.addWidget(self.view_profile_button)
        self.layout.addWidget(self.add_user_button)
        self.layout.addWidget(self.delete_user_button)
        self.layout.addWidget(self.approve_user_button)
        self.setLayout(self.layout)

    def add_user(self):
        dialog = AddUserDialog()
        dialog.exec()

    def delete_user(self):
        dialog = DeleteUserDialog()
        dialog.exec()

    def approve_user(self):
        dialog = ApproveUserDialog()
        dialog.exec()

    def view_profiles(self):
        try:
            cursor.execute("SELECT * FROM general_data")
            users = cursor.fetchall()

            if not users:
                QMessageBox.information(self, "Info", "No users found.")
                return

            dialog = QDialog(self)
            dialog.setWindowTitle("User Profiles")
            dialog.setGeometry(150, 150, 600, 400)

            layout = QVBoxLayout()

            table = QTableWidget()
            table.setRowCount(len(users))
            table.setColumnCount(10)
            table.setHorizontalHeaderLabels([
                "Name", "Matric No", "Level", "Department", "Age",
                "Phone number", "Username", "Password", "Approved", "Role"
            ])

            # Populate the table and make cells editable
            for i, user in enumerate(users):
                for j in range(10):
                    item = QTableWidgetItem(str(user[j]))
                    table.setItem(i, j, item)

            layout.addWidget(table)

            # Add the 'Done' button
            done_button = QPushButton("Done")

            # Function to save changes to the database
            def save_changes():
                try:
                    for i in range(table.rowCount()):
                        updated_values = []
                        for j in range(table.columnCount()):
                            updated_values.append(table.item(i, j).text())

                        update_query = """
                            UPDATE general_data 
                            SET name = ?, matric_no = ?, level = ?, department = ?, age = ?, 
                                phone_number = ?, username = ?, password = ?, approved = ?, role = ?
                            WHERE matric_no = ?
                        """
                        # Execute the update query using matric_no as the unique identifier
                        cursor.execute(update_query, (*updated_values, updated_values[1]))

                    conn.commit()  # Commit changes after all updates
                    QMessageBox.information(self, "Info", "Changes saved successfully.")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"An error occurred while saving changes: {e}")
                finally:
                    dialog.accept()  # Close the dialog after saving or in case of error

            done_button.clicked.connect(save_changes)
            layout.addWidget(done_button)

            dialog.setLayout(layout)
            dialog.exec()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")


# Dialog for approving a user
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

        self.name_input = QLineEdit()
        self.matric_no_input = QLineEdit()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.role_input = QLineEdit()  # Role input

        layout.addRow("Name:", self.name_input)
        layout.addRow("Matric No:", self.matric_no_input)
        layout.addRow("Username:", self.username_input)
        layout.addRow("Password:", self.password_input)
        layout.addRow("Role (student/admin/teacher):", self.role_input)

        self.add_button = QPushButton("Add User")
        self.add_button.clicked.connect(self.add_user_to_db)
        layout.addRow(self.add_button)
        self.setLayout(layout)

    def add_user_to_db(self):
        name = self.name_input.text()
        matric_no = self.matric_no_input.text()
        username = self.username_input.text()
        password = self.password_input.text()
        role = self.role_input.text()

        if not name or not matric_no or not username or not password or not role:
            QMessageBox.warning(self, "Error", "All fields are required.")
            return

        hashed_password = hash_password(password)
        try:
            cursor.execute("SELECT * FROM general_data WHERE username = ?", (username,))
            existing_user = cursor.fetchone()
            if existing_user:
                QMessageBox.warning(self, "Error", "Username already exists.")
                return

            cursor.execute(
                "INSERT INTO general_data (name, matric_no, username, password, approved, role) VALUES (?, ?, ?, ?, ?, ?)",
                (name, matric_no, username, hashed_password, 1, role)  # Automatically approve for admin
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


# Dialog for Academic Programs and Courses Management
class ProgramCourseManagementDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manage Academic Programs and Courses")
        self.setGeometry(150, 150, 500, 400)
        self.layout = QVBoxLayout()

        self.add_course_button = QPushButton("Add Course")
        self.add_course_button.clicked.connect(self.add_course)

        self.edit_course_button = QPushButton("Edit Course")
        self.edit_course_button.clicked.connect(self.edit_course)

        self.delete_course_button = QPushButton("Delete Course")
        self.delete_course_button.clicked.connect(self.delete_course)

        # Add buttons to layout
        self.layout.addWidget(self.add_course_button)
        self.layout.addWidget(self.edit_course_button)
        self.layout.addWidget(self.delete_course_button)
        self.setLayout(self.layout)

    def add_course(self):
        dialog = AddCourseDialog()
        dialog.exec()

    def edit_course(self):
        dialog = EditCourseDialog()
        dialog.exec()

    def delete_course(self):
        dialog = DeleteCourseDialog()
        dialog.exec()


# Dialog for adding a course
class AddCourseDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Courses for Department and Level")
        self.setGeometry(200, 200, 600, 600)

        # Connect to the database
        try:
            self.conn = sqlite3.connect("school_database.db")  # Replace with actual path
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"Could not connect to database: {e}")
            self.close()

        # Main layout
        self.layout = QVBoxLayout()

        # Level Selection Field (using QComboBox for predefined options)
        self.level_input = QComboBox()
        self.level_input.addItems(["100L", "200L", "300L", "400L", "500L"])

        # Department Selection Field
        self.department_input = QComboBox()
        self.department_input.addItems(["Biochemistry", "Industrial Chemistry", "Microbiology", "Applied Mathematics",
                                        "Statistics", "Biotechnology", "Computer Scence", "Information Technology",

                                        "Mechanical Engineering", "Mechatronics Engineering", "Civil Engineering",
                                        "Biomedical Engineering",
                                        "Telecommunication Engineering", "Electrical/Electronics Engineering",
                                        "Agricultural and Bioresources Engineering",

                                        "Human Resources Management", "Accounting", "Economics", "Marketing",
                                        "Business Computing", "International Business",
                                        "Project Management Tech", "Transport Management and Logistics",

                                        "Food Technology", "Nutrition and Dietetics"])

        self.layout.addWidget(QLabel("Department:"))
        self.layout.addWidget(self.department_input)
        self.layout.addWidget(QLabel("Level:"))
        self.layout.addWidget(self.level_input)

        # Courses container layout
        self.courses_layout = QVBoxLayout()
        self.course_inputs = []

        # Initially add three course input rows
        for _ in range(3):
            self.add_course_fields()

        # Scroll area for course fields
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_widget.setLayout(self.courses_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        self.layout.addWidget(scroll_area)

        # Button to add more courses
        self.add_more_button = QPushButton("Add More Courses")
        self.add_more_button.clicked.connect(self.add_course_fields)
        self.layout.addWidget(self.add_more_button)

        # Save Button
        self.add_button = QPushButton("Save Courses")
        self.add_button.clicked.connect(self.add_courses_to_db)
        self.layout.addWidget(self.add_button)

        self.setLayout(self.layout)

    def add_course_fields(self):
        # Limit to a maximum of 15 courses
        if len(self.course_inputs) >= 15:
            QMessageBox.warning(self, "Limit Reached", "You can only add up to 15 courses.")
            return

        # Course input row
        course_layout = QHBoxLayout()
        course_name = QLineEdit()
        course_code = QLineEdit()
        course_unit = QSpinBox()
        course_unit.setRange(1, 6)  # Assuming course units range from 1 to 6

        course_layout.addWidget(QLabel(f"Course {len(self.course_inputs) + 1} Name:"))
        course_layout.addWidget(course_name)
        course_layout.addWidget(QLabel("Code:"))
        course_layout.addWidget(course_code)
        course_layout.addWidget(QLabel("Unit:"))
        course_layout.addWidget(course_unit)

        # Store inputs for later retrieval
        self.course_inputs.append((course_name, course_code, course_unit))
        self.courses_layout.addLayout(course_layout)

    def add_courses_to_db(self):
        department = self.department_input.text()
        level = self.level_input.currentText()

        # Gather course information
        courses = []
        for course_name_input, course_code_input, course_unit_input in self.course_inputs:
            course_name = course_name_input.text()
            course_code = course_code_input.text()
            course_unit = course_unit_input.value()

            if course_name and course_code:
                courses.append((course_name, course_code, course_unit))

        if not department or not courses:
            QMessageBox.warning(self, "Error", "Department and at least one course with valid details are required.")
            return

        try:
            # SQL for insertion
            query = '''
                INSERT INTO Courses (
                    department,
                    level,
                    course1_name, course1_code, course1_unit,
                    course2_name, course2_code, course2_unit,
                    course3_name, course3_code, course3_unit,
                    course4_name, course4_code, course4_unit,
                    course5_name, course5_code, course5_unit,
                    course6_name, course6_code, course6_unit,
                    course7_name, course7_code, course7_unit,
                    course8_name, course8_code, course8_unit,
                    course9_name, course9_code, course9_unit,
                    course10_name, course10_code, course10_unit,
                    course11_name, course11_code, course11_unit,
                    course12_name, course12_code, course12_unit,
                    course13_name, course13_code, course13_unit,
                    course14_name, course14_code, course14_unit,
                    course15_name, course15_code, course15_unit
                ) VALUES (?, ?, 
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''

            # Prepare values
            values = [department, level]
            for i in range(15):
                if i < len(courses):
                    values.extend(courses[i])
                else:
                    values.extend([None, None, None])  # Fill with None for unused courses

            # Execute and commit to the database
            self.cursor.execute(query, values)
            self.conn.commit()
            QMessageBox.information(self, "Success", "Courses added successfully.")
            self.accept()

        except sqlite3.Error as e:
            QMessageBox.warning(self, "Error", f"Database error: {e}")


# Dialog for editing a course
class EditCourseDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edit Course")
        self.setGeometry(200, 200, 400, 300)
        layout = QFormLayout()

        self.course_code_input = QLineEdit()
        self.new_course_name_input = QLineEdit()
        self.new_course_code_input = QLineEdit()

        layout.addRow("Course Code to Edit:", self.course_code_input)
        layout.addRow("New Course Name:", self.new_course_name_input)
        layout.addRow("New Course Code:", self.new_course_code_input)

        self.edit_button = QPushButton("Edit Course")
        self.edit_button.clicked.connect(self.edit_course_in_db)
        layout.addRow(self.edit_button)
        self.setLayout(layout)

    def edit_course_in_db(self):
        course_code = self.course_code_input.text()
        new_course_name = self.new_course_name_input.text()
        new_course_code = self.new_course_code_input.text()

        if not course_code:
            QMessageBox.warning(self, "Error", "Course code is required.")
            return

        try:
            cursor.execute("SELECT * FROM courses WHERE course_code = ?", (course_code,))
            course = cursor.fetchone()
            if not course:
                QMessageBox.warning(self, "Error", "Course not found.")
                return

            cursor.execute(
                "UPDATE courses SET course_name = ?, course_code = ? WHERE course_code = ?",
                (new_course_name or course[1], new_course_code or course[2], course_code)
            )
            conn.commit()
            QMessageBox.information(self, "Success", "Course edited successfully.")
            self.accept()
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Error", f"Database error: {e}")


# Dialog for deleting a course
class DeleteCourseDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Course")
        self.setGeometry(200, 200, 400, 200)
        layout = QFormLayout()

        self.course_code_input = QLineEdit()
        layout.addRow("Course Code to Delete:", self.course_code_input)

        self.delete_button = QPushButton("Delete Course")
        self.delete_button.clicked.connect(self.delete_course_from_db)
        layout.addRow(self.delete_button)
        self.setLayout(layout)

    def delete_course_from_db(self):
        course_code = self.course_code_input.text()
        if not course_code:
            QMessageBox.warning(self, "Error", "Course code is required.")
            return

        try:
            cursor.execute("DELETE FROM courses WHERE course_code = ?", (course_code,))
            conn.commit()
            if cursor.rowcount == 0:
                QMessageBox.warning(self, "Error", "Course not found.")
            else:
                QMessageBox.information(self, "Success", "Course deleted successfully.")
                self.accept()
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Error", f"Database error: {e}")


class StudentDashboard(QDialog):
    def __init__(self, student_data):
        super().__init__()
        self.setWindowTitle("Student Dashboard")
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
        # Placeholder action for course registration
        self.new_window = RegisterCoursesPage()
        self.new_window.setModal(True)  # Makes the dialog modal
        self.new_window.exec()  # Opens the dialog modally

    def register_hostel(self):
        # Placeholder action for hostel registration
        self.new_window = HostelRegistrationPage()
        self.new_window.setModal(True)  # Makes the dialog modal
        self.new_window.exec()  # Opens the dialog modally


    def print_result(self):
        # Placeholder action for printing results
        QMessageBox.information(self, "Print Result", "Result printing window opened.")

    def request_id_card(self):
        # Placeholder action for ID card request
        QMessageBox.information(self, "ID Card Request", "ID Card request form opened.")
    
from PyQt6.QtWidgets import (
    QApplication, QDialog, QLabel, QComboBox, QTextEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QWidget
)

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
            self.level_dropdown.addItems(["-- Select Level --", "100 Level", "200 Level", "300 Level", "400 Level","500 Level"])

            # Department Dropdown
            department_label = QLabel("SELECT DEPARTMENT:")
            department_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))

            self.department_dropdown = QComboBox()
            self.department_dropdown.addItems(["-- Select Department --", "Computer Science", "Electrical Engineering", "Mechanical Engineering", "Civil Engineering", "Mechatronic Engineering "])

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
        self.setWindowTitle("Teacher Dashboard")
        self.setGeometry(200, 200, 800, 600)

        # Teacher data
        self.teacher_data = teacher_data

        # Main layout
        main_layout = QVBoxLayout(self)

        # Tabs
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # Teacher Info Tab
        self.teacher_info_tab = QWidget()
        self.tabs.addTab(self.teacher_info_tab, "Teacher Info")
        self.setup_teacher_info_tab()

        # View Courses Tab
        self.courses_tab = QWidget()
        self.tabs.addTab(self.courses_tab, "Courses")
        self.setup_courses_tab()

    def setup_teacher_info_tab(self):
        layout = QVBoxLayout(self.teacher_info_tab)

        # Display teacher information
        name_label = QLabel(f"Name: {self.teacher_data['name']}")
        username_label = QLabel(f"Username: {self.teacher_data['username']}")
        department_label = QLabel(f"Department: {self.teacher_data['department']}")
        phone_label = QLabel(f"Phone Number: {self.teacher_data['phone_number']}")

        # Add teacher info labels to the layout
        layout.addWidget(name_label)
        layout.addWidget(username_label)
        layout.addWidget(department_label)
        layout.addWidget(phone_label)

    def setup_courses_tab(self):
        layout = QVBoxLayout(self.courses_tab)

        # View Courses Button
        self.view_courses_button = QPushButton("View Courses")
        self.view_courses_button.clicked.connect(self.view_courses)
        layout.addWidget(self.view_courses_button)

        # Placeholder for courses table
        self.courses_table = QTableWidget()
        self.courses_table.setColumnCount(17)  # Assuming 15 courses + department + level
        self.courses_table.setHorizontalHeaderLabels(["Department", "Level"] + [f"Course {i + 1}" for i in range(15)])
        layout.addWidget(self.courses_table)

    def view_courses(self):
        try:
            # Query to retrieve all courses
            query = "SELECT department, level, course1, course2, course3, course4, course5, course6, course7, course8, course9, course10, course11, course12, course13, course14, course15 FROM Courses"
            cursor.execute(query)
            courses = cursor.fetchall()

            # Check if courses are available
            if not courses:
                QMessageBox.information(self, "Info", "No courses available.")
                return

            # Populate the table with the course data
            self.courses_table.setRowCount(len(courses))
            for row_index, row_data in enumerate(courses):
                for column_index, data in enumerate(row_data):
                    item = QTableWidgetItem(str(data) if data is not None else "")
                    self.courses_table.setItem(row_index, column_index, item)

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred: {e}")
            if conn:
                conn.close()


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
window = MainWindow()
window.show()
sys.exit(app.exec())
