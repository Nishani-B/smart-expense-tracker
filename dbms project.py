import mysql.connector

# 🔹 Update these credentials to match your MySQL setup
conn = mysql.connector.connect(
    host="localhost",
    user="root",              # your MySQL username
    password="Nisha_2006"     # your MySQL password
)

cursor = conn.cursor()

# 🔹 Create the database if it doesn't exist
cursor.execute("CREATE DATABASE IF NOT EXISTS budget_tracker;")
cursor.execute("USE budget_tracker;")

# 🔹 Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    category_id INT,
    amount DECIMAL(10,2),
    type ENUM('Income', 'Expense'),
    description VARCHAR(255),
    date DATE,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);
""")

# 🔹 Insert default categories (only if not already present)
categories = [
    ('Food',),
    ('Transportation',),
    ('Bills',),
    ('Shopping',),
    ('Salary',),
    ('Entertainment',),
    ('Health',),
    ('Education',),
    ('Miscellaneous',)
]

cursor.executemany("""
INSERT IGNORE INTO categories (name) VALUES (%s)
""", categories)

conn.commit()

print("✅ Database, tables, and default categories created successfully!")

cursor.close()
conn.close()
