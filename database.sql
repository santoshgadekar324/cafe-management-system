-- Café Management System Database Schema

-- Create database
CREATE DATABASE IF NOT EXISTS cafe_management;
USE cafe_management;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(15),
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Categories table (for menu items)
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Menu items table
CREATE TABLE IF NOT EXISTS menu_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category_id INT,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    image VARCHAR(255),
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
);

-- Tables (restaurant tables)
CREATE TABLE IF NOT EXISTS tables (
    id INT AUTO_INCREMENT PRIMARY KEY,
    table_number INT UNIQUE NOT NULL,
    capacity INT NOT NULL,
    status ENUM('available', 'occupied', 'reserved') DEFAULT 'available',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bookings table
CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    table_id INT,
    booking_date DATE NOT NULL,
    booking_time TIME NOT NULL,
    persons INT NOT NULL,
    status ENUM('pending', 'confirmed', 'cancelled', 'completed') DEFAULT 'pending',
    special_request TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (table_id) REFERENCES tables(id) ON DELETE SET NULL
);

-- Orders table
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    table_id INT,
    order_type ENUM('dine-in', 'takeaway') NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    tax DECIMAL(10, 2) DEFAULT 0.00,
    discount DECIMAL(10, 2) DEFAULT 0.00,
    final_amount DECIMAL(10, 2) NOT NULL,
    status ENUM('pending', 'preparing', 'ready', 'completed', 'cancelled') DEFAULT 'pending',
    payment_status ENUM('pending', 'paid') DEFAULT 'pending',
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (table_id) REFERENCES tables(id) ON DELETE SET NULL
);

-- Order items table
CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    menu_item_id INT,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (menu_item_id) REFERENCES menu_items(id) ON DELETE CASCADE
);

-- Payments table
CREATE TABLE IF NOT EXISTS payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    amount DECIMAL(10, 2) NOT NULL,
    payment_method ENUM('cash', 'card', 'upi', 'online') DEFAULT 'cash',
    status ENUM('pending', 'completed', 'failed') DEFAULT 'pending',
    transaction_id VARCHAR(100),
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
);

-- Insert default admin user (password: admin123)
INSERT INTO users (name, email, password, is_admin) VALUES 
('Admin', 'admin@cafe.com', 'scrypt:32768:8:1$fJzGQxCcEw3vWMhi$1e1a8b8f8c0a9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f', TRUE);

-- Insert sample categories
INSERT INTO categories (name) VALUES 
('Beverages'),
('Appetizers'),
('Main Course'),
('Desserts'),
('Breakfast');

-- Insert sample menu items
INSERT INTO menu_items (name, category_id, description, price, image, is_available) VALUES 
('Cappuccino', 1, 'Classic Italian coffee with steamed milk foam', 120.00, 'cappuccino.jpg', TRUE),
('Espresso', 1, 'Strong black coffee shot', 80.00, 'espresso.jpg', TRUE),
('Green Tea', 1, 'Fresh brewed green tea', 60.00, 'green-tea.jpg', TRUE),
('French Fries', 2, 'Crispy golden fries', 100.00, 'fries.jpg', TRUE),
('Garlic Bread', 2, 'Toasted bread with garlic butter', 120.00, 'garlic-bread.jpg', TRUE),
('Grilled Chicken', 3, 'Tender grilled chicken with herbs', 280.00, 'grilled-chicken.jpg', TRUE),
('Pasta Alfredo', 3, 'Creamy white sauce pasta', 250.00, 'pasta.jpg', TRUE),
('Chocolate Cake', 4, 'Rich chocolate layered cake', 150.00, 'chocolate-cake.jpg', TRUE),
('Pancakes', 5, 'Fluffy pancakes with maple syrup', 180.00, 'pancakes.jpg', TRUE),
('Club Sandwich', 5, 'Triple decker sandwich', 200.00, 'sandwich.jpg', TRUE);

-- Insert sample tables
INSERT INTO tables (table_number, capacity, status) VALUES 
(1, 2, 'available'),
(2, 4, 'available'),
(3, 4, 'available'),
(4, 6, 'available'),
(5, 2, 'available'),
(6, 8, 'available'),
(7, 4, 'available'),
(8, 2, 'available');
