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