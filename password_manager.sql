CREATE DATABASE IF NOT EXISTS password_manager_aes;
USE password_manager_aes;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    salt VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) 

CREATE TABLE IF NOT EXISTS passwords (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    account VARCHAR(255) NOT NULL,
    username VARCHAR(255),
    category VARCHAR(100) NOT NULL DEFAULT 'General',
    encrypted_password TEXT NOT NULL,
    nonce VARCHAR(255) NOT NULL,
    notes TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_passwords_user
        FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE
)