-- init.sql
CREATE DATABASE IF NOT EXISTS cloud_db;
USE cloud_db;

CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    program VARCHAR(100) NOT NULL
);

INSERT INTO students (name, program) VALUES 
    ('Alice Smith', 'ECE Cloud Computing'),
    ('Bob Johnson', 'Software Engineering'),
    ('Charlie Davis', 'Data Science');
