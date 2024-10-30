import sys
import sqlite3
import hashlib
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QMessageBox, QTableWidget, QTableWidgetItem, QDialog, QFormLayout, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt

# Connect to SQLite database
conn = sqlite3.connect('university.db')
cursor = conn.cursor()

# Add new columns if they don't exist
try:
    cursor.execute('ALTER TABLE students ADD COLUMN username TEXT')
except sqlite3.OperationalError:
    pass  # Column already exists

try:
    cursor.execute('ALTER TABLE students ADD COLUMN password TEXT')
except sqlite3.OperationalError:
    pass  # Column already exists

try:
    cursor.execute('ALTER TABLE students ADD COLUMN role TEXT DEFAULT "student"')
except sqlite3.OperationalError:
    pass  # Column already exists

# Helper function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Automatically create an admin user if not exists
def create_admin_user():
    cursor.execute("SELECT * FROM students WHERE username = ?", ('admin-user',))
    admin = cursor.fetchone()
    if not admin:
        # Create admin with username 'admin-user' and password 'admin-admin'
        admin_password = hash_password('admin-admin')
        cursor.execute(
            "INSERT INTO students (name, matric_no, level, department, age, phone, username, password, role) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ('Admin User', 'ADMIN001', 'Admin', 'None', 0, '0000000000', 'admin-user', admin_password, 'admin')
        )
        conn.commit()

# Call the function to create the admin user
create_admin_user()

# Add the function to fetch a single student's details
def get_student_biodata(username):
    cursor.execute("SELECT matric_no, name, level, department, phone FROM students WHERE username = ?", (username,))
    return cursor.fetchone()

class UniversityApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('University App')
        self.setGeometry(100, 100, 600, 500)

        # Main layout
        self.main_layout = QVBoxLayout()

        # Create the top layout for university name
        self.create_top_layout()

        # Create the login layout
        self.create_login_widgets()

        self.setLayout(self.main_layout)

    def create_top_layout(self):
        # University name at the top left
        self.university_label = QLabel('Bells University Of Technology')
        self.university_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Create a horizontal layout to align the university name at the top
        self.top_layout = QHBoxLayout()
        self.top_layout.addWidget(self.university_label)

        self.main_layout.addLayout(self.top_layout)

    def create_login_widgets(self):
        # Login form in bottom-right corner
        self.login_label = QLabel('Login')

        self.username_label = QLabel('Username')
        self.username_input = QLineEdit()

        self.password_label = QLabel('Password')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        # Submit button
        self.login_button = QPushButton('Login')
        self.login_button.clicked.connect(self.login)

        # Add the login widgets in a vertical layout
        self.form_layout = QVBoxLayout()
        self.form_layout.addWidget(self.login_label)
        self.form_layout.addWidget(self.username_label)
        self.form_layout.addWidget(self.username_input)
        self.form_layout.addWidget(self.password_label)
        self.form_layout.addWidget(self.password_input)
        self.form_layout.addWidget(self.login_button)

        # Create bottom-right layout
        self.bottom_right_layout = QHBoxLayout()

        # Add a spacer to push the login form to the bottom right
        self.bottom_right_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self.bottom_right_layout.addLayout(self.form_layout)

        # Add the bottom-right layout to the main layout
        self.main_layout.addLayout(self.bottom_right_layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        hashed_password = hash_password(password)

        cursor.execute("SELECT * FROM students WHERE username = ? AND password = ?", (username, hashed_password))
        user = cursor.fetchone()

        if user:
            if user[-1] == 'admin':
                QMessageBox.information(self, 'Admin', 'Logged in as Admin')
                self.create_admin_panel()  # Correctly load the admin panel
            else:
                QMessageBox.information(self, 'Student', 'Logged in successfully')
                self.create_student_panel(username)  # Pass username to student panel
        else:
            QMessageBox.warning(self, 'Error', 'Invalid credentials')

    def create_student_panel(self, username):
        # Clear layout
        self.clear_layout()

        # Fetch student biodata
        biodata = get_student_biodata(username)

        # Display student biodata
        biodata_label = QLabel(f"""
        Matric No: {biodata[0]}
        Full Name: {biodata[1]}
        Level: {biodata[2]}
        Department: {biodata[3]}
        Phone: {biodata[4]}
        """)
        self.main_layout.addWidget(biodata_label)

        # Create a dropdown with student options
        self.student_navbar = QVBoxLayout()

        self.dropdown_button = QPushButton('Options')
        self.student_navbar.addWidget(self.dropdown_button)

        # Add dropdown menu for student actions
        self.dropdown_button_menu = QVBoxLayout()
        self.dropdown_button_menu.addWidget(QPushButton('Pay Fees'))
        self.dropdown_button_menu.addWidget(QPushButton('Payment History'))
        self.dropdown_button_menu.addWidget(QPushButton('Print Examination Clearance'))
        self.dropdown_button_menu.addWidget(QPushButton('Print Result'))
        self.dropdown_button_menu.addWidget(QPushButton('Hostel Registration'))

        self.main_layout.addLayout(self.student_navbar)
        self.main_layout.addLayout(self.dropdown_button_menu)

    def create_admin_panel(self):
        # Clear layout
        self.clear_layout()  # Ensure layout is cleared before adding admin widgets

        # Add buttons for admin functionalities
        self.view_button = QPushButton('View Students')
        self.view_button.clicked.connect(self.view_students)
        self.main_layout.addWidget(self.view_button)

        self.add_button = QPushButton('Add New Student')
        self.add_button.clicked.connect(self.add_student_form)
        self.main_layout.addWidget(self.add_button)

        self.delete_button = QPushButton('Delete Student')
        self.delete_button.clicked.connect(self.delete_student_form)
        self.main_layout.addWidget(self.delete_button)

    def view_students(self):
        # Create table to show student records
        self.students_window = QDialog(self)
        self.students_window.setWindowTitle("Students List")
        self.students_window.setGeometry(150, 150, 500, 400)

        students = self.get_students()

        if students:
            self.table = QTableWidget()
            self.table.setRowCount(len(students))
            self.table.setColumnCount(5)
            self.table.setHorizontalHeaderLabels(['ID', 'Name', 'Matric No', 'Level', 'Department'])

            for i, student in enumerate(students):
                for j, value in enumerate(student[:5]):
                    item = QTableWidgetItem(str(value))
                    self.table.setItem(i, j, item)

            # Enable editing when double-clicked
            self.table.itemDoubleClicked.connect(self.enable_editing)

            layout = QVBoxLayout()
            layout.addWidget(self.table)
            self.students_window.setLayout(layout)
            self.students_window.exec()
        else:
            QMessageBox.information(self, 'Info', 'No students found.')

    def enable_editing(self, item):
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
        # Show Done button for saving edits
        self.done_button = QPushButton('Done')
        self.done_button.clicked.connect(self.save_edits)
        self.main_layout.addWidget(self.done_button)

    def save_edits(self):
        for row in range(self.table.rowCount()):
            student_id = self.table.item(row, 0).text()
            name = self.table.item(row, 1).text()
            matric_no = self.table.item(row, 2).text()
            level = self.table.item(row, 3).text()
            department = self.table.item(row, 4).text()

            cursor.execute(
                "UPDATE students SET name = ?, matric_no = ?, level = ?, department = ? WHERE id = ?",
                (name, matric_no, level, department, student_id)
            )
        conn.commit()
        QMessageBox.information(self, 'Success', 'Changes saved successfully!')
        self.done_button.hide()  # Hide the Done button after saving

    def clear_layout(self):
        # Function to clear the current layout
        for i in reversed(range(self.main_layout.count())):
            widget = self.main_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    def get_students(self):
        cursor.execute("SELECT * FROM students")
        return cursor.fetchall()

    def add_student_form(self):
        # Create a form to add a new student
        self.add_window = QDialog(self)
        self.add_window.setWindowTitle('Add New Student')
        self.add_window.setGeometry(150, 150, 300, 400)

        layout = QFormLayout()

        self.name_input = QLineEdit()
        self.matric_no_input = QLineEdit()
        self.level_input = QLineEdit()
        self.department_input = QLineEdit()
        self.age_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        layout.addRow("Name", self.name_input)
        layout.addRow("Matric No", self.matric_no_input)
        layout.addRow("Level", self.level_input)
        layout.addRow("Department", self.department_input)
        layout.addRow("Age", self.age_input)
        layout.addRow("Phone", self.phone_input)
        layout.addRow("Username", self.username_input)
        layout.addRow("Password", self.password_input)

        self.add_button = QPushButton('Add Student')
        self.add_button.clicked.connect(self.add_student)
        layout.addWidget(self.add_button)

        self.add_window.setLayout(layout)
        self.add_window.exec()

    def add_student(self):
        name = self.name_input.text()
        matric_no = self.matric_no_input.text()
        level = self.level_input.text()
        department = self.department_input.text()
        age = self.age_input.text()
        phone = self.phone_input.text()
        username = self.username_input.text()
        password = hash_password(self.password_input.text())

        try:
            cursor.execute(
                "INSERT INTO students (name, matric_no, level, department, age, phone, username, password, role) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (name, matric_no, level, department, age, phone, username, password, 'student')
            )
            conn.commit()
            QMessageBox.information(self, 'Success', 'Student added successfully!')
            self.add_window.close()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, 'Error', 'Matric number or username already exists!')

    def delete_student_form(self):
        # Create a form to delete a student
        self.delete_window = QDialog(self)
        self.delete_window.setWindowTitle('Delete Student')
        self.delete_window.setGeometry(150, 150, 300, 200)

        layout = QFormLayout()

        self.matric_no_input = QLineEdit()
        layout.addRow("Matric No", self.matric_no_input)

        self.delete_button = QPushButton('Delete Student')
        self.delete_button.clicked.connect(self.delete_student)
        layout.addWidget(self.delete_button)

        self.delete_window.setLayout(layout)
        self.delete_window.exec()

    def delete_student(self):
        matric_no = self.matric_no_input.text()

        cursor.execute("DELETE FROM students WHERE matric_no = ?", (matric_no,))
        conn.commit()
        QMessageBox.information(self, 'Success', 'Student deleted successfully!')
        self.delete_window.close()

# Create an instance of QApplication and run the application
app = QApplication(sys.argv)
window = UniversityApp()
window.show()
sys.exit(app.exec())
