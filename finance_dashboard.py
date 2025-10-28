import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

if "transactions" not in st.session_state:
    st.session_state.transactions = pd.DataFrame(columns=["Type", "Category", "Amount", "Description", "Date"])

st.title("Personal Finance Tracker")

st.header("Add a Transaction")

transaction_type = st.selectbox("Select Transaction Type", ["Income", "Expense"])

income_categories = ["Salary", "Business", "Freelance", "Other"]
expense_categories = ["Food", "Rent", "Shopping", "Travel", "Bills", "Other"]

if transaction_type == "Income":
    category_choice = st.selectbox("Select Income Category", income_categories)
else:
    category_choice = st.selectbox("Select Expense Category", expense_categories)

if category_choice == "Other":
    category = st.text_input("Enter Custom Category")
else:
    category = category_choice

amount = st.number_input("Amount", min_value=0.0, format="%.2f")
description = st.text_input("Description")
transaction_date = st.date_input("Date", value=date.today())

income_total = st.session_state.transactions[st.session_state.transactions["Type"] == "Income"]["Amount"].sum()
expense_total = st.session_state.transactions[st.session_state.transactions["Type"] == "Expense"]["Amount"].sum()
balance = income_total - expense_total

if st.button("Add Transaction"):
    if transaction_type == "Expense" and income_total == 0:
        st.error("Please add income before recording any expense.")
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

    all_expense_categories = expense_categories.copy()
    expense_data = st.session_state.transactions[st.session_state.transactions["Type"] == "Expense"]
    expense_summary = expense_data.groupby("Category")["Amount"].sum().reindex(all_expense_categories, fill_value=0)

    fig2, ax2 = plt.subplots()
    ax2.bar(expense_summary.index, expense_summary.values)
    ax2.set_xlabel("Expense Category")
    ax2.set_ylabel("Amount (₹)")
    ax2.set_title("Category-wise Expenses (Including Zero Spending)")
    st.pyplot(fig2)

st.header("Transaction History")
st.dataframe(st.session_state.transactions)
