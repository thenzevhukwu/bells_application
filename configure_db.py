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
    grading_id INTEGER PRIMARY KEY AUTOINCREMENT,
    semester_id INTEGER NOT NULL,
    matric_no TEXT NOT NULL,
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

# Courses
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        department TEXT NOT NULL,
        level TEXT NOT NULL,
        
        course1_name TEXT,
        course1_code TEXT,
        course1_unit INTEGER,
        
        course2_name TEXT,
        course2_code TEXT,
        course2_unit INTEGER,
        
        course3_name TEXT,
        course3_code TEXT,
        course3_unit INTEGER,
        
        course4_name TEXT,
        course4_code TEXT,
        course4_unit INTEGER,
        
        course5_name TEXT,
        course5_code TEXT,
        course5_unit INTEGER,
        
        course6_name TEXT,
        course6_code TEXT,
        course6_unit INTEGER,
        
        course7_name TEXT,
        course7_code TEXT,
        course7_unit INTEGER,
        
        course8_name TEXT,
        course8_code TEXT,
        course8_unit INTEGER,
        
        course9_name TEXT,
        course9_code TEXT,
        course9_unit INTEGER,
        
        course10_name TEXT,
        course10_code TEXT,
        course10_unit INTEGER,
        
        course11_name TEXT,
        course11_code TEXT,
        course11_unit INTEGER,
        
        course12_name TEXT,
        course12_code TEXT,
        course12_unit INTEGER,
        
        course13_name TEXT,
        course13_code TEXT,
        course13_unit INTEGER,
        
        course14_name TEXT,
        course14_code TEXT,
        course14_unit INTEGER,
        
        course15_name TEXT,
        course15_code TEXT,
        course15_unit INTEGER
    )
''')



cursor.execute('''CREATE TABLE IF NOT EXISTS Attendance (
    attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    date DATE DEFAULT CURRENT_DATE,
    status TEXT CHECK(status IN ('Present', 'Absent', 'Tardy')),
    FOREIGN KEY (student_id) REFERENCES Students(student_id)
)''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database and tables configured successfully.")
