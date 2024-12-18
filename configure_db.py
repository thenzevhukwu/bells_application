import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect("assets/school_database.db")
cursor = conn.cursor()

# Modify the 'general_data' table to add a primary key if not already present
cursor.execute('''
CREATE TABLE IF NOT EXISTS general_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Added primary key
    name TEXT NOT NULL,
    matric_no TEXT UNIQUE NOT NULL,
    level INTEGER,
    department TEXT,
    age INTEGER,
    phone_number TEXT,
    email TEXT UNIQUE NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    approved BOOLEAN,
    role TEXT
)
''')

# Modify the 'user_management' table to include a foreign key linking to 'general_data'
cursor.execute('''
CREATE TABLE IF NOT EXISTS user_management (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username INTEGER NOT NULL,  -- Foreign key to link with 'general_data'
    email TEXT UNIQUE NOT NULL,
    phone_number TEXT,
    last_active TEXT,
    date_added TEXT,
    role TEXT,
    FOREIGN KEY (username) REFERENCES general_data (username) ON DELETE CASCADE
    FOREIGN KEY (phone_number) REFERENCES general_data (phone_number) ON DELETE CASCADE
    FOREIGN KEY (email) REFERENCES general_data (email) ON DELETE CASCADE
    FOREIGN KEY (role) REFERENCES general_data (role) ON DELETE CASCADE
)
''')


# Create the 'student_grading' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS student_grading (
    grading_id INTEGER PRIMARY KEY AUTOINCREMENT,
    semester_id INTEGER NOT NULL,
    matric_no TEXT UNIQUE NOT NULL,
    course_code TEXT NOT NULL,
    assignment_score REAL,
    exam_scores REAL CHECK (exam_scores >= 0 AND exam_scores <= 100),
    test_scores REAL CHECK (test_scores >= 0 AND test_scores <= 100),
    grade TEXT CHECK (grade IN ('A', 'B', 'C', 'D', 'E', 'F')),
    FOREIGN KEY (matric_no) REFERENCES general_data (matric_no)
)
''')

# Create the 'student_cgpa' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS student_cgpa (
    matric_no TEXT,
    cgpa REAL,
    FOREIGN KEY (matric_no) REFERENCES general_data (matric_no)
)
''')

# Create the Students table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Students (
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        matric_no TEXT NOT NULL UNIQUE,
        student_name TEXT
    )
''')

# Create the Student_Courses junction table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Student_Courses (
        student_id INTEGER,
        course_id INTEGER,
        registration_date DATE DEFAULT CURRENT_DATE,
        PRIMARY KEY (student_id, course_id),
        FOREIGN KEY (student_id) REFERENCES Students(student_id),
        FOREIGN KEY (course_id) REFERENCES Courses(course_id)
    )
''')

# Courses table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        department TEXT NOT NULL,  -- Reference the department
        level TEXT NOT NULL,       -- Reference the level (e.g., 100, 200, etc.)
        session TEXT NOT NULL,     -- e.g., "2023/2024"
        semester TEXT NOT NULL,    -- e.g., "1st Semester" 
        course_name TEXT NOT NULL,
        course_code TEXT UNIQUE NOT NULL,
        course_unit INTEGER NOT NULL
    )
''')

# Attendance table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Attendance (
    attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    matric_no TEXT UNIQUE NOT NULL,
    course_code TEXT NOT NULL,
    date DATE DEFAULT CURRENT_DATE,
    status TEXT CHECK(status IN ('Present', 'Absent', 'Tardy')) NOT NULL,
    level TEXT NOT NULL,
    department TEXT NOT NULL,
    FOREIGN KEY (matric_no) REFERENCES general_data(matric_no),
    FOREIGN KEY (course_code) REFERENCES Courses(course_code)
)''')


# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database and tables configured successfully.")
