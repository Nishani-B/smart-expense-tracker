import tkinter as tk
from tkinter import ttk, messagebox
import database


def open_add_transaction(user_id, parent, refresh_callback):
    """Opens a window to add a new transaction."""
    add_window = tk.Toplevel(parent)
    add_window.title("Add Transaction")
    add_window.geometry("400x400")
    add_window.resizable(False, False)

    tk.Label(add_window, text="Add New Transaction", font=("Arial", 16, "bold"), fg="darkblue").pack(pady=10)

    # Fields
    tk.Label(add_window, text="Category").pack()
    category_combo = ttk.Combobox(add_window, width=30, state="readonly")
    category_combo.pack(pady=5)

    tk.Label(add_window, text="Type").pack()
    type_combo = ttk.Combobox(add_window, width=30, state="readonly", values=["Income", "Expense"])
    type_combo.pack(pady=5)

    tk.Label(add_window, text="Amount").pack()
    amount_entry = tk.Entry(add_window, width=32)
    amount_entry.pack(pady=5)

    tk.Label(add_window, text="Description").pack()
    desc_entry = tk.Entry(add_window, width=32)
    desc_entry.pack(pady=5)

    # Fetch categories from DB
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM categories")
    categories = cursor.fetchall()
    category_combo["values"] = [c[1] for c in categories]
    cursor.close()
    conn.close()

    # Save transaction
    def save_transaction():
        category_name = category_combo.get()
        txn_type = type_combo.get()
        amount = amount_entry.get()
        desc = desc_entry.get()

        if not category_name or not txn_type or not amount:
            messagebox.showerror("Error", "Please fill all required fields!")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number!")
            return

        # Get category_id
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM categories WHERE name=%s", (category_name,))
        category_id = cursor.fetchone()

        if not category_id:
            messagebox.showerror("Error", "Category not found!")
            return

        # Insert transaction
        cursor.execute("""
            INSERT INTO transactions (user_id, category_id, type, amount, description, date)
            VALUES (%s, %s, %s, %s, %s, NOW())
        """, (user_id, category_id[0], txn_type, amount, desc))
        conn.commit()

        cursor.close()
        conn.close()

        messagebox.showinfo("Success", "Transaction added successfully!")
        add_window.destroy()
        refresh_callback()  # Refresh dashboard table

    # Buttons
    tk.Button(add_window, text="Save Transaction", command=save_transaction, bg="lightgreen", width=20).pack(pady=15)
    tk.Button(add_window, text="Cancel", command=add_window.destroy, bg="tomato", width=20).pack(pady=5)
