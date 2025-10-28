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

if transaction_type == "Income" and category == "Salary":
    st.text("Description: Salary Income (auto-filled)")
    description = "Salary Income"
else:
    description = st.text_input("Description")

date = st.date_input("Date")

mismatch = False
if transaction_type == "Income" and any(word.lower() in description.lower() for word in ["food", "travel", "transport", "bill", "entertainment"]):
    mismatch = True
elif transaction_type == "Expense" and any(word.lower() in description.lower() for word in ["salary", "income", "freelance", "investment"]):
    mismatch = True

if st.button("Add Transaction"):
    if mismatch:
        st.error("Description does not match the selected transaction type or category.")
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

    if income > 0 or expense > 0:
        fig, ax = plt.subplots()
        ax.bar(["Income", "Expense"], [income, expense], color=["green", "red"])
        ax.set_title("Income vs Expense")
        ax.set_ylabel("Amount (₹)")
        for i, v in enumerate([income, expense]):
            ax.text(i, v + 10, f"₹{v}", ha="center", fontweight="bold")
        st.pyplot(fig)
else:
    st.write("No transactions to display yet.")
