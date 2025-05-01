import mysql.connector
from mysql.connector import Error
from tkinter import messagebox

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',       
            user='root',          
            password='2005',            
            database='student_db' 
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def create_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='2005' 
        )
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS student_db")
        print("Database created or already exists")
        connection.close()
    except Error as e:
        print(f"Error creating database: {e}")

def create_tables():
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS colleges (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                code VARCHAR(20) NOT NULL UNIQUE
            )
            """)
            
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS programs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                code VARCHAR(20) NOT NULL,
                college_id INT,
                FOREIGN KEY (college_id) REFERENCES colleges(id)
            )
            """)
            
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                last_name VARCHAR(50) NOT NULL,
                first_name VARCHAR(50) NOT NULL,
                id_number VARCHAR(30) NOT NULL UNIQUE,
                year_level INT,
                gender VARCHAR(10),
                program_id INT NULL,
                FOREIGN KEY (program_id) REFERENCES programs(id) ON DELETE SET NULL
            )
            """)
            
            connection.commit()
            print("Tables created successfully!")
        except Error as e:
            print(f"Error creating tables: {e}")
        finally:
            connection.close()

# Student operations
def save_student(first_name, last_name, id_number, year_level, gender, program_id):
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            
            # Check if student ID already exists
            cursor.execute("SELECT id FROM students WHERE id_number = %s", (id_number,))
            if cursor.fetchone():
                return False, "Student ID number already exists"
            
            # Convert year level from string to integer
            year_mapping = {"1st": 1, "2nd": 2, "3rd": 3, "4th": 4, "5+": 5}
            year_level_int = year_mapping.get(year_level, 1)
            
            # Insert student
            cursor.execute("""
                INSERT INTO students 
                (first_name, last_name, id_number, year_level, gender, program_id) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (first_name, last_name, id_number, year_level_int, gender, program_id))
            
            connection.commit()
            return True, "Student saved successfully!"
        except Error as e:
            print(f"Error saving student: {e}")
            return False, f"Error: {str(e)}"
        finally:
            connection.close()
    return False, "Database connection failed"

def update_student(student_id, first_name, last_name, id_number, year_level, gender, program_id):
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            
            # Check if student ID already exists for another student
            cursor.execute("SELECT id FROM students WHERE id_number = %s AND id != %s", 
                          (id_number, student_id))
            if cursor.fetchone():
                return False, "Student ID number already exists"
            
            # Convert year level from string to integer
            year_mapping = {"1st": 1, "2nd": 2, "3rd": 3, "4th": 4, "5+": 5}
            year_level_int = year_mapping.get(year_level, 1)
            
            # Update student
            cursor.execute("""
                UPDATE students 
                SET first_name = %s, last_name = %s, id_number = %s, 
                    year_level = %s, gender = %s, program_id = %s 
                WHERE id = %s
            """, (first_name, last_name, id_number, year_level_int, gender, program_id, student_id))
            
            connection.commit()
            if cursor.rowcount > 0:
                return True, "Student updated successfully"
            else:
                return False, "No changes made or student not found"
        except Error as e:
            print(f"Error updating student: {e}")
            return False, f"Error: {str(e)}"
        finally:
            connection.close()
    return False, "Database connection failed"

def delete_student(student_id):
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
            connection.commit()
            if cursor.rowcount > 0:
                return True, "Student deleted successfully"
            else:
                return False, "Student not found"
        except Error as e:
            print(f"Error deleting student: {e}")
            return False, f"Error: {str(e)}"
        finally:
            connection.close()
    return False, "Database connection failed"

def get_all_students(page=1, items_per_page=10, search_term=None):
    connection = create_connection()
    students = []
    total_count = 0
    
    if connection is not None:
        try:
            cursor = connection.cursor(dictionary=True)
            
            # Get total count
            count_query = """
                SELECT COUNT(*) as count FROM students s
                LEFT JOIN programs p ON s.program_id = p.id
                LEFT JOIN colleges c ON p.college_id = c.id
            """
            
            params = []
            if search_term:
                count_query += """ WHERE 
                    s.first_name LIKE %s OR 
                    s.last_name LIKE %s OR 
                    s.id_number LIKE %s OR 
                    p.name LIKE %s OR 
                    c.name LIKE %s
                """
                search_pattern = f"%{search_term}%"
                params = [search_pattern]*5
            
            cursor.execute(count_query, params)
            total_count = cursor.fetchone()['count']

            # Get student data with original college info
            query = """
                SELECT 
                    s.id, s.first_name, s.last_name, s.id_number, 
                    s.year_level, s.gender,
                    p.id as program_id, 
                    p.name as program_name, 
                    p.code as program_code,
                    c.id as college_id,
                    c.name as college_name,
                    c.code as college_code,
                    -- Get original college info from program's college
                    (SELECT name FROM colleges WHERE id = p.college_id) as original_college_name,
                    (SELECT code FROM colleges WHERE id = p.college_id) as original_college_code
                FROM students s
                LEFT JOIN programs p ON s.program_id = p.id
                LEFT JOIN colleges c ON p.college_id = c.id
            """
            
            if search_term:
                query += """ WHERE 
                    s.first_name LIKE %s OR 
                    s.last_name LIKE %s OR 
                    s.id_number LIKE %s OR 
                    p.name LIKE %s OR 
                    c.name LIKE %s
                """
            
            query += " ORDER BY s.last_name, s.first_name LIMIT %s OFFSET %s"
            params.extend([items_per_page, (page-1)*items_per_page])
            
            cursor.execute(query, params)
            students = cursor.fetchall()

            # Process results
            for student in students:
                # Handle program display
                if not student['program_id']:
                    student['program_name'] = "N/A"
                    student['program_code'] = "N/A"
                
                # Always use original college info if available
                if student['original_college_name']:
                    student['college_name'] = student['original_college_name']
                    student['college_code'] = student['original_college_code']
                elif not student['college_id']:
                    student['college_name'] = "N/A"
                    student['college_code'] = "N/A"
            
        except Error as e:
            print(f"Error retrieving students: {e}")
        finally:
            connection.close()
    
    return students, total_count

def get_student_by_id(student_id):
    connection = create_connection()
    student = None
    
    if connection is not None:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT s.id, s.first_name, s.last_name, s.id_number, s.year_level, s.gender,
                       s.program_id,
                       COALESCE(p.name, 'N/A') as program_name,
                       COALESCE(p.code, 'N/A') as program_code,
                       p.college_id as college_id,
                       COALESCE(c.name, 'N/A') as college_name,
                       COALESCE(c.code, 'N/A') as college_code
                FROM students s
                LEFT JOIN programs p ON s.program_id = p.id
                LEFT JOIN colleges c ON p.college_id = c.id
                WHERE s.id = %s
            """, (student_id,))
            
            student = cursor.fetchone()
            
        except Error as e:
            print(f"Error retrieving student: {e}")
        finally:
            connection.close()
    
    return student

# College operations
def save_college(name, code):
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()

            cursor.execute("SELECT code FROM colleges WHERE code = %s", (code,))
            if cursor.fetchone():
                return False, "College code already exists"

            cursor.execute("INSERT INTO colleges (name, code) VALUES (%s, %s)", (name, code))
            connection.commit()
            return True, "College saved successfully!"
        except Error as e:
            print(f"Error saving college: {e}")
            return False, f"Error: {str(e)}"
        finally:
            connection.close()
    return False, "Database connection failed"

def get_all_colleges():
    connection = create_connection()
    colleges = []
    if connection is not None:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT id, name, code FROM colleges ORDER BY name")
            colleges = cursor.fetchall()
        except Error as e:
            print(f"Error retrieving colleges: {e}")
        finally:
            connection.close()
    return colleges

def delete_college(college_id):
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            
            cursor.execute("DELETE FROM programs WHERE college_id = %s", (college_id,))
            
            cursor.execute("DELETE FROM colleges WHERE id = %s", (college_id,))
            
            connection.commit()
            
            if cursor.rowcount > 0:
                return True, "College and all its programs deleted successfully"
            else:
                return False, "College not found"
        except Error as e:
            connection.rollback()
            print(f"Error deleting college: {e}")
            return False, f"Error: {str(e)}"
        finally:
            connection.close()
    return False, "Database connection failed"

def update_college(college_id, name, code):
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            
            cursor.execute("SELECT id FROM colleges WHERE code = %s AND id != %s", (code, college_id))
            if cursor.fetchone():
                return False, "College code already exists"

            cursor.execute("UPDATE colleges SET name = %s, code = %s WHERE id = %s", 
                          (name, code, college_id))
            connection.commit()
            if cursor.rowcount > 0:
                return True, "College updated successfully"
            else:
                return False, "No changes made or college not found"
        except Error as e:
            print(f"Error updating college: {e}")
            return False, f"Error: {str(e)}"
        finally:
            connection.close()
    return False, "Database connection failed"

#Program operations
def save_program(name, code, college_id):
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            
            # Check if program code already exists
            cursor.execute("SELECT code FROM programs WHERE code = %s", (code,))
            if cursor.fetchone():
                return False, "Program code already exists"
            
            # Check if college exists
            cursor.execute("SELECT id FROM colleges WHERE id = %s", (college_id,))
            if not cursor.fetchone():
                return False, "Selected college does not exist"
                
            # Insert program
            cursor.execute(
                "INSERT INTO programs (name, code, college_id) VALUES (%s, %s, %s)", 
                (name, code, college_id)
            )
            connection.commit()
            return True, "Program saved successfully!"
        except Error as e:
            print(f"Error saving program: {e}")
            return False, f"Error: {str(e)}"
        finally:
            connection.close()
    return False, "Database connection failed"

def get_all_programs(include_deleted=False):
    connection = create_connection()
    programs = []
    if connection is not None:
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT p.id, p.name, p.code, p.college_id, c.name as college_name, c.code as college_code 
                FROM programs p
                JOIN colleges c ON p.college_id = c.id
            """
            if not include_deleted:
                query += " WHERE p.name != 'N/A (Deleted)'"
            query += " ORDER BY p.name"
            
            cursor.execute(query)
            programs = cursor.fetchall()
        except Error as e:
            print(f"Error retrieving programs: {e}")
        finally:
            connection.close()
    return programs

def get_programs_by_college(college_id):
    connection = create_connection()
    programs = []
    if connection is not None:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT id, name, code 
                FROM programs 
                WHERE college_id = %s
                ORDER BY name
            """, (college_id,))
            programs = cursor.fetchall()
        except Error as e:
            print(f"Error retrieving programs by college: {e}")
        finally:
            connection.close()
    return programs

def update_program(program_id, name, code, college_id):
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            
            # Check if program code already exists for other programs
            cursor.execute("SELECT id FROM programs WHERE code = %s AND id != %s", (code, program_id))
            if cursor.fetchone():
                return False, "Program code already exists"
                
            # Check if college exists
            cursor.execute("SELECT id FROM colleges WHERE id = %s", (college_id,))
            if not cursor.fetchone():
                return False, "Selected college does not exist"

            cursor.execute("""
                UPDATE programs 
                SET name = %s, code = %s, college_id = %s 
                WHERE id = %s
            """, (name, code, college_id, program_id))
            
            connection.commit()
            if cursor.rowcount > 0:
                return True, "Program updated successfully"
            else:
                return False, "No changes made or program not found"
        except Error as e:
            print(f"Error updating program: {e}")
            return False, f"Error: {str(e)}"
        finally:
            connection.close()
    return False, "Database connection failed"

def delete_program(program_id):
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            
            # Instead of deleting, update the program to mark it as "N/A"
            cursor.execute("""
                UPDATE programs 
                SET name = 'N/A (Deleted)', code = 'N/A'
                WHERE id = %s
            """, (program_id,))
            
            connection.commit()
            if cursor.rowcount > 0:
                return True, "Program marked as deleted successfully"
            else:
                return False, "Program not found"
        except Error as e:
            print(f"Error updating program: {e}")
            return False, f"Error: {str(e)}"
        finally:
            connection.close()
    return False, "Database connection failed"

def get_college_program_counts():
    connection = create_connection()
    results = []
    if connection is not None:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT c.id, c.code, c.name, 
                       COUNT(p.id) as program_count,
                       (SELECT COUNT(*) FROM students s 
                        JOIN programs p2 ON s.program_id = p2.id 
                        WHERE p2.college_id = c.id) as student_count
                FROM colleges c
                LEFT JOIN programs p ON c.id = p.college_id
                GROUP BY c.id, c.code, c.name
                ORDER BY c.name
            """)
            results = cursor.fetchall()
        except Error as e:
            print(f"Error retrieving college program counts: {e}")
        finally:
            connection.close()
    return results

def migrate_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='2005',
            database='student_db'
        )
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Drop existing foreign key constraint first
            try:
                cursor.execute("""
                    ALTER TABLE students 
                    DROP FOREIGN KEY students_ibfk_1;
                """)
                print("Dropped foreign key constraint")
            except Error as e:
                print(f"Error dropping foreign key or it doesn't exist: {e}")
            
            # Modify the program_id column to allow NULL values
            try:
                cursor.execute("""
                    ALTER TABLE students 
                    MODIFY program_id INT NULL;
                """)
                print("Modified program_id column to allow NULL values")
            except Error as e:
                print(f"Error modifying column: {e}")
            
            # Add the new foreign key with ON DELETE SET NULL
            try:
                cursor.execute("""
                    ALTER TABLE students 
                    ADD CONSTRAINT students_ibfk_1 
                    FOREIGN KEY (program_id) 
                    REFERENCES programs(id) 
                    ON DELETE SET NULL;
                """)
                print("Added new foreign key with ON DELETE SET NULL")
            except Error as e:
                print(f"Error adding foreign key: {e}")
            
            connection.commit()
            print("Database migration completed successfully!")
            
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    migrate_database()

def initialize_database():
    """Initialize the database and run any necessary migrations"""
    create_database()
    
    # Connect to the database to check schema version or run migrations
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            
            # Check for schema version table
            cursor.execute("SHOW TABLES LIKE 'schema_version'")
            if not cursor.fetchone():
                # Create schema version table if it doesn't exist
                cursor.execute("""
                    CREATE TABLE schema_version (
                        id INT PRIMARY KEY,
                        version INT NOT NULL,
                        applied_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                cursor.execute("INSERT INTO schema_version (id, version) VALUES (1, 0)")
                connection.commit()
            
            # Get current schema version
            cursor.execute("SELECT version FROM schema_version WHERE id = 1")
            result = cursor.fetchone()
            current_version = result[0] if result else 0
            
            # Apply migrations based on version
            if current_version < 1:
                print("Running migration to version 1...")
                
                # Drop existing foreign key constraint first
                try:
                    cursor.execute("""
                        ALTER TABLE students 
                        DROP FOREIGN KEY students_ibfk_1;
                    """)
                    print("Dropped foreign key constraint")
                except Error as e:
                    print(f"Error dropping foreign key or it doesn't exist: {e}")
                
                # Modify the program_id column to allow NULL values
                try:
                    cursor.execute("""
                        ALTER TABLE students 
                        MODIFY program_id INT NULL;
                    """)
                    print("Modified program_id column to allow NULL values")
                except Error as e:
                    print(f"Error modifying column: {e}")
                
                # Add the new foreign key with ON DELETE SET NULL
                try:
                    cursor.execute("""
                        ALTER TABLE students 
                        ADD CONSTRAINT students_ibfk_1 
                        FOREIGN KEY (program_id) 
                        REFERENCES programs(id) 
                        ON DELETE SET NULL;
                    """)
                    print("Added new foreign key with ON DELETE SET NULL")
                except Error as e:
                    print(f"Error adding foreign key: {e}")
                
                # Update schema version
                cursor.execute("UPDATE schema_version SET version = 1 WHERE id = 1")
                connection.commit()
                print("Migration to version 1 completed")
            
            print(f"Database initialized with schema version {current_version}")
            
        except Error as e:
            print(f"Error initializing database: {e}")
        finally:
            connection.close()
    
    # Now create or confirm tables with latest schema
    create_tables()
