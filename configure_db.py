import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect("school_database.db")
cursor = conn.cursor()

# Create the 'general_data' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS general_data (
    name TEXT NOT NULL,
    matric_no TEXT UNIQUE NOT NULL,
    level INTEGER,
    department TEXT,
    age INTEGER,
    phone_number TEXT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    approved BOOLEAN,
    role TEXT
)
''')

# Create the 'student_grading' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS student_grading (
    semester_id INTEGER,
    matric_no TEXT,
    course_code TEXT,
    exam_scores REAL,
    test_scores REAL,
    gpa REAL,
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

# Create the Courses table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Courses (
        course_id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_code TEXT NOT NULL UNIQUE,
        course_name TEXT
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

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database and tables configured successfully.")
