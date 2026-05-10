import mysql.connector
from mysql.connector import Error
from typing import Optional, Dict, Any

from crypto_utils import generate_salt, hash_master_password, verify_master_password, b64e, b64d
from db_config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT


def get_server_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )

def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT
    )


def init_db():
    server_conn = get_server_connection()
    server_cursor = server_conn.cursor()
    server_cursor.execute(
        f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
    )
    server_cursor.close()
    server_conn.close()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) NOT NULL UNIQUE,
            salt VARCHAR(255) NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    ''')
    
    conn.commit()
    cursor.close()
    conn.close()

def create_user(email: str, master_password: str) -> tuple [bool, str]:
email = email.strip().lower()
if not email or '@' not in email:
    return False, 'Shkruaj nje email valid.'
if len(master_password) < 8:
    return False, 'Master password duhet te kete se paku 8 karaktere'

salt = generate_salt()
password_hash = hash_master_password(master_password, salt)

try:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO users(email, salt, password_hash) VALUES (%s, %s, %s)',
        (email, b64e(salt), password_hash)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return True, 'Llogaria u krijua me sukses.'
except mysql.connector.IntegrityError:
    return False, 'Ky email ekziston tashme.'
except Error as e:
    return False, f'Gabim ne databaze: {e}'
