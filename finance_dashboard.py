import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

st.set_page_config(page_title="Personal Finance Dashboard", layout="wide")

DATA_FILE = "finance_data.csv"

def load_data():
    try:
        df = pd.read_csv(DATA_FILE, parse_dates=["Date"])
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=["Date", "Type", "Category", "Amount", "Description"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

if "data" not in st.session_state:
    st.session_state.data = load_data()

st.title("Personal Finance Dashboard")

st.header("Add Transaction")
col1, col2, col3 = st.columns(3)
with col1:
    t_type = st.radio("Type", ["Income", "Expense"], horizontal=True)
with col2:
    t_date = st.date_input("Date", value=date.today())
with col3:
    category = st.text_input("Category (e.g. Salary, Rent, Food)")

amount = st.number_input("Amount (₹)", min_value=0.0, step=100.0)
description = st.text_area("Description (optional)")

if st.button("Add Transaction"):
    total_income = st.session_state.data[st.session_state.data["Type"] == "Income"]["Amount"].sum()
    total_expense = st.session_state.data[st.session_state.data["Type"] == "Expense"]["Amount"].sum()
    balance = total_income - total_expense

    if t_type == "Expense" and amount > balance:
        st.error("Expense exceeds available balance. Please add income first.")
    elif amount <= 0 or category.strip() == "":
        st.warning("Please enter valid details.")
    else:
        new_entry = pd.DataFrame(
            [[t_date, t_type, category, amount, description]],
            columns=["Date", "Type", "Category", "Amount", "Description"]
        )
        st.session_state.data = pd.concat([st.session_state.data, new_entry], ignore_index=True)
        save_data(st.session_state.data)
        st.success("Transaction added successfully!")

st.header("Summary")
col1, col2, col3 = st.columns(3)
total_income = st.session_state.data[st.session_state.data["Type"] == "Income"]["Amount"].sum()
total_expense = st.session_state.data[st.session_state.data["Type"] == "Expense"]["Amount"].sum()
balance = total_income - total_expense

col1.metric("Total Income", f"₹{total_income:,.2f}")
col2.metric("Total Expenses", f"₹{total_expense:,.2f}")
col3.metric("Remaining Balance", f"₹{balance:,.2f}")

st.header("Expense vs Income Chart")

if not st.session_state.data.empty:
    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots()
        chart_data = st.session_state.data.groupby("Type")["Amount"].sum()
        ax.bar(chart_data.index, chart_data.values, color=["green", "red"])
        ax.set_title("Income vs Expense")
        ax.set_ylabel("Amount (₹)")
        st.pyplot(fig)

    with col2:
        expense_data = st.session_state.data[st.session_state.data["Type"] == "Expense"]
        if not expense_data.empty:
            fig2, ax2 = plt.subplots()
            category_data = expense_data.groupby("Category")["Amount"].sum()
            ax2.pie(category_data, labels=category_data.index, autopct="%1.1f%%", startangle=90)
            ax2.set_title("Spending by Category")
            st.pyplot(fig2)
        else:
            st.info("No expenses to display in pie chart.")
else:
    st.info("No transactions recorded yet.")

st.header("Transaction History")
if not st.session_state.data.empty:
    st.dataframe(st.session_state.data.sort_values(by="Date", ascending=False), use_container_width=True)
else:
    st.info("No transactions available.")

st.download_button(
    label="Download All Transactions (CSV)",
    data=st.session_state.data.to_csv(index=False),
    file_name="finance_data.csv",
    mime="text/csv"
)
