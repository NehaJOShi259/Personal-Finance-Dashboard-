import streamlit as st
import pandas as pd
from datetime import date

# -----------------------------

# Configuration

# -----------------------------

st.set_page_config(page_title="Expense Tracker", layout="wide")

DATA_FILE = "expense_data.csv"

# -----------------------------

# Data helpers

# -----------------------------

def load_data():
try:
df = pd.read_csv(DATA_FILE, parse_dates=["Date"])
return df
except FileNotFoundError:
return pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])

def save_data(df):
df.to_csv(DATA_FILE, index=False)

# -----------------------------

# Initialize

# -----------------------------

st.title("Personal Expense Tracker")

if "data" not in st.session_state:
st.session_state.data = load_data()

# -----------------------------

# Sidebar: Add new expense

# -----------------------------

st.sidebar.header("Add New Expense")
transaction_date = st.sidebar.date_input("Date", value=date.today())
category = st.sidebar.selectbox(
"Category",
["Food", "Travel", "Shopping", "Health", "Bills", "Entertainment", "Other"]
)
amount = st.sidebar.number_input("Amount (₹)", min_value=0.0, step=1.0)
description = st.sidebar.text_input("Description")

if st.sidebar.button("Add Expense"):
if amount <= 0 or category == "":
st.sidebar.error("Please enter valid details before submitting.")
else:
new_entry = pd.DataFrame(
[[transaction_date, category, amount, description]],
columns=["Date", "Category", "Amount", "Description"]
)
st.session_state.data = pd.concat([st.session_state.data, new_entry], ignore_index=True)
save_data(st.session_state.data)
st.sidebar.success("Expense added successfully!")

# -----------------------------

# Main: Expense list

# -----------------------------

st.subheader("Expense List")

if not st.session_state.data.empty:
for i, row in st.session_state.data.iterrows():
cols = st.columns([1, 1, 1, 2, 0.5])
cols[0].write(str(row["Date"])[:10])
cols[1].write(row["Category"])
cols[2].write(f"₹{row['Amount']:.2f}")
cols[3].write(row["Description"] if row["Description"] else "-")
if cols[4].button("Delete", key=f"del_{i}"):
st.session_state.data.drop(i, inplace=True)
st.session_state.data.reset_index(drop=True, inplace=True)
save_data(st.session_state.data)
st.rerun()
else:
st.info("No expenses recorded yet.")

# -----------------------------

# Budget Summary

# -----------------------------

st.subheader("Budget Summary")
budget = st.number_input("Enter your total budget (₹)", min_value=0.0, step=500.0)

if not st.session_state.data.empty and budget > 0:
total_spent = st.session_state.data["Amount"].sum()
balance = budget - total_spent

```
st.write(f"**Total Spent:** ₹{total_spent:.2f}")
st.write(f"**Remaining Balance:** ₹{balance:.2f}")

if total_spent > budget:
    st.error("Budget exceeded! Try to cut down expenses.")
else:
    st.success("You are within budget.")

st.bar_chart(pd.DataFrame({"Spent": [total_spent], "Remaining": [balance]}).T)
```

# -----------------------------

# Download Button

# -----------------------------

st.download_button(
label="Download Expenses CSV",
data=st.session_state.data.to_csv(index=False),
file_name="expenses.csv",
mime="text/csv",
)

