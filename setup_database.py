import mysql.connector
from mysql.connector import Error

def create_database():
    try:
        # Connect to MySQL server (without specifying a database)
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # replace with your MySQL username
            password='sweety123'   # replace with your MySQL password
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database
            cursor.execute("CREATE DATABASE IF NOT EXISTS Akkani")
            cursor.execute("USE Akkani")
            
            # Create dept table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS dept (
                Dept_id INT AUTO_INCREMENT PRIMARY KEY,
                Dept_name TEXT
            )
            """)
            
            # Create services table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS services (
                service_id INT AUTO_INCREMENT PRIMARY KEY,
                Service_name TEXT
            )
            """)
            
            # Create dept_service junction table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS dept_service (
                ID INT AUTO_INCREMENT PRIMARY KEY,
                s_id INT,
                d_id INT,
                FOREIGN KEY (s_id) REFERENCES services(service_id) ON DELETE CASCADE,
                FOREIGN KEY (d_id) REFERENCES dept(Dept_id) ON DELETE CASCADE
            )
            """)
            
            print("Database 'Akkani' and tables created successfully!")
            
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

if __name__ == "__main__":
    create_database()
