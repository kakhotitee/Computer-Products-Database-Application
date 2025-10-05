
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS categories CASCADE;


CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    description TEXT
);


CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    brand VARCHAR(50) NOT NULL,
    model VARCHAR(100) NOT NULL,
    full_name VARCHAR(200),
    price DECIMAL(10,2),
    rating DECIMAL(3,2),
    stock_quantity INTEGER,
    warranty_months INTEGER,
    category_id INTEGER REFERENCES categories(category_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO categories (category_name, description) VALUES
('Видеокарты', 'Графические карты для игр и работы'),
('Процессоры', 'Центральные процессоры'),
('Память', 'Оперативная память'),
('Материнские платы', 'Основные платы'),
('SSD', 'Твердотельные накопители'),
('Блоки питания', 'Источники питания');

INSERT INTO products (brand, model, full_name, price, rating, stock_quantity, warranty_months, category_id) VALUES

('ASUS', 'ROG Strix RTX 4080', 'ASUS ROG Strix RTX 4080 16GB GDDR6X', 120000, 4.8, 5, 36, 1),
('MSI', 'Gaming X Trio RTX 4070 Ti', 'MSI Gaming X Trio RTX 4070 Ti 12GB GDDR6X', 85000, 4.6, 8, 36, 1),
('Gigabyte', 'AORUS RTX 4090', 'Gigabyte AORUS RTX 4090 24GB GDDR6X', 180000, 4.9, 3, 48, 1),


('Intel', 'Core i9-14900K', 'Intel Core i9-14900K 3.2GHz', 55000, 4.7, 15, 36, 2),
('AMD', 'Ryzen 7 7800X3D', 'AMD Ryzen 7 7800X3D 4.2GHz', 45000, 4.8, 12, 36, 2),
('Intel', 'Core i5-13600KF', 'Intel Core i5-13600KF 3.5GHz', 30000, 4.6, 20, 36, 2),


('Corsair', 'Vengeance RGB 32GB', 'Corsair Vengeance RGB 32GB DDR5 6000MHz', 15000, 4.5, 25, 24, 3),
('Kingston', 'Fury Beast 16GB', 'Kingston Fury Beast 16GB DDR5 5600MHz', 8000, 4.4, 30, 24, 3),


('ASUS', 'ROG Maximus Z790 Hero', 'ASUS ROG Maximus Z790 Hero', 45000, 4.6, 6, 36, 4),
('MSI', 'MAG B650 Tomahawk', 'MSI MAG B650 Tomahawk WiFi', 35000, 4.5, 10, 36, 4),


('Samsung', '980 Pro 1TB', 'Samsung 980 Pro 1TB NVMe SSD', 12000, 4.3, 20, 60, 5),
('Kingston', 'KC3000 2TB', 'Kingston KC3000 2TB NVMe SSD', 25000, 4.6, 15, 60, 5),


('Corsair', 'RM850x', 'Corsair RM850x 850W Power Supply', 14000, 4.2, 10, 120, 6),
('be quiet!', 'Straight Power 11 1000W', 'be quiet! Straight Power 11 1000W', 20000, 4.7, 5, 120, 6);
