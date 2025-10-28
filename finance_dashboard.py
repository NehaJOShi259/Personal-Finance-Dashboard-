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

amount = st.number_input("Amount (₹)", min_value=0.0, step=0.1)
description = st.text_input("Description")
date = st.date_input("Date")

# Strict mismatch detection based on category
mismatch = False
desc_lower = description.lower()

if transaction_type == "Income":
    if category == "Salary" and any(w in desc_lower for w in ["food", "travel", "bill", "movie", "entertainment"]):
        mismatch = True
    elif category == "Freelance" and any(w in desc_lower for w in ["food", "transport", "bill", "salary"]):
        mismatch = True
    elif category == "Investment" and any(w in desc_lower for w in ["food", "travel", "rent", "bill"]):
        mismatch = True
else:
    if category == "Food" and any(w in desc_lower for w in ["salary", "income", "investment"]):
        mismatch = True
    elif category == "Transport" and any(w in desc_lower for w in ["salary", "income", "investment", "food"]):
        mismatch = True
    elif category == "Bills" and any(w in desc_lower for w in ["salary", "income", "investment", "food", "transport"]):
        mismatch = True
    elif category == "Entertainment" and any(w in desc_lower for w in ["salary", "income", "investment", "food", "bill"]):
        mismatch = True

if st.button("Add Transaction"):
    if amount <= 0:
        st.warning("Enter a valid amount.")
    elif mismatch:
        st.error("Description does not match the selected category.")
    elif transaction_type == "Expense":
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

    # Pie chart for category-wise expenses only
    expense_data = st.session_state.transactions[st.session_state.transactions["Type"] == "Expense"]
    if not expense_data.empty:
        category_sums = expense_data.groupby("Category")["Amount"].sum()
        category_sums = category_sums[category_sums > 0]
        if not category_sums.empty:
            fig, ax = plt.subplots()
            ax.pie(category_sums, labels=category_sums.index, startangle=90)
            ax.set_title("Category-wise Expense Distribution")
            st.pyplot(fig)
    else:
        st.info("No expenses yet to display pie chart.")

    # Income vs Expense Bar chart
    fig2, ax2 = plt.subplots()
    ax2.bar(["Income", "Expense"], [income, expense], color=["green", "red"])
    ax2.set_title("Income vs Expense")
    ax2.set_ylabel("Amount (₹)")
    for i, v in enumerate([income, expense]):
        ax2.text(i, v + 10, f"₹{v}", ha="center", fontweight="bold")
    st.pyplot(fig2)
else:
    st.write("No transactions to display yet.")
