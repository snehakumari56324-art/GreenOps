CREATE DATABASE IF NOT EXISTS greenops;
USE greenops;

CREATE TABLE IF NOT EXISTS cloud_resources (
    id INT AUTO_INCREMENT PRIMARY KEY,
    resource_id VARCHAR(100) NOT NULL UNIQUE,
    resource_type VARCHAR(50) NOT NULL,
    region VARCHAR(50),
    instance_type VARCHAR(50),
    status VARCHAR(30),
    cpu_utilization FLOAT DEFAULT 0,
    memory_utilization FLOAT DEFAULT 0,
    estimated_cost FLOAT DEFAULT 0,
    carbon_emission FLOAT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
