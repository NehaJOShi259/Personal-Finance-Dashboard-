import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Personal Finance Tracker")

if "transactions" not in st.session_state:
    st.session_state.transactions = pd.DataFrame(columns=["Type", "Category", "Amount", "Description", "Date"])

transaction_type = st.selectbox("Transaction Type", ["Income", "Expense"])

if transaction_type == "Income":
    category = st.selectbox("Category", ["Salary", "Freelance", "Investment", "Other"])
else:
    category = st.selectbox("Category", ["Food", "Transport", "Bills", "Entertainment", "Other"])

amount = st.number_input("Amount", min_value=0.0, step=0.1)
description = st.text_input("Description")
date = st.date_input("Date")

if st.button("Add Transaction"):
    if transaction_type == "Expense":
        total_income = st.session_state.transactions[st.session_state.transactions["Type"] == "Income"]["Amount"].sum()
        total_expense = st.session_state.transactions[st.session_state.transactions["Type"] == "Expense"]["Amount"].sum()
        if total_income - total_expense < amount:
            st.warning("Insufficient balance. Add income first.")
        else:
            new_transaction = pd.DataFrame({
                "Type": [transaction_type],
                "Category": [category],
                "Amount": [amount],
                "Description": [description],
                "Date": [date]
            })
            st.session_state.transactions = pd.concat([st.session_state.transactions, new_transaction], ignore_index=True)
            st.success("Transaction added successfully.")
    else:
        new_transaction = pd.DataFrame({
            "Type": [transaction_type],
            "Category": [category],
            "Amount": [amount],
            "Description": [description],
            "Date": [date]
        })
        st.session_state.transactions = pd.concat([st.session_state.transactions, new_transaction], ignore_index=True)
        st.success("Transaction added successfully.")

st.subheader("All Transactions")
st.dataframe(st.session_state.transactions)

if not st.session_state.transactions.empty:
    delete_index = st.selectbox("Select transaction to delete", range(len(st.session_state.transactions)))
    if st.button("Delete Transaction"):
        st.session_state.transactions = st.session_state.transactions.drop(delete_index).reset_index(drop=True)
        st.success("Transaction deleted successfully.")

st.subheader("Summary")
if not st.session_state.transactions.empty:
    income = st.session_state.transactions[st.session_state.transactions["Type"] == "Income"]["Amount"].sum()
    expense = st.session_state.transactions[st.session_state.transactions["Type"] == "Expense"]["Amount"].sum()
    balance = income - expense
    st.write(f"Total Income: ₹{income}")
    st.write(f"Total Expense: ₹{expense}")
    st.write(f"Balance: ₹{balance}")

    st.subheader("Category-wise Expense Distribution")
    expense_data = st.session_state.transactions[st.session_state.transactions["Type"] == "Expense"]

    categories = ["Food", "Transport", "Bills", "Entertainment", "Other"]
    category_sums = {cat: 0 for cat in categories}
    for cat in expense_data["Category"].unique():
        category_sums[cat] = expense_data[expense_data["Category"] == cat]["Amount"].sum()

    fig1, ax1 = plt.subplots()
    ax1.pie(category_sums.values(), labels=category_sums.keys(), autopct="%1.1f%%")
    st.pyplot(fig1)

    st.subheader("Income vs Expense by Category")
    income_data = st.session_state.transactions[st.session_state.transactions["Type"] == "Income"]

    income_sums = {cat: 0 for cat in ["Salary", "Freelance", "Investment", "Other"]}
    for cat in income_data["Category"].unique():
        income_sums[cat] = income_data[income_data["Category"] == cat]["Amount"].sum()

    df_bar = pd.DataFrame({
        "Category": list(set(list(income_sums.keys()) + list(category_sums.keys()))),
        "Income": [income_sums.get(cat, 0) for cat in set(income_sums.keys()).union(category_sums.keys())],
        "Expense": [category_sums.get(cat, 0) for cat in set(income_sums.keys()).union(category_sums.keys())]
    })

    fig2, ax2 = plt.subplots()
    df_bar.plot(x="Category", kind="bar", ax=ax2)
    st.pyplot(fig2)
else:
    st.write("No transactions to display yet.")
