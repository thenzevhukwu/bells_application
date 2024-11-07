import sys
import sqlite3
import hashlib
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
        self.setWindowTitle('University Login')
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
            else:
                QMessageBox.information(self, 'Student', 'Logged in successfully')
        else:
            QMessageBox.warning(self, 'Error', 'Invalid credentials or account not approved')

    def open_admin_panel(self):
        dialog = AdminPanel()
        dialog.exec()

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

        # Insert data into the existing general_data table
        conn = sqlite3.connect('school_database.db')
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO general_data (name, matric_no, level, department, age, phone_number, username, password, approved, role)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, matric_number, level, department, age, phone_number, username, password, approved, role))
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

        self.disapprove_user_button = QPushButton("Disapprove User")
        self.disapprove_user_button.clicked.connect(self.disapprove_user)

        # Add buttons to layout
        self.layout.addWidget(self.add_user_button)
        self.layout.addWidget(self.edit_user_button)
        self.layout.addWidget(self.delete_user_button)
        self.layout.addWidget(self.approve_user_button)
        self.layout.addWidget(self.disapprove_user_button)
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

    def disapprove_user(self):
        dialog = DisapproveUserDialog()
        dialog.exec()


# Dialog for approving a user
class ApproveUserDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Approve User")
        self.setGeometry(200, 200, 400, 300)
        layout = QFormLayout()

        self.username_input = QLineEdit()
        layout.addRow("Username to Approve:", self.username_input)

        self.approve_button = QPushButton("Approve User")
        self.approve_button.clicked.connect(self.approve_user_in_db)
        layout.addRow(self.approve_button)
        self.setLayout(layout)

    def approve_user_in_db(self):
        username = self.username_input.text()
        if not username:
            QMessageBox.warning(self, "Error", "Username is required.")
            return

        try:
            cursor.execute("UPDATE general_data SET approved = ? WHERE username = ?", (1, username))
            conn.commit()
            if cursor.rowcount == 0:
                QMessageBox.warning(self, "Error", "User not found.")
            else:
                QMessageBox.information(self, "Success", "User approved successfully.")
                self.accept()
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Error", f"Database error: {e}")


# Dialog for disapproving a user
class DisapproveUserDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Disapprove User")
        self.setGeometry(200, 200, 400, 300)
        layout = QFormLayout()

        self.username_input = QLineEdit()
        layout.addRow("Username to Disapprove:", self.username_input)

        self.disapprove_button = QPushButton("Disapprove User")
        self.disapprove_button.clicked.connect(self.disapprove_user_in_db)
        layout.addRow(self.disapprove_button)
        self.setLayout(layout)

    def disapprove_user_in_db(self):
        username = self.username_input.text()
        if not username:
            QMessageBox.warning(self, "Error", "Username is required.")
            return

        try:
            cursor.execute("UPDATE general_data SET approved = ? WHERE username = ?", (0, username))
            conn.commit()
            if cursor.rowcount == 0:
                QMessageBox.warning(self, "Error", "User not found.")
            else:
                QMessageBox.information(self, "Success", "User disapproved successfully.")
                self.accept()
        except sqlite3.Error as e:
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

# Main execution of the application
app = QApplication(sys.argv)
window = LoginWindow()
window.show()
sys.exit(app.exec())
