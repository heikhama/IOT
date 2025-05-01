CREATE DATABASE iotdemo;

USE iotdemo;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(100)
);

INSERT INTO users (username, password) VALUES ('admin', 'admin123');

CREATE TABLE temperature_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sensor_id VARCHAR(50),
    temperature FLOAT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
