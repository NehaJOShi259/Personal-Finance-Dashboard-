import tkinter as tk
from tkinter import ttk, messagebox
from rapidfuzz import process, fuzz

# -------------------- CATEGORY DATA --------------------
categories = {
    "Income": ["Salary", "Bonus", "Gift", "Investment Return"],
    "Expense": ["Food", "Bills", "Rent", "Shopping", "Travel", "Mutual Fund"]
}

transactions = []

# -------------------- MATCH CATEGORY FUNCTION --------------------
def match_category(user_input):
    all_items = [item for sublist in categories.values() for item in sublist]
    best_match = process.extractOne(user_input, all_items, scorer=fuzz.partial_ratio)
    if best_match and best_match[1] > 70:
        return best_match[0]
    else:
        return None

# -------------------- ADD TRANSACTION FUNCTION --------------------
def add_transaction():
    category_type = category_type_var.get()
    category = category_var.get()
    amount = amount_entry.get().strip()

    if not amount.isdigit():
        messagebox.showerror("Error", "Please enter a valid amount.")
        return

    amount = float(amount)
    matched = match_category(category)

    if matched:
        transactions.append({
            "type": category_type,
            "category": matched,
            "amount": amount
        })
        messagebox.showinfo("Added", f"{category_type} - {matched}: ₹{amount} added successfully.")
    else:
        messagebox.showwarning("Mismatch", f"'{category}' not found in categories. Please check spelling.")

    amount_entry.delete(0, tk.END)
    category_var.set("")

    update_summary()

# -------------------- UPDATE SUMMARY FUNCTION --------------------
def update_summary():
    total_income = sum(t["amount"] for t in transactions if t["type"] == "Income")
    total_expense = sum(t["amount"] for t in transactions if t["type"] == "Expense")
    balance = total_income - total_expense

    income_label.config(text=f"Total Income: ₹{total_income}")
    expense_label.config(text=f"Total Expense: ₹{total_expense}")
    balance_label.config(text=f"Balance: ₹{balance}")

# -------------------- UI SETUP --------------------
root = tk.Tk()
root.title("Smart Expense Tracker")
root.geometry("400x450")
root.config(bg="#f3f3f3")

tk.Label(root, text="Smart Expense Tracker", font=("Arial", 16, "bold"), bg="#f3f3f3").pack(pady=10)

# Category Type (Income/Expense)
category_type_var = tk.StringVar()
tk.Label(root, text="Select Type:", bg="#f3f3f3").pack()
type_dropdown = ttk.Combobox(root, textvariable=category_type_var, values=["Income", "Expense"], state="readonly")
type_dropdown.pack(pady=5)
type_dropdown.current(0)

# Category Dropdown
category_var = tk.StringVar()
tk.Label(root, text="Select or Enter Category:", bg="#f3f3f3").pack()
category_dropdown = ttk.Combobox(root, textvariable=category_var)
category_dropdown.pack(pady=5)

def update_category_dropdown(event):
    selected_type = category_type_var.get()
    category_dropdown["values"] = categories.get(selected_type, [])
type_dropdown.bind("<<ComboboxSelected>>", update_category_dropdown)
update_category_dropdown(None)

# Amount Entry
tk.Label(root, text="Enter Amount (₹):", bg="#f3f3f3").pack()
amount_entry = tk.Entry(root)
amount_entry.pack(pady=5)

# Add Button
tk.Button(root, text="Add Transaction", command=add_transaction, bg="#4CAF50", fg="white", width=20).pack(pady=10)

# Summary Section
summary_frame = tk.Frame(root, bg="#f3f3f3")
summary_frame.pack(pady=15)

income_label = tk.Label(summary_frame, text="Total Income: ₹0", bg="#f3f3f3", font=("Arial", 12))
income_label.pack()
expense_label = tk.Label(summary_frame, text="Total Expense: ₹0", bg="#f3f3f3", font=("Arial", 12))
expense_label.pack()
balance_label = tk.Label(summary_frame, text="Balance: ₹0", bg="#f3f3f3", font=("Arial", 12, "bold"))
balance_label.pack()

root.mainloop()
