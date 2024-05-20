import mysql.connector
from mysql.connector import Error
import hashlib

class UserDao:
    def __init__(self, db_config):
        self.db_config = db_config

    def connect(self):
        try:
            self.conn = mysql.connector.connect(**self.db_config)
            self.cursor = self.conn.cursor()
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            self.conn = None
            self.cursor = None

    def disconnect(self):
        if self.cursor and self.conn:
            self.cursor.close()
            self.conn.close()

    def create_user_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL
        );
        '''
        self.connect()
        self.cursor.execute(query)
        self.conn.commit()
        self.disconnect()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def insert_user(self, email, password):
        hashed_password = self.hash_password(password)
        query = "INSERT INTO users (email, password) VALUES (%s, %s)"
        self.connect()
        try:
            self.cursor.execute(query, (email, hashed_password))
            self.conn.commit()
        except Error as e:
            print(f"Error inserting user: {e}")
        self.disconnect()

    def get_user_by_email(self, email):
        query = "SELECT * FROM users WHERE email = %s"
        self.connect()
        self.cursor.execute(query, (email,))
        user = self.cursor.fetchone()
        self.disconnect()
        return user

    def verify_user(self, email, password):
        user = self.get_user_by_email(email)
        if user:
            stored_password = user[2]  # Assuming the password is the third field in the table
            return stored_password == self.hash_password(password)
        return False

if __name__ == "__main__":
    db_config = {
        'user': 'root',
        'password': 'abdellah2004.7',
        'database': 'webLog'
    }

    user_dao = UserDao(db_config)
    user_dao.create_user_table()

    # Example of inserting a new user
    user_dao.insert_user('test@example.com', 'securepassword123')

    # Example of verifying a user
    email = 'test@example.com'
    password = 'securepassword123'
    if user_dao.verify_user(email, password):
        print(f"User {email} verified successfully.")
    else:
        print(f"Failed to verify user {email}.")

    """ssh_log_dao = SSHLogDAO(db_config)

    results = ssh_log_dao.get_failed_login_attempts_by_date()
    
    for log_date, failed_attempts in results:
        print(f"Date: {log_date}, Failed Attempts: {failed_attempts}")"""