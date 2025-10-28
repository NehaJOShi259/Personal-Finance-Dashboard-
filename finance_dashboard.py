import streamlit as st
import pandas as pd
from datetime import date

if "transactions" not in st.session_state:
    st.session_state.transactions = pd.DataFrame(columns=["Type", "Category", "Amount", "Description", "Date"])

st.title("Personal Finance Tracker")

st.header("Add a Transaction")

transaction_type = st.selectbox("Select Transaction Type", ["Income", "Expense"])
category = st.text_input("Category (e.g. Salary, Food, Rent, etc.)")
amount = st.number_input("Amount", min_value=0.0, format="%.2f")
description = st.text_input("Description")
transaction_date = st.date_input("Date", value=date.today())

income_total = st.session_state.transactions[st.session_state.transactions["Type"] == "Income"]["Amount"].sum()
expense_total = st.session_state.transactions[st.session_state.transactions["Type"] == "Expense"]["Amount"].sum()
balance = income_total - expense_total

if st.button("Add Transaction"):
    if transaction_type == "Expense" and income_total == 0:
        st.error("You cannot add an expense before adding income.")
    elif transaction_type == "Expense" and amount > balance:
        st.error("Insufficient balance. Add more income before spending.")
    elif category and amount > 0:
        new_transaction = pd.DataFrame({
            "Type": [transaction_type],
            "Category": [category],
            "Amount": [amount],
            "Description": [description],
            "Date": [transaction_date]
        })
        st.session_state.transactions = pd.concat(
            [st.session_state.transactions, new_transaction],
            ignore_index=True
        )
        st.success("Transaction added successfully.")
    else:
        st.warning("Please enter all fields correctly.")

st.header("Summary")

st.write(f"Total Income: ₹{income_total:.2f}")
st.write(f"Total Expenses: ₹{expense_total:.2f}")
st.write(f"Current Balance: ₹{balance:.2f}")

st.header("Transaction History")
st.dataframe(st.session_state.transactions)
