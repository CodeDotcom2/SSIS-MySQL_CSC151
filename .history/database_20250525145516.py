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

def save_student(first_name, last_name, id_number, year_level, gender, program_id):
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            
            cursor.execute("SELECT id FROM students WHERE id_number = %s", (id_number,))
            if cursor.fetchone():
                return False, "Student ID number already exists"
            

            year_mapping = {"1st": 1, "2nd": 2, "3rd": 3, "4th": 4, "5+": 5}
            year_level_int = year_mapping.get(year_level, 1)

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
            
            cursor.execute("SELECT id FROM students WHERE id_number = %s AND id != %s", 
                          (id_number, student_id))
            if cursor.fetchone():
                return False, "Student ID number already exists"

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

def get_all_students(page=1, items_per_page=10, search_term=None, search_field="all", sort_field="id_number", sort_direction="ascending"):
    connection = create_connection()
    students = []
    total_count = 0
    
    if connection is not None:
        try:
            cursor = connection.cursor(dictionary=True)
            
            # Base query for counting and data retrieval
            count_query = """
                SELECT COUNT(*) as count FROM students s
                LEFT JOIN programs p ON s.program_id = p.id
                LEFT JOIN colleges c ON p.college_id = c.id
            """
            
            query = """
                SELECT 
                    s.id, 
                    s.first_name, 
                    s.last_name, 
                    s.id_number, 
                    s.year_level, 
                    s.gender,
                    s.program_id,
                    COALESCE(p.name, 'N/A') as program_name, 
                    COALESCE(p.code, 'N/A') as program_code,
                    COALESCE(c.id, 0) as college_id,
                    COALESCE(c.name, 'N/A') as college_name, 
                    COALESCE(c.code, 'N/A') as college_code
                FROM students s
                LEFT JOIN programs p ON s.program_id = p.id
                LEFT JOIN colleges c ON p.college_id = c.id
            """
            
            params = []
            where_clause = ""
            
            # Add WHERE clause if search term is provided
            if search_term:
                # Map year level text to numerical values for search
                year_mapping = {"1st": 1, "2nd": 2, "3rd": 3, "4th": 4, "5+": 5}
                year_level_value = None
                
                # Check if search_term matches any year level text
                for text, value in year_mapping.items():
                    if text.lower() == search_term.lower():
                        year_level_value = value
                        break
                
                # Construct appropriate WHERE clause based on search field
                where_clause = ""
                
                if search_field == "all":
                    where_clause = """ WHERE 
                        s.first_name LIKE %s OR 
                        s.last_name LIKE %s OR 
                        s.id_number LIKE %s OR 
                        s.gender LIKE %s OR
                        COALESCE(p.name, '') LIKE %s OR
                        COALESCE(p.code, '') LIKE %s OR
                        COALESCE(c.name, '') LIKE %s OR
                        COALESCE(c.code, '') LIKE %s
                    """
                    search_pattern = f"%{search_term}%"
                    params = [search_pattern] * 8
                    
                    # Add year level search if applicable
                    if year_level_value is not None:
                        where_clause += " OR s.year_level = %s"
                        params.append(year_level_value)
                
                elif search_field == "id_number":
                    where_clause = " WHERE s.id_number LIKE %s"
                    params = [f"%{search_term}%"]
                
                elif search_field == "last_name":
                    where_clause = " WHERE s.last_name LIKE %s"
                    params = [f"%{search_term}%"]
                
                elif search_field == "first_name":
                    where_clause = " WHERE s.first_name LIKE %s"
                    params = [f"%{search_term}%"]
                
                elif search_field == "gender":
                    where_clause = " WHERE s.gender LIKE %s"
                    params = [f"%{search_term}%"]
                
                elif search_field == "year_level":
                    if year_level_value is not None:
                        where_clause = " WHERE s.year_level = %s"
                        params = [year_level_value]
                    else:
                        # Handle direct year level number input
                        try:
                            year_number = int(search_term)
                            if 1 <= year_number <= 5:
                                where_clause = " WHERE s.year_level = %s"
                                params = [year_number]
                        except ValueError:
                            # Not a valid year level, use a condition that will return no results
                            where_clause = " WHERE 1=0"
                
                elif search_field == "college":
                    where_clause = " WHERE COALESCE(c.name, '') LIKE %s OR COALESCE(c.code, '') LIKE %s"
                    params = [f"%{search_term}%", f"%{search_term}%"]
                
                elif search_field == "program":
                    where_clause = " WHERE COALESCE(p.name, '') LIKE %s OR COALESCE(p.code, '') LIKE %s"
                    params = [f"%{search_term}%", f"%{search_term}%"]
                
                count_query += where_clause
                query += where_clause
            
            # Execute count query
            cursor.execute(count_query, params)
            result = cursor.fetchone()
            total_count = result['count'] if result else 0
            
            # Add ORDER BY clause based on sort_field and sort_direction
            order_by = ""
            if sort_field == "id_number":
                order_by = "s.id_number"
            elif sort_field == "last_name":
                order_by = "s.last_name, s.first_name"
                if sort_direction == "descending":
                    order_by = "s.last_name DESC, s.first_name DESC"
                else:
                    order_by = "s.last_name ASC, s.first_name ASC"
                    
            else:
                order_by = "s.id_number"  # default
            
            if sort_direction == "descending":
                order_by += " DESC"
            else:
                order_by += " ASC"
                
            query = f"""
                WITH sorted_students AS (
                    {query}
                    {f"WHERE {where_clause}" if search_term else ""}
                    ORDER BY {order_by}
                )
                SELECT * FROM sorted_students
                LIMIT %s OFFSET %s
            """
            
            offset = (page - 1) * items_per_page
            cursor.execute(query, params + [items_per_page, offset])
            students = cursor.fetchall()
            
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
                SELECT 
                    s.id, 
                    s.first_name, 
                    s.last_name, 
                    s.id_number, 
                    s.year_level, 
                    s.gender,
                    s.program_id,
                    COALESCE(p.name, 'N/A') as program_name,
                    COALESCE(p.code, 'N/A') as program_code,
                    COALESCE(c.id, 0) as college_id,
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
            cursor.execute("""
                SELECT 
                    c.id, c.name, c.code,
                    (SELECT COUNT(*) FROM programs WHERE college_id = c.id) as program_count,
                    (SELECT COUNT(*) FROM students s 
                     JOIN programs p ON s.program_id = p.id 
                     WHERE p.college_id = c.id) as student_count
                FROM colleges c
                ORDER BY c.name
            """)
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
            
            # 1. First check if college has any students through its programs
            cursor.execute("""
                SELECT COUNT(*) FROM students s
                JOIN programs p ON s.program_id = p.id
                WHERE p.college_id = %s
            """, (college_id,))
            has_students = cursor.fetchone()[0] > 0
            
            if has_students:
                # 2. If has students, set their program_id to NULL
                cursor.execute("""
                    UPDATE students s
                    JOIN programs p ON s.program_id = p.id
                    SET s.program_id = NULL
                    WHERE p.college_id = %s
                """, (college_id,))
            
            # 3. Delete all programs in this college
            cursor.execute("DELETE FROM programs WHERE college_id = %s", (college_id,))
            
            # 4. Finally delete the college
            cursor.execute("DELETE FROM colleges WHERE id = %s", (college_id,))
            
            connection.commit()
            return True, "College and its programs deleted successfully"
            
        except Error as e:
            connection.rollback()
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

def is_college_referenced(college_id):
    """Check if college has any students through its programs"""
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT EXISTS (
                    SELECT 1 FROM students s
                    JOIN programs p ON s.program_id = p.id
                    WHERE p.college_id = %s
                ) as is_referenced
            """, (college_id,))
            return cursor.fetchone()[0]
        finally:
            connection.close()
    return True  # Assume referenced if connection fails

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
                AND name != 'N/A'
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
            
            # 1. First check if program has any students
            cursor.execute("""
                SELECT COUNT(*) FROM students 
                WHERE program_id = %s
            """, (program_id,))
            has_students = cursor.fetchone()[0] > 0
            
            if has_students:
                # 2. If has students, soft delete
                cursor.execute("""
                    UPDATE programs 
                    SET name = 'N/A (Deleted)', code = 'N/A'
                    WHERE id = %s
                """, (program_id,))
                message = "Program marked as deleted (kept for existing students)"
            else:
                # 3. If no students, hard delete
                cursor.execute("""
                    DELETE FROM programs 
                    WHERE id = %s
                """, (program_id,))
                message = "Program permanently deleted"
            
            # 4. NEW: More aggressive cleanup of all unreferenced N/A programs
            cursor.execute("""
                DELETE FROM programs 
                WHERE name = 'N/A (Deleted)' 
                AND code = 'N/A'
                AND id NOT IN (
                    SELECT DISTINCT program_id 
                    FROM students 
                    WHERE program_id IS NOT NULL
                )
            """)
            
            connection.commit()
            return True, message
            
        except Error as e:
            connection.rollback()
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
    
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            
            cursor.execute("SHOW TABLES LIKE 'schema_version'")
            if not cursor.fetchone():
                cursor.execute("""
                    CREATE TABLE schema_version (
                        id INT PRIMARY KEY,
                        version INT NOT NULL,
                        applied_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                cursor.execute("INSERT INTO schema_version (id, version) VALUES (1, 0)")
                connection.commit()
            
            cursor.execute("SELECT version FROM schema_version WHERE id = 1")
            result = cursor.fetchone()
            current_version = result[0] if result else 0
            
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
    
    create_tables()