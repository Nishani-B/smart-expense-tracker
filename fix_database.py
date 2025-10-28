import mysql.connector

# Connect to your MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Nisha_2006",
    database="budget_tracker"
)

cursor = conn.cursor()

# ✅ Add the missing column if not exists
try:
    cursor.execute("ALTER TABLE users ADD COLUMN monthly_income DECIMAL(10,2) DEFAULT 0;")
    print("✅ Column 'monthly_income' added successfully!")
except mysql.connector.errors.ProgrammingError as e:
    if "Duplicate column name" in str(e):
        print("ℹ️ Column 'monthly_income' already exists.")
    else:
        raise

conn.commit()
conn.close()
