import mysql.connector
from mysql.connector import Error

def create_connection():
    """Create a connection to MySQL database"""
    try:
        connection = mysql.connector.connect(
            host='localhost',        # Change these credentials
            user='root',             # to match your MySQL setup
            password='password',     # 
            database='student_info_system'
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def create_database():
    """Create database if it doesn't exist"""
    try:
        connection = mysql.connector.connect(
            host='localhost',        # Change these credentials
            user='root',             # to match your MySQL setup
            password='password'      # 
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS student_info_system")
            cursor.close()
            connection.close()
            print("Database created successfully")
    except Error as e:
        print(f"Error creating database: {e}")

def create_tables():
    """Create necessary tables for the student information system"""
    connection = create_connection()
    
    if connection is not None:
        try:
            cursor = connection.cursor()
            
            # Create Colleges table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS colleges (
                    college_id INT AUTO_INCREMENT PRIMARY KEY,
                    college_name VARCHAR(100) NOT NULL,
                    abbreviation VARCHAR(20),
                    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create Programs table with foreign key to Colleges
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS programs (
                    program_id INT AUTO_INCREMENT PRIMARY KEY,
                    program_name VARCHAR(100) NOT NULL,
                    college_id INT NOT NULL,
                    abbreviation VARCHAR(20),
                    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (college_id) REFERENCES colleges(college_id)
                )
            """)
            
            # Create Students table with foreign keys
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    student_id INT AUTO_INCREMENT PRIMARY KEY,
                    id_no VARCHAR(20) UNIQUE NOT NULL,
                    last_name VARCHAR(50) NOT NULL,
                    first_name VARCHAR(50) NOT NULL,
                    gender VARCHAR(10),
                    year_level VARCHAR(5),
                    college_id INT,
                    program_id INT,
                    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (college_id) REFERENCES colleges(college_id),
                    FOREIGN KEY (program_id) REFERENCES programs(program_id)
                )
            """)
            
            connection.commit()
            print("Tables created successfully")
            
        except Error as e:
            print(f"Error creating tables: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

def initialize_database():
    """Initialize the database and tables"""
    create_database()
    create_tables()

# Database operations for colleges
def add_college(college_name, abbreviation=None):
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            sql = "INSERT INTO colleges (college_name, abbreviation) VALUES (%s, %s)"
            values = (college_name, abbreviation)
            cursor.execute(sql, values)
            connection.commit()
            print(f"College '{college_name}' added successfully")
            return cursor.lastrowid
        except Error as e:
            print(f"Error adding college: {e}")
            return None
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

def get_all_colleges():
    connection = create_connection()
    colleges = []
    if connection is not None:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM colleges ORDER BY college_name")
            colleges = cursor.fetchall()
        except Error as e:
            print(f"Error retrieving colleges: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    return colleges

# Database operations for programs
def add_program(program_name, college_id, abbreviation=None):
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            sql = "INSERT INTO programs (program_name, college_id, abbreviation) VALUES (%s, %s, %s)"
            values = (program_name, college_id, abbreviation)
            cursor.execute(sql, values)
            connection.commit()
            print(f"Program '{program_name}' added successfully")
            return cursor.lastrowid
        except Error as e:
            print(f"Error adding program: {e}")
            return None
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

def get_programs_by_college(college_id):
    connection = create_connection()
    programs = []
    if connection is not None:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM programs WHERE college_id = %s ORDER BY program_name", (college_id,))
            programs = cursor.fetchall()
        except Error as e:
            print(f"Error retrieving programs: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    return programs

def get_all_programs():
    connection = create_connection()
    programs = []
    if connection is not None:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT p.*, c.college_name 
                FROM programs p
                JOIN colleges c ON p.college_id = c.college_id
                ORDER BY c.college_name, p.program_name
            """)
            programs = cursor.fetchall()
        except Error as e:
            print(f"Error retrieving programs: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    return programs

# Database operations for students
def add_student(id_no, last_name, first_name, gender, year_level, college_id, program_id):
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            sql = """
                INSERT INTO students 
                (id_no, last_name, first_name, gender, year_level, college_id, program_id) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (id_no, last_name, first_name, gender, year_level, college_id, program_id)
            cursor.execute(sql, values)
            connection.commit()
            print(f"Student {first_name} {last_name} added successfully")
            return cursor.lastrowid
        except Error as e:
            print(f"Error adding student: {e}")
            return None
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

def get_all_students():
    connection = create_connection()
    students = []
    if connection is not None:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT s.*, c.college_name, p.program_name 
                FROM students s
                LEFT JOIN colleges c ON s.college_id = c.college_id
                LEFT JOIN programs p ON s.program_id = p.program_id
                ORDER BY s.last_name, s.first_name
            """)
            students = cursor.fetchall()
        except Error as e:
            print(f"Error retrieving students: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    return students

def update_student(student_id, id_no, last_name, first_name, gender, year_level, college_id, program_id):
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            sql = """
                UPDATE students 
                SET id_no = %s, last_name = %s, first_name = %s, gender = %s, 
                    year_level = %s, college_id = %s, program_id = %s
                WHERE student_id = %s
            """
            values = (id_no, last_name, first_name, gender, year_level, college_id, program_id, student_id)
            cursor.execute(sql, values)
            connection.commit()
            print(f"Student ID {student_id} updated successfully")
            return True
        except Error as e:
            print(f"Error updating student: {e}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

def delete_student(student_id):
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            sql = "DELETE FROM students WHERE student_id = %s"
            cursor.execute(sql, (student_id,))
            connection.commit()
            print(f"Student ID {student_id} deleted successfully")
            return True
        except Error as e:
            print(f"Error deleting student: {e}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

# Call this function at the beginning to set up the database
if __name__ == "__main__":
    initialize_database()