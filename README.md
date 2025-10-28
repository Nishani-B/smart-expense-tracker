💰 Smart Budget Tracker

A simple and user-friendly Python desktop application that helps you track income and expenses, manage budgets, and visualize spending through graphs — built using Tkinter, MySQL, and Matplotlib.

🧩 Features

🏠 User Dashboard



A clean, intuitive dashboard that acts as the control center of your Smart Budget Tracker.
Users can seamlessly add, view, and delete transactions, while instantly viewing updates to their overall financial summary.

💸 Set Monthly Income



Allows each user to define or update their monthly income manually.
This income value is used to calculate the total available balance dynamically after accounting for all transactions.

📥 Add Transactions



Users can easily add transactions by specifying:

Type: Income or Expense
Category: e.g., Food, Transportation, Entertainment, Textile, etc.
Amount: Numeric value of the transaction
Description: Optional note for better tracking
Each new entry is stored in the MySQL database and immediately reflected on the dashboard.
📊 Auto Summary Update



The summary section automatically recalculates and displays:

✅ Total Income (Base income + recorded income transactions)
❌ Total Expense (Sum of all expenses)
💰 Balance (Income − Expense)
All updates are shown live without restarting the app.
📈 Graph Visualization



An integrated bar graph provides a visual summary of spending and income patterns.

The chart displays total income vs. expense grouped by category.
Every time you add or view transactions, the graph updates in real time.
This helps identify where most of your money goes and how well you’re budgeting.
🧾 Transaction Management



Includes full CRUD (Create, Read, Update, Delete) support for financial records.
When a transaction is deleted, the system:

Automatically renumbers the transaction IDs for consistency.
Ensures the AUTO_INCREMENT value in MySQL resets properly.
Refreshes the display and recalculates totals instantly.
🗄 MySQL Integration



All user and transaction data are securely stored in a MySQL database, ensuring persistence between sessions.
The application uses mysql.connector for direct database communication, supporting:

User authentication and income tracking
Category management
Transaction recording with relational consistency
🛠️ Tech Stack
Component	Technology Used
Frontend (GUI)	Tkinter (Python)
Backend (Database)	MySQL
Visualization	Matplotlib
Language	Python 3.10+


📁 Project Structure
Smart_Budget_Tracker/
│
├── main.py              # Entry point / login
├── dashboard.py         # Dashboard GUI with graphs
├── README.md            # Documentation
└── requirements.txt     # (optional) Python dependencies

