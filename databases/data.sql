create database rent_agreements_db;
use rent_agreements_db;
-- CREATE TABLE users (
--     id int PRIMARY KEY auto_increment,
--     username varchar(50) UNIQUE NOT NULL,
--     password varchar(100) NOT NULL  -- This will store a hashed string
-- );
-- delete table rent_agreements_db;
-- DROP TABLE IF EXISTS users;
-- CREATE DATABASE IF NOT EXISTS rent_agreements_db;
-- USE rent_agreements_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);