-- betty_db.sql
-- Schema and sample data for Betty's Bird Boutique product pricing database.

CREATE DATABASE IF NOT EXISTS betty_db;
USE betty_db;

DROP TABLE IF EXISTS products;

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    in_stock BOOLEAN NOT NULL DEFAULT TRUE
);

INSERT INTO products (name, category, price, in_stock) VALUES
    ('Large Cockatiel Cage', 'Housing', 129.99, TRUE),
    ('Small Finch Cage', 'Housing', 49.99, TRUE),
    ('Cockatiel Seed Mix', 'Food', 12.49, TRUE),
    ('Parrot Pellet Food', 'Food', 18.99, TRUE),
    ('Millet Spray (3-pack)', 'Food', 6.99, TRUE),
    ('Cuttlebone', 'Health & Accessories', 3.49, TRUE),
    ('Wooden Perch Set', 'Accessories', 14.99, TRUE),
    ('Bird Bath Accessory', 'Accessories', 9.99, TRUE),
    ('Travel Bird Carrier', 'Housing', 34.99, TRUE),
    ('Avian Vitamin Supplement', 'Health & Accessories', 11.49, TRUE);