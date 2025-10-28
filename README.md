💰 Smart Budget Tracker

A simple and user-friendly Python desktop application that helps you track income and expenses, manage budgets, and visualize spending through graphs — built using Tkinter, MySQL, and Matplotlib.

🧩 Features

✅ User Dashboard — Add, delete, and view all your transactions
✅ Set Monthly Income — Manage or update your total monthly income
✅ Add Transactions — Categorize entries as Income or Expense
✅ Auto Summary Update — View total income, expenses, and balance instantly
✅ Graph Visualization — Category-wise income and expense bar chart
✅ Transaction Management — Auto-renumber IDs when a transaction is deleted
✅ MySQL Integration — All data is stored securely in a MySQL database

🛠️ Tech Stack
Component	Technology Used
Frontend (GUI)	Tkinter (Python)
Backend (Database)	MySQL
Visualization	Matplotlib
Language	Python 3.10+

🗄️ Database Setup
CREATE DATABASE IF NOT EXISTS budget_tracker;
USE budget_tracker;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    monthly_income DECIMAL(10,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create categories table
CREATE TABLE IF NOT EXISTS categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- Create transactions table
CREATE TABLE IF NOT EXISTS transactions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    category_id INT,
    amount DECIMAL(10,2),
    type ENUM('Income', 'Expense'),
    description VARCHAR(255),
    date DATE,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- Add default categories
INSERT IGNORE INTO categories (name)
VALUES ('Food'), ('Transport'), ('Rent'), ('Salary'), ('Entertainment'), ('Shopping');


📁 Project Structure
Smart_Budget_Tracker/
│
├── main.py              # Entry point / login
├── dashboard.py         # Dashboard GUI with graphs
├── README.md            # Documentation
└── requirements.txt     # (optional) Python dependencies
