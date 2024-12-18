import hashlib
import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem, QScrollArea, QGroupBox, QGridLayout, QHeaderView, QMessageBox,
    QComboBox, QDialog, QFormLayout, QLineEdit
)
from PyQt6.QtGui import QFont, QIcon, QIntValidator
from PyQt6.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

# Connect to SQLite database
conn = sqlite3.connect('assets/school_database.db')
cursor = conn.cursor()


# Helper function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


class AdminPanel(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("University Admin Panel")
        self.setGeometry(100, 100, 1080, 720)

        # Database connection
        self.conn = sqlite3.connect("assets/school_database.db")

        # White background for a specific widget
        QMainWindow.setStyleSheet(self, """
            background-color: white; 
            color: black;
            }
        """)

        # Main layout
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        self.setCentralWidget(main_widget)

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
        self.conn.close()
        self.close()
        print("Logged out successfully.")


class DashboardAnalytics(QWidget):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        layout = QVBoxLayout(self)

        # Header
        header = QLabel("Dashboard Overview")
        header.setFont(QFont("Artifakt Element Medium", 20))
        layout.addWidget(header)

        # Analytics Grid
        grid = QGridLayout()
        layout.addLayout(grid)

        metrics = self.get_dashboard_metrics()
        for i, (metric_name, value) in enumerate(metrics.items()):
            group = QGroupBox(metric_name)
            group_layout = QVBoxLayout(group)
            value_label = QLabel(value)
            value_label.setFont(QFont("Arial", 12))
            group_layout.addWidget(value_label)
            grid.addWidget(group, i // 2, i % 2)

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
        header_label.setFont(QFont("Arial", 20))
        header_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(header_label)

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

        # Action Buttons
        self.add_user_button = QPushButton("Add User")
        self.add_user_button.clicked.connect(self.add_user)
        self.add_user_button.setStyleSheet(
            "color: white; background-color: #002147; padding: 4px 8px; border-radius: 4px;")
        layout.addWidget(self.add_user_button)

        self.delete_user_button = QPushButton("Delete User")
        self.delete_user_button.clicked.connect(self.delete_user)
        self.delete_user_button.setStyleSheet(
            "color: white; background-color: #002147; padding: 4px 8px; border-radius: 4px;")
        layout.addWidget(self.delete_user_button)

        self.approve_user_button = QPushButton("Approve User")
        self.approve_user_button.clicked.connect(self.approve_user)
        self.approve_user_button.setStyleSheet(
            "color: white; background-color: #002147; padding: 4px 8px; border-radius: 4px;")
        layout.addWidget(self.approve_user_button)

    def populate_users_table(self):
        cursor = self.conn.cursor()

        # Fetch user data from the database (adjust query to match your schema)
        cursor.execute("SELECT username, email, role, last_active, date_added FROM user_management")
        rows = cursor.fetchall()

        self.users_table.setRowCount(len(rows))  # Set row count based on the number of users

        for row_idx, row_data in enumerate(rows):
            # Name and Email
            name_item = QTableWidgetItem(row_data[0])
            email_item = QTableWidgetItem(row_data[1])

            # Role with style
            role_label = QLabel(row_data[2])
            if row_data[2] == "Admin" or "admin":
                role_label.setStyleSheet("color: white; background-color: #1976D2;"
                                         "padding: 4px 8px; border-radius: 4px;")
            elif row_data[2] == "Student" or "student":
                role_label.setStyleSheet("color: black; background-color: #C8E6C9;"
                                         "padding: 4px 8px; border-radius: 4px;")
            elif row_data[2] == "Teacher" or "teacher":
                role_label.setStyleSheet("color: white; background-color: #FF8A65;"
                                         "padding: 4px 8px; border-radius: 4px;")
            role_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Last Active and Date Added
            last_active_item = QTableWidgetItem(row_data[3])
            date_added_item = QTableWidgetItem(row_data[4])

            # Action buttons (e.g., Edit)
            action_layout = QHBoxLayout()
            edit_button = QPushButton("Edit")
            edit_button.setIcon(QIcon.fromTheme("edit"))
            edit_button.setStyleSheet("color: #4CAF50; padding: 2px;")
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

    def view_profiles(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT * FROM general_data")
            users = cursor.fetchall()

            if not users:
                QMessageBox.information(self, "Info", "No users found.")
                return

            dialog = QDialog(self)
            dialog.setWindowTitle("User Profiles")
            dialog.setGeometry(150, 150, 1200, 720)

            layout = QVBoxLayout()

            table = QTableWidget()
            table.setRowCount(len(users))
            table.setColumnCount(12)
            table.setHorizontalHeaderLabels([
                "ID", "Name", "Matric Number", "Level", "Department",
                "Age", "Phone Number", "Email", "Username", "Password", "Approved", "Role"
            ])

            for i, user in enumerate(users):
                for j in range(12):
                    item = QTableWidgetItem(str(user[j]))
                    table.setItem(i, j, item)

            layout.addWidget(table)

            save_button = QPushButton("Save Changes")
            done_button = QPushButton("Done")

            def save_changes():
                try:
                    for i in range(table.rowCount()):
                        updated_values = []
                        for j in range(table.columnCount()):
                            updated_values.append(table.item(i, j).text())

                        update_query = """
                        UPDATE general_data 
                        SET name = ?, matric_no = ?, level = ?, department = ?, age = ?, 
                            phone_number = ?, email = ?, username = ?, password = ?, approved = ?, role = ?
                        WHERE matric_no = ?
                        """
                        cursor.execute(update_query, (*updated_values[1:], updated_values[2]))

                    self.conn.commit()
                    QMessageBox.information(self, "Info", "Changes saved successfully.")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"An error occurred while saving changes: {e}")

            save_button.clicked.connect(save_changes)
            done_button.clicked.connect(dialog.accept)

            button_layout = QHBoxLayout()
            button_layout.addWidget(save_button)
            button_layout.addWidget(done_button)
            layout.addLayout(button_layout)

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
        grades_chart = self.create_grades_chart()
        visualizations_layout.addWidget(grades_chart)

        layout.addWidget(visualizations_group)

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
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT grade, COUNT(*)
            FROM student_grading
            GROUP BY grade
        """)
        data = cursor.fetchall()
        grades, counts = zip(*data) if data else ([], [])

        # Create a matplotlib pie chart
        figure = Figure(figsize=(6, 3))
        canvas = FigureCanvasQTAgg(figure)
        ax = figure.add_subplot(111)
        ax.pie(counts, labels=grades, autopct="%1.1f%%", startangle=90, colors=["#4CAF50", "#2196F3", "#FFC107",
                                                                                "#FF5722", "#E91E63", "#9C27B0"])
        ax.set_title("Grades Distribution")

        return canvas


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


class SyncUserManagementWithGeneralData:
    def __init__(self, conn):
        self.conn = conn

    def sync(self):
        """Synchronize data from general_data to user_management."""
        cursor = self.conn.cursor()

        # Fetch data from general_data
        cursor.execute("SELECT username, email, role FROM general_data")
        general_data_rows = cursor.fetchall()

        # Get existing usernames in user_management
        cursor.execute("SELECT username FROM user_management")
        user_management_usernames = {row[0] for row in cursor.fetchall()}

        # Insert missing users into user_management
        for username, email, role in general_data_rows:
            if username not in user_management_usernames:
                cursor.execute(
                    """
                    INSERT INTO user_management (username, email, role, last_active, date_added)
                    VALUES (?, ?, ?, datetime('now'), datetime('now'))
                    """,
                    (username, email, role)
                )

        self.conn.commit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminPanel()
    window.show()
    sys.exit(app.exec())
