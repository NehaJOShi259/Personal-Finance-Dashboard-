import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

st.set_page_config(page_title="Smart Budget Tracker", layout="wide")

DATA_FILE = "budget_data.csv"

def load_data():
    try:
        df = pd.read_csv(DATA_FILE, parse_dates=["Date"])
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=["Date", "Type", "Category", "Amount", "Description"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

st.title("Smart Budget Tracker")

if "data" not in st.session_state:
    st.session_state.data = load_data()

if "balance" not in st.session_state:
    st.session_state.balance = 0.0

st.sidebar.header("Add Transaction")
transaction_type = st.sidebar.radio("Type", ["Income", "Expense"])
transaction_date = st.sidebar.date_input("Date", value=date.today())
category = st.sidebar.selectbox(
    "Category",
    ["Salary", "Bonus", "Investment", "Food", "Rent", "Shopping", "Travel", "Health", "Bills", "Entertainment", "Other"]
)
amount = st.sidebar.number_input("Amount (₹)", min_value=0.0, step=100.0)
description = st.sidebar.text_input("Description")

if st.sidebar.button("Add Transaction"):
    if amount <= 0:
        st.sidebar.error("Please enter a valid amount.")
    else:
        if transaction_type == "Expense" and amount > st.session_state.balance:
            st.sidebar.error("Not enough balance! Add income first.")
        else:
            new_entry = pd.DataFrame(
                [[transaction_date, transaction_type, category, amount, description]],
                columns=["Date", "Type", "Category", "Amount", "Description"]
            )
            st.session_state.data = pd.concat([st.session_state.data, new_entry], ignore_index=True)
            save_data(st.session_state.data)

            if transaction_type == "Income":
                st.session_state.balance += amount
            else:
                st.session_state.balance -= amount

            st.sidebar.success("Transaction added successfully!")

st.subheader("Transaction History")

if not st.session_state.data.empty:
    st.dataframe(st.session_state.data.sort_values(by="Date", ascending=False), use_container_width=True)
else:
    st.info("No transactions yet.")

st.subheader("Summary")

total_income = st.session_state.data[st.session_state.data["Type"] == "Income"]["Amount"].sum()
total_expense = st.session_state.data[st.session_state.data["Type"] == "Expense"]["Amount"].sum()
remaining_balance = total_income - total_expense

col1, col2, col3 = st.columns(3)
col1.metric("Total Income", f"₹{total_income:,.2f}")
col2.metric("Total Expenses", f"₹{total_expense:,.2f}")
col3.metric("Remaining Balance", f"₹{remaining_balance:,.2f}")

if total_expense > total_income:
    st.error("You have overspent! Reduce your expenses.")
else:
    st.success("You are within your budget.")

if not st.session_state.data.empty:
    expense_data = st.session_state.data[st.session_state.data["Type"] == "Expense"]

    if not expense_data.empty:
        category_summary = expense_data.groupby("Category")["Amount"].sum().reset_index()
        pie_chart = px.pie(category_summary, names="Category", values="Amount", title="Expense Distribution by Category")
        st.plotly_chart(pie_chart, use_container_width=True)

    summary_df = pd.DataFrame({"Type": ["Income", "Expense"], "Amount": [total_income, total_expense]})
    bar_chart = px.bar(summary_df, x="Type", y="Amount", color="Type", title="Income vs Expense Comparison", text="Amount")
    st.plotly_chart(bar_chart, use_container_width=True)

st.download_button(
    label="Download Transactions as CSV",
    data=st.session_state.data.to_csv(index=False),
    file_name="budget_data.csv",
    mime="text/csv"
)
