# University Login Application

This is a **University Login Application** built using **PyQt6** for the graphical user interface (GUI) and **SQLite3** for secure data storage. The application allows **Students**, **Teachers**, and **Admin** to log in and access different features based on their roles.

## Features

- **Student Login**: Students can log in to access their courses, grades, and personal information.
- **Teacher Login**: Teachers can log in to manage courses, grade submissions, and interact with students.
- **Admin Login**: Admin users have the highest access level, allowing them to manage all users (students and teachers) and configure system settings.

## Technologies Used

- **Frontend**:
    - **PyQt6**: Used for creating the graphical user interface (GUI), including login forms, buttons, and input fields.

- **Backend**:
    - **SQLite3**: A lightweight database used to securely store user data such as login credentials, user roles, and additional personal information.

## Setup Instructions

### Prerequisites

Before you begin, make sure you have the following installed:

- **Python 3.x** (preferably the latest version)
- **PyQt6**: For creating the user interface. You can install it using `pip`:
  ```bash
  pip install pyqt6

### SQLite3 Database

The application uses an **SQLite3** database to store and retrieve user information. It contains tables for users (students, teachers, and admin) with the following structure:

- **Users Table**:
    - `id` (INTEGER): The unique ID for each user.
    - `username` (TEXT): The username for the user.
    - `password` (TEXT): The password (hashed for security).
    - `role` (TEXT): Defines the role of the user: `student`, `teacher`, or `admin`.

### Configuration

Ensure the database is properly set up with the necessary tables. If the database is not present, the application will create it upon first run.

### Login Form Details

- **Student Login**:
    - Username: `John`
    - Password: `fshaw`

- **Teacher Login**:
    - Username: `Florence`
    - Password: `fshaw`

- **Admin Login**:
    - Username: `admin-user`
    - Password: `admin-admin`

## Application Workflow

1. When the application is launched, the login interface is displayed with three options: **Student**, **Teacher**, and **Admin**.
2. The user selects their role, enters their credentials (username and password), and submits the form.
3. The application checks the entered credentials against the SQLite3 database:
    - If valid, the user is granted access to the corresponding section (Student Dashboard, Teacher Dashboard, or Admin Panel).
    - If invalid, the user is prompted to retry.

## Contributions

We welcome contributions! If you would like to contribute to the project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.


## Contact

For any questions or feedback, you can reach us at [favour.adimora@bellsuniversity.edu.ng].

---

Thank you for using the University Login Application!
