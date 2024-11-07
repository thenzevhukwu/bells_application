import sys
import sqlite3
import hashlib
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QMessageBox, QDialog, QFormLayout, QTableWidget, QTableWidgetItem, QComboBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontDatabase

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
            ('Teacher Name', 'TEACH001', 0, 'Teacher Department', 0, '0000000000', 'SANGO', teacher_password, 'teacher', 1)
        )
        conn.commit()

create_admin_user()

# Retrieve a student's details
def get_student_biodata(username):
    cursor.execute("SELECT matric_no, name, level, department, phone_number FROM general_data WHERE username = ?", (username,))
    return cursor.fetchone()

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Bells University Login Page')
        self.setGeometry(100, 100, 600, 400)

        self.main_layout = QVBoxLayout()
        self.create_top_layout()
        self.create_login_widgets()
        self.setLayout(self.main_layout)

    def create_top_layout(self):
        font_id = QFontDatabase.addApplicationFont("Artifakt Element.ttf.ttf")
        self.university_label = QLabel('Bells University Of Technology')
        self.university_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.main_layout.addWidget(self.university_label)

    def create_login_widgets(self):
        self.login_label = QLabel('Login')

        self.username_label = QLabel('Username')
        self.username_input = QLineEdit()

        self.password_label = QLabel('Password')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_button = QPushButton('Login')
        self.login_button.clicked.connect(self.login)

        self.create_account_button = QPushButton('Create Account')
        self.create_account_button.clicked.connect(self.open_create_account_dialog)

        self.form_layout = QVBoxLayout()
        self.form_layout.addWidget(self.login_label)
        self.form_layout.addWidget(self.username_label)
        self.form_layout.addWidget(self.username_input)
        self.form_layout.addWidget(self.password_label)
        self.form_layout.addWidget(self.password_input)
        self.form_layout.addWidget(self.login_button)
        self.form_layout.addWidget(self.create_account_button)
        self.main_layout.addLayout(self.form_layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        hashed_password = hash_password(password)
        cursor.execute("SELECT * FROM general_data WHERE username = ? AND password = ?", (username, hashed_password))
        user = cursor.fetchone()

        if user and user[8]:  # Account approved (column approved is at index 8)
            if user[9] == 'admin':  # Role column is at index 9
                self.open_admin_panel()
            elif user[9] == 'teacher':
                QMessageBox.information(self, 'Teacher', 'Logged in successfully')
                teacher_data = {
                    'name': user[0],           # Assuming user[0] is the name
                    'username': user[7],       # Assuming user[7] is the username
                    'department': user[3],     # Assuming user[3] is the department
                    'phone_number': user[5],   # Assuming user[5] is the phone number
                }
                self.open_teacher_dashboard(teacher_data)
            else:
                QMessageBox.information(self, 'Student', 'Logged in successfully')
                student_data = {
                    'name': user[0],           # Assuming user[0] is the name
                    'matric_no': user[1],      # Assuming user[1] is the matric number
                    'level': user[2],          # Assuming user[2] is the level
                    'department': user[3],     # Assuming user[3] is the department
                    'phone_number': user[5],   # Assuming user[5] is the phone number
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
        dashboard.exec()  # Show the teacher dashboard window

    def open_create_account_dialog(self):
        dialog = CreateAccountDialog(self)
        dialog.exec()

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

        self.profile_management_button = QPushButton("Manage User Profiles")
        self.profile_management_button.clicked.connect(self.open_profile_management)

        self.program_course_management_button = QPushButton("Manage Academic Programs and Courses")
        self.program_course_management_button.clicked.connect(self.open_program_course_management)

        self.logout_button = QPushButton("Logout")
        self.logout_button.clicked.connect(self.logout)

        # Add buttons to layout
        self.layout.addWidget(self.user_management_button)
        self.layout.addWidget(self.profile_management_button)
        self.layout.addWidget(self.program_course_management_button)
        self.layout.addWidget(self.logout_button)
        self.setLayout(self.layout)

    def open_user_management(self):
        dialog = UserManagementDialog()
        dialog.exec()

    def open_profile_management(self):
        dialog = ProfileManagementDialog()
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

        self.add_user_button = QPushButton("Add User")
        self.add_user_button.clicked.connect(self.add_user)

        self.edit_user_button = QPushButton("Edit User")
        self.edit_user_button.clicked.connect(self.edit_user)

        self.delete_user_button = QPushButton("Delete User")
        self.delete_user_button.clicked.connect(self.delete_user)

        self.approve_user_button = QPushButton("Approve User")
        self.approve_user_button.clicked.connect(self.approve_user)

        # Add buttons to layout
        self.layout.addWidget(self.add_user_button)
        self.layout.addWidget(self.edit_user_button)
        self.layout.addWidget(self.delete_user_button)
        self.layout.addWidget(self.approve_user_button)
        self.setLayout(self.layout)

    def add_user(self):
        dialog = AddUserDialog()
        dialog.exec()

    def edit_user(self):
        dialog = EditUserDialog()
        dialog.exec()

    def delete_user(self):
        dialog = DeleteUserDialog()
        dialog.exec()

    def approve_user(self):
        dialog = ApproveUserDialog()
        dialog.exec()


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

# Dialog for editing a user
class EditUserDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edit User")
        self.setGeometry(200, 200, 400, 300)
        layout = QFormLayout()

        self.username_input = QLineEdit()
        self.new_name_input = QLineEdit()
        self.new_matric_no_input = QLineEdit()
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_role_input = QLineEdit()  # Role input

        layout.addRow("Username to Edit:", self.username_input)
        layout.addRow("New Name:", self.new_name_input)
        layout.addRow("New Matric No:", self.new_matric_no_input)
        layout.addRow("New Password:", self.new_password_input)
        layout.addRow("New Role (student/admin/teacher):", self.new_role_input)

        self.edit_button = QPushButton("Edit User")
        self.edit_button.clicked.connect(self.edit_user_in_db)
        layout.addRow(self.edit_button)
        self.setLayout(layout)

    def edit_user_in_db(self):
        username = self.username_input.text()
        new_name = self.new_name_input.text()
        new_matric_no = self.new_matric_no_input.text()
        new_password = self.new_password_input.text()
        new_role = self.new_role_input.text()

        if not username:
            QMessageBox.warning(self, "Error", "Username is required.")
            return

        hashed_password = hash_password(new_password) if new_password else None
        try:
            cursor.execute("SELECT * FROM general_data WHERE username = ?", (username,))
            user = cursor.fetchone()
            if not user:
                QMessageBox.warning(self, "Error", "User not found.")
                return

            # Update user information
            cursor.execute(
                "UPDATE general_data SET name = ?, matric_no = ?, password = ?, role = ? WHERE username = ?",
                (new_name or user[1], new_matric_no or user[2], hashed_password or user[7], new_role or user[9], username)
            )
            conn.commit()
            QMessageBox.information(self, "Success", "User edited successfully.")
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

# Dialog for Profile Management
class ProfileManagementDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manage User Profiles")
        self.setGeometry(150, 150, 500, 400)
        self.layout = QVBoxLayout()

        self.view_profiles_button = QPushButton("View Profiles")
        self.view_profiles_button.clicked.connect(self.view_profiles)

        # Add buttons to layout
        self.layout.addWidget(self.view_profiles_button)
        self.setLayout(self.layout)

    def view_profiles(self):
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
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels(["Name", "Matric No", "Username", "Role", "Approved", "Phone"])

        for i, user in enumerate(users):
            for j in range(6):
                table.setItem(i, j, QTableWidgetItem(str(user[j])))

        layout.addWidget(table)
        dialog.setLayout(layout)
        dialog.exec()

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
        self.setWindowTitle("Add Course")
        self.setGeometry(200, 200, 400, 300)
        layout = QFormLayout()

        self.course_name_input = QLineEdit()
        self.course_code_input = QLineEdit()

        layout.addRow("Course Name:", self.course_name_input)
        layout.addRow("Course Code:", self.course_code_input)

        self.add_button = QPushButton("Add Course")
        self.add_button.clicked.connect(self.add_course_to_db)
        layout.addRow(self.add_button)
        self.setLayout(layout)

    def add_course_to_db(self):
        course_name = self.course_name_input.text()
        course_code = self.course_code_input.text()

        if not course_name or not course_code:
            QMessageBox.warning(self, "Error", "Both fields are required.")
            return

        try:
            cursor.execute(
                "INSERT INTO courses (course_name, course_code) VALUES (?, ?)",
                (course_name, course_code)
            )
            conn.commit()
            QMessageBox.information(self, "Success", "Course added successfully.")
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
        QMessageBox.information(self, "Register Courses", "Course registration window opened.")

    def register_hostel(self):
        # Placeholder action for hostel registration
        QMessageBox.information(self, "Hostel Registration", "Hostel registration window opened.")

    def print_result(self):
        # Placeholder action for printing results
        QMessageBox.information(self, "Print Result", "Result printing window opened.")

    def request_id_card(self):
        # Placeholder action for ID card request
        QMessageBox.information(self, "ID Card Request", "ID Card request form opened.")

class TeacherDashboard(QDialog):
    def __init__(self, teacher_data):
        super().__init__()
        self.setWindowTitle("Teacher Dashboard")
        self.setGeometry(200, 200, 500, 400)

        layout = QVBoxLayout()

        # Display teacher information
        self.teacher_data = teacher_data
        name_label = QLabel(f"Name: {self.teacher_data['name']}")
        username_label = QLabel(f"Username: {self.teacher_data['username']}")
        department_label = QLabel(f"Department: {self.teacher_data['department']}")
        phone_label = QLabel(f"Phone Number: {self.teacher_data['phone_number']}")

        # Add teacher info labels to the layout
        layout.addWidget(name_label)
        layout.addWidget(username_label)
        layout.addWidget(department_label)
        layout.addWidget(phone_label)

        # Add action buttons
        self.view_courses_button = QPushButton("View Courses")
        self.view_courses_button.clicked.connect(self.view_courses)

        self.view_students_button = QPushButton("View Students")
        self.view_students_button.clicked.connect(self.view_students)

        self.generate_reports_button = QPushButton("Generate Reports")
        self.generate_reports_button.clicked.connect(self.generate_reports)

        # Add buttons to the layout
        layout.addWidget(self.view_courses_button)
        layout.addWidget(self.view_students_button)
        layout.addWidget(self.generate_reports_button)

        self.setLayout(layout)

    def view_courses(self):
        # Placeholder action for viewing courses
        QMessageBox.information(self, "View Courses", "Course viewing window opened.")

    def view_students(self):
        # Placeholder action for viewing students
        QMessageBox.information(self, "View Students", "Student viewing window opened.")

    def generate_reports(self):
        # Placeholder action for generating reports
        QMessageBox.information(self, "Generate Reports", "Report generation window opened.")


# Main execution of the application
app = QApplication(sys.argv)
window = LoginWindow()
window.show()
sys.exit(app.exec())
