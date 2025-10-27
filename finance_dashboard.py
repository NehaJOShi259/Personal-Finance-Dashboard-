import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Personal Finance Dashboard", layout="wide")
st.title("Personal Finance Dashboard")

DATA_FILE = "transactions.csv"

# --- Load existing data ---
if os.path.exists(DATA_FILE):
    data = pd.read_csv(DATA_FILE, parse_dates=["Date"])
else:
    data = pd.DataFrame(columns=["Date", "Type", "Category", "Amount"])

# Store in session state
if "data" not in st.session_state:
    st.session_state.data = data

# --- Sidebar: Add Transaction ---
st.sidebar.header("Add Transaction")
transaction_type = st.sidebar.selectbox("Type", ["Income", "Expense"])
category = st.sidebar.text_input("Category (e.g., Salary, Rent, Grocery)")
amount = st.sidebar.number_input("Amount (₹)", min_value=0.0, step=0.01)
date = st.sidebar.date_input("Date")

if st.sidebar.button("Add Transaction"):
    if category.strip() == "":
        st.sidebar.error("Please enter a category.")
    else:
        new_entry = {
            "Date": pd.to_datetime(date),
            "Type": transaction_type,
            "Category": category.strip(),
            "Amount": amount,
        }
        st.session_state.data = pd.concat(
            [st.session_state.data, pd.DataFrame([new_entry])], ignore_index=True
        )
        st.session_state.data.to_csv(DATA_FILE, index=False)
        st.sidebar.success("Transaction added successfully!")

# --- Main Dashboard ---
data = st.session_state.data

if not data.empty:
    st.subheader("Transactions")
    data_display = data.sort_values(by="Date", ascending=False).reset_index(drop=True)
    st.dataframe(data_display)

    # --- Delete Transaction ---
    st.subheader("Delete a Transaction")
    if len(data_display) > 0:
        delete_index = st.number_input(
            "Enter the row number to delete (starting from 0)",
            min_value=0,
            max_value=len(data_display) - 1,
            step=1,
        )
        if st.button("Delete Selected Transaction"):
            st.session_state.data.drop(delete_index, inplace=True)
            st.session_state.data.to_csv(DATA_FILE, index=False)
            st.success("Transaction deleted successfully!")
            st.experimental_rerun()

    # --- Summary ---
    st.subheader("Summary")
    total_income = data[data["Type"] == "Income"]["Amount"].sum()
    total_expense = data[data["Type"] == "Expense"]["Amount"].sum()
    balance = total_income - total_expense

    st.write(f"**Total Income:** ₹{total_income:,.2f}")
    st.write(f"**Total Expenses:** ₹{total_expense:,.2f}")
    st.write(f"**Balance:** ₹{balance:,.2f}")

    # --- Simple Chart ---
    expenses = data[data["Type"] == "Expense"].groupby("Category")["Amount"].sum()

    if not expenses.empty:
        fig, ax = plt.subplots()
        expenses.plot(kind="bar", ax=ax, color="orange")
        ax.set_ylabel("Amount (₹)")
        ax.set_title("Expenses by Category")
        st.pyplot(fig)
        plt.close(fig)

    # --- Download CSV ---
    st.download_button(
        label="Download Transactions CSV",
        data=data.to_csv(index=False).encode("utf-8"),
        file_name="transactions.csv",
        mime="text/csv",
    )
else:
    st.info("No transactions yet. Add some using the sidebar.")
