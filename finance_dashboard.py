import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

if "transactions" not in st.session_state:
    st.session_state.transactions = pd.DataFrame(columns=["Type", "Category", "Amount", "Description", "Date"])

st.title("Personal Finance Tracker")

st.header("Add a Transaction")

transaction_type = st.selectbox("Select Transaction Type", ["Income", "Expense"])

if transaction_type == "Income":
    income_category = st.selectbox("Select Income Category", ["Salary", "Business", "Freelance", "Other"])
    if income_category == "Other":
        category = st.text_input("Enter Custom Income Category")
    else:
        category = income_category
else:
    expense_category = st.selectbox("Select Expense Category", ["Food", "Rent", "Shopping", "Travel", "Bills", "Other"])
    if expense_category == "Other":
        category = st.text_input("Enter Custom Expense Category")
    else:
        category = expense_category

amount = st.number_input("Amount", min_value=0.0, format="%.2f")
description = st.text_input("Description")
transaction_date = st.date_input("Date", value=date.today())

income_total = st.session_state.transactions[st.session_state.transactions["Type"] == "Income"]["Amount"].sum()
expense_total = st.session_state.transactions[st.session_state.transactions["Type"] == "Expense"]["Amount"].sum()
balance = income_total - expense_total

if st.button("Add Transaction"):
    if transaction_type == "Expense" and income_total == 0:
        st.error("Add income before recording an expense.")
    elif transaction_type == "Expense" and amount > balance:
        st.error("Insufficient balance. You cannot spend more than your available amount.")
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
        st.warning("Please fill in all fields correctly.")

st.header("Summary")

st.write(f"Total Income: ₹{income_total:.2f}")
st.write(f"Total Expenses: ₹{expense_total:.2f}")
st.write(f"Current Balance: ₹{balance:.2f}")

if not st.session_state.transactions.empty:
    st.header("Visual Analysis")

    if income_total + expense_total > 0:
        data_summary = pd.DataFrame({
            "Type": ["Income", "Expense"],
            "Amount": [income_total, expense_total]
        })
        fig1, ax1 = plt.subplots()
        ax1.pie(data_summary["Amount"], labels=data_summary["Type"], autopct="%1.1f%%", startangle=90)
        ax1.axis("equal")
        st.pyplot(fig1)
    else:
        st.info("Add some transactions to see the Expense vs Income chart.")

    expense_data = st.session_state.transactions[st.session_state.transactions["Type"] == "Expense"]
    if not expense_data.empty:
        fig2, ax2 = plt.subplots()
        ax2.bar(expense_data["Category"], expense_data["Amount"])
        ax2.set_xlabel("Expense Category")
        ax2.set_ylabel("Amount (₹)")
        ax2.set_title("Category-wise Expenses")
        st.pyplot(fig2)

st.header("Transaction History")
st.dataframe(st.session_state.transactions)
