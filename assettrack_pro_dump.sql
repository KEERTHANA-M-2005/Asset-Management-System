-- AssetTrack Pro Database Dump
-- Prepared By: Keerthana M

-- ===============================
-- DATABASE CREATION
-- ===============================

CREATE DATABASE assettrack_pro;
\c assettrack_pro;

-- ===============================
-- DEPARTMENTS TABLE
-- ===============================

CREATE TABLE departments (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO departments (department_name) VALUES
('HR'),
('IT'),
('Finance'),
('Admin'),
('Operations');


-- ===============================
-- ADMINS TABLE
-- ===============================

CREATE TABLE admins (
    admin_id SERIAL PRIMARY KEY,
    admin_name VARCHAR(150),
    admin_email VARCHAR(150) UNIQUE,
    password_hash TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO admins (admin_name, admin_email, password_hash)
VALUES ('System Admin','admin@company.com','hashed_password');


-- ===============================
-- EMPLOYEES TABLE
-- ===============================

CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    employee_code VARCHAR(50) UNIQUE,
    employee_name VARCHAR(150),
    email VARCHAR(150),
    department_id INT,
    designation VARCHAR(100),
    phone VARCHAR(20),
    joining_date DATE,
    status VARCHAR(50) DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO employees 
(employee_code, employee_name, email, department_id, designation, phone, joining_date)
VALUES
('EMP001','Rahul Sharma','rahul@company.com',2,'Software Engineer','9876543210','2023-06-01'),
('EMP002','Anita Roy','anita@company.com',1,'HR Manager','9876543211','2022-05-10');


-- ===============================
-- ASSET CATEGORIES TABLE
-- ===============================

CREATE TABLE asset_categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO asset_categories (category_name, description) VALUES
('Electronics','Electronic Devices'),
('Furniture','Office Furniture'),
('Accessories','Peripheral Accessories');


-- ===============================
-- ASSETS TABLE
-- ===============================

CREATE TABLE assets (
    asset_id SERIAL PRIMARY KEY,
    asset_tag VARCHAR(100) UNIQUE,
    asset_name VARCHAR(150),
    category_id INT,
    brand VARCHAR(100),
    model VARCHAR(100),
    purchase_date DATE,
    purchase_cost NUMERIC(10,2),
    asset_status VARCHAR(50) DEFAULT 'AVAILABLE',
    location VARCHAR(150),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO assets
(asset_tag, asset_name, category_id, brand, model, purchase_date, purchase_cost, location)
VALUES
('AST001','Dell Laptop',1,'Dell','Latitude 5420','2024-01-01',65000,'Head Office'),
('AST002','Office Chair',2,'Godrej','ErgoChair','2024-02-15',12000,'Head Office');


-- ===============================
-- ASSET ASSIGNMENTS TABLE
-- ===============================

CREATE TABLE asset_assignments (
    assignment_id SERIAL PRIMARY KEY,
    asset_id INT,
    employee_id INT,
    assigned_by_admin_id INT,
    assignment_date DATE,
    expected_return_date DATE,
    assignment_status VARCHAR(50) DEFAULT 'ASSIGNED',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO asset_assignments
(asset_id, employee_id, assigned_by_admin_id, assignment_date, expected_return_date)
VALUES
(1,1,1,'2025-01-01','2026-01-01');


-- ===============================
-- ASSET RETURNS TABLE
-- ===============================

CREATE TABLE asset_returns (
    return_id SERIAL PRIMARY KEY,
    assignment_id INT,
    return_date DATE,
    asset_condition VARCHAR(50),
    remarks TEXT,
    recorded_by_admin_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ===============================
-- ASSET MAINTENANCE TABLE
-- ===============================

CREATE TABLE asset_maintenance (
    maintenance_id SERIAL PRIMARY KEY,
    asset_id INT,
    maintenance_type VARCHAR(100),
    maintenance_date DATE,
    vendor_name VARCHAR(150),
    cost NUMERIC(10,2),
    status VARCHAR(50),
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ===============================
-- ASSET HISTORY TABLE
-- ===============================

CREATE TABLE asset_history (
    history_id SERIAL PRIMARY KEY,
    asset_id INT,
    employee_id INT,
    action_type VARCHAR(50),
    action_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    performed_by_admin_id INT,
    notes TEXT
);

INSERT INTO asset_history
(asset_id, employee_id, action_type, performed_by_admin_id, notes)
VALUES
(1,1,'ASSIGNED',1,'Laptop assigned to Rahul');


-- ===============================
-- INDEXING FOR PERFORMANCE
-- ===============================

CREATE INDEX idx_employee_department ON employees(department_id);
CREATE INDEX idx_asset_category ON assets(category_id);
CREATE INDEX idx_assignment_employee ON asset_assignments(employee_id);
CREATE INDEX idx_assignment_asset ON asset_assignments(asset_id);
