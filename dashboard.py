import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import date
import matplotlib.pyplot as plt


# ✅ Database connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Nisha_2006",  # change if needed
        database="budget_tracker"
    )


# ✅ Dashboard window
def show_dashboard(user_id):
    dashboard = tk.Toplevel()
    dashboard.title("Smart Budget Tracker - Dashboard")
    dashboard.geometry("850x600")
    dashboard.config(bg="#f9f9f9")

    conn = get_connection()
    cursor = conn.cursor()

    # ======== FUNCTIONS ========

    def update_summary():
        """Update total income, expense, and balance"""
        cursor.execute("SELECT monthly_income FROM users WHERE id=%s", (user_id,))
        user_income = cursor.fetchone()[0] or 0

        cursor.execute("""
            SELECT 
                SUM(CASE WHEN type='Expense' THEN amount ELSE 0 END),
                SUM(CASE WHEN type='Income' THEN amount ELSE 0 END)
            FROM transactions WHERE user_id=%s
        """, (user_id,))
        exp, inc = cursor.fetchone()
        total_expense = exp or 0
        total_income = inc or 0
        balance = user_income + total_income - total_expense

        lbl_total_income.config(text=f"₹ {user_income + total_income:.2f}")
        lbl_total_expense.config(text=f"₹ {total_expense:.2f}")
        lbl_balance.config(text=f"₹ {balance:.2f}")

    def set_income():
        """Set or update monthly income"""
        new_income = income_entry.get()
        if not new_income.strip():
            messagebox.showwarning("Empty", "Enter an amount first.")
            return
        try:
            new_income = float(new_income)
            cursor.execute("UPDATE users SET monthly_income=%s WHERE id=%s", (new_income, user_id))
            conn.commit()
            messagebox.showinfo("Updated", f"Monthly income set to ₹{new_income:.2f}")
            update_summary()
        except ValueError:
            messagebox.showerror("Invalid", "Please enter a valid number.")

    def load_transactions(show_graph=False):
        """Load and refresh transactions, optionally show graph"""
        for row in tree.get_children():
            tree.delete(row)
        cursor.execute("""
            SELECT t.id, c.name, t.type, t.amount, t.description, t.date
            FROM transactions t
            JOIN categories c ON t.category_id = c.id
            WHERE t.user_id=%s
            ORDER BY t.date DESC
        """, (user_id,))
        rows = cursor.fetchall()
        for row in rows:
            tree.insert("", "end", values=row)

        update_summary()

        if show_graph:
            # ✅ Prepare data for the graph (category-wise total)
            cursor.execute("""
                SELECT c.name, 
                       SUM(CASE WHEN t.type='Expense' THEN t.amount ELSE 0 END) AS total_expense,
                       SUM(CASE WHEN t.type='Income' THEN t.amount ELSE 0 END) AS total_income
                FROM transactions t
                JOIN categories c ON t.category_id = c.id
                WHERE t.user_id=%s
                GROUP BY c.name
                ORDER BY c.name;
            """, (user_id,))
            data = cursor.fetchall()

            if not data:
                messagebox.showinfo("No Data", "No transactions to display.")
                return

            categories = [d[0] for d in data]
            expenses = [float(d[1]) for d in data]
            incomes = [float(d[2]) for d in data]

            # ✅ Create bar chart
            x = range(len(categories))
            plt.figure(figsize=(8, 5))
            plt.bar(x, expenses, width=0.4, label='Expenses', color='#e74c3c')
            plt.bar([i + 0.4 for i in x], incomes, width=0.4, label='Incomes', color='#2ecc71')
            plt.xticks([i + 0.2 for i in x], categories, rotation=30, ha="right")
            plt.title("Category-wise Income vs Expense")
            plt.xlabel("Category")
            plt.ylabel("Amount (₹)")
            plt.legend()
            plt.tight_layout()
            plt.show()

    def add_transaction():
        """Add income/expense transaction"""
        t_type = type_var.get()
        category = category_var.get()
        amount = amount_var.get()
        desc = desc_entry.get()

        if not category or not amount:
            messagebox.showwarning("Missing Info", "Please fill all fields.")
            return
        try:
            amount = float(amount)
            # get category id
            cursor.execute("SELECT id FROM categories WHERE name=%s", (category,))
            cat_row = cursor.fetchone()
            if not cat_row:
                messagebox.showerror("Error", "Category not found.")
                return
            cat_id = cat_row[0]

            cursor.execute("""
                INSERT INTO transactions (user_id, category_id, amount, type, description, date)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (user_id, cat_id, amount, t_type, desc, date.today()))
            conn.commit()
            messagebox.showinfo("Success", "Transaction added successfully!")
            amount_var.set("")
            desc_entry.delete(0, tk.END)
            load_transactions()
        except ValueError:
            messagebox.showerror("Invalid", "Amount must be numeric.")

    def delete_transaction():
        """Delete selected transaction and renumber IDs"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Select", "Choose a transaction to delete.")
            return

        item = tree.item(selected)
        trans_id = item["values"][0]

        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this transaction?")
        if not confirm:
            return

        try:
            cursor.execute("DELETE FROM transactions WHERE id=%s", (trans_id,))
            conn.commit()

            # ✅ Reorder transaction IDs
            cursor.execute("SET @count = 0;")
            cursor.execute("UPDATE transactions SET id = @count:=@count+1 ORDER BY id;")
            cursor.execute("ALTER TABLE transactions AUTO_INCREMENT = 1;")
            conn.commit()

            messagebox.showinfo("Deleted", "Transaction deleted and IDs renumbered successfully!")
            load_transactions()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete: {e}")

    # ======== UI LAYOUT ========

    tk.Label(dashboard, text="💰 Smart Budget Tracker", font=("Helvetica", 18, "bold"), bg="#f9f9f9").pack(pady=10)

    # Income Section
    frame_income = tk.Frame(dashboard, bg="#f9f9f9")
    frame_income.pack(pady=5)
    tk.Label(frame_income, text="Set / Update Monthly Income: ₹", bg="#f9f9f9").grid(row=0, column=0)
    income_entry = tk.Entry(frame_income, width=10)
    income_entry.grid(row=0, column=1)
    tk.Button(frame_income, text="Save", command=set_income, bg="#3498db", fg="white", width=10).grid(row=0, column=2, padx=10)

    # Summary
    summary_frame = tk.Frame(dashboard, bg="#f9f9f9")
    summary_frame.pack(pady=10)
    tk.Label(summary_frame, text="Total Income:", bg="#f9f9f9").grid(row=0, column=0, padx=10)
    lbl_total_income = tk.Label(summary_frame, text="₹ 0.00", font=("Arial", 12, "bold"), bg="#f9f9f9")
    lbl_total_income.grid(row=0, column=1)
    tk.Label(summary_frame, text="Total Expense:", bg="#f9f9f9").grid(row=0, column=2, padx=10)
    lbl_total_expense = tk.Label(summary_frame, text="₹ 0.00", font=("Arial", 12, "bold"), bg="#f9f9f9")
    lbl_total_expense.grid(row=0, column=3)
    tk.Label(summary_frame, text="Balance:", bg="#f9f9f9").grid(row=0, column=4, padx=10)
    lbl_balance = tk.Label(summary_frame, text="₹ 0.00", font=("Arial", 12, "bold"), bg="#f9f9f9")
    lbl_balance.grid(row=0, column=5)

    # Add Transaction Form
    form_frame = tk.LabelFrame(dashboard, text="Add Transaction", bg="#f9f9f9", padx=10, pady=10)
    form_frame.pack(fill="x", padx=20, pady=10)

    tk.Label(form_frame, text="Type:", bg="#f9f9f9").grid(row=0, column=0, padx=5)
    type_var = tk.StringVar(value="Expense")
    ttk.Combobox(form_frame, textvariable=type_var, values=["Income", "Expense"], width=10).grid(row=0, column=1)

    tk.Label(form_frame, text="Category:", bg="#f9f9f9").grid(row=0, column=2, padx=5)
    category_var = tk.StringVar()
    cursor.execute("SELECT name FROM categories")
    categories = [r[0] for r in cursor.fetchall()]
    ttk.Combobox(form_frame, textvariable=category_var, values=categories, width=15).grid(row=0, column=3)

    tk.Label(form_frame, text="Amount:", bg="#f9f9f9").grid(row=0, column=4, padx=5)
    amount_var = tk.StringVar()
    tk.Entry(form_frame, textvariable=amount_var, width=10).grid(row=0, column=5)

    tk.Label(form_frame, text="Description:", bg="#f9f9f9").grid(row=0, column=6, padx=5)
    desc_entry = tk.Entry(form_frame, width=20)
    desc_entry.grid(row=0, column=7)

    # Buttons
    button_frame = tk.Frame(dashboard, bg="#f9f9f9")
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="➕ Add Transaction", command=add_transaction,
              bg="#27ae60", fg="white", width=18).grid(row=0, column=0, padx=10)

    tk.Button(button_frame, text="📊 View Summary", command=lambda: load_transactions(show_graph=True),
              bg="#2980b9", fg="white", width=18).grid(row=0, column=1, padx=10)

    tk.Button(button_frame, text="🗑 Delete Transaction", command=delete_transaction,
              bg="#c0392b", fg="white", width=18).grid(row=0, column=2, padx=10)

    # Transaction Table
    columns = ("ID", "Category", "Type", "Amount", "Description", "Date")
    tree = ttk.Treeview(dashboard, columns=columns, show="headings", height=10)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")
    tree.pack(fill="x", padx=20, pady=10)

    load_transactions()

    dashboard.mainloop()
