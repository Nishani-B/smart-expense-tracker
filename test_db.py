import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",       # change if your MySQL username is different
        password="Nisha_2006",  # replace with your MySQL password
        database="budget_tracker"         # replace with your database name
    )
    if conn.is_connected():
        print("✅ Successfully connected to MySQL database!")
    conn.close()
except mysql.connector.Error as e:
    print("❌ MySQL connection failed:", e)
