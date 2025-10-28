import streamlit as st
import pandas as pd

st.set_page_config(page_title="Personal Finance Dashboard", layout="wide")

st.title("Personal Finance Dashboard")

# Initialize state

if "transactions" not in st.session_state:
    st.session_state.transactions = pd.DataFrame(columns=["Type", "Category", "Amount", "Description", "Date"])
if "total_income" not in st.session_state:
    st.session_state.total_income = 0
if "total_expense" not in st.session_state:
    st.session_state.total_expense = 0

# Sidebar input

st.sidebar.header("Add Transaction")
transaction_type = st.sidebar.selectbox("Type", ["Income", "Expense"])

if transaction_type == "Income":
    income_category = st.sidebar.selectbox("Source", ["Salary", "Freelancing", "Investment", "Gift", "Other"])
if income_category == "Other":
    income_category = st.sidebar.text_input("Enter Income Source")
    amount = st.sidebar.number_input("Amount (₹)", min_value=0.0, step=100.0)
    desc = st.sidebar.text_area("Description")
    date = st.sidebar.date_input("Date")
if st.sidebar.button("Add Income"):
    if amount > 0:
        new_data = pd.DataFrame([[transaction_type, income_category, amount, desc, date]],
                                columns=["Type", "Category", "Amount", "Description", "Date"])
        st.session_state.transactions = pd.concat([st.session_state.transactions, new_data], ignore_index=True)
        st.session_state.total_income += amount
        st.success("Income added successfully.")
    else:
        st.warning("Amount must be greater than zero.")


else:
expense_category = st.sidebar.selectbox("Category", ["Food", "Transport", "Rent", "Shopping", "Bills", "Entertainment", "Other"])
if expense_category == "Other":
    expense_category = st.sidebar.text_input("Enter Expense Category")
    amount = st.sidebar.number_input("Amount (₹)", min_value=0.0, step=100.0)
    desc = st.sidebar.text_area("Description")
    date = st.sidebar.date_input("Date")

remaining_balance = st.session_state.total_income - st.session_state.total_expense

if st.sidebar.button("Add Expense"):
    if amount <= 0:
        st.warning("Amount must be greater than zero.")
    elif remaining_balance < amount:
        st.error("Insufficient balance. Please add more income first.")
    else:
        new_data = pd.DataFrame([[transaction_type, expense_category, amount, desc, date]],
                                columns=["Type", "Category", "Amount", "Description", "Date"])
        st.session_state.transactions = pd.concat([st.session_state.transactions, new_data], ignore_index=True)
        st.session_state.total_expense += amount
        st.success("Expense added successfully.")


# Transaction table

st.header("Transaction History")
st.dataframe(st.session_state.transactions, use_container_width=True)

# Summary metrics

st.header("Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Income", f"₹{st.session_state.total_income:,.2f}")
col2.metric("Total Expenses", f"₹{st.session_state.total_expense:,.2f}")
col3.metric("Remaining Balance", f"₹{st.session_state.total_income - st.session_state.total_expense:,.2f}")





