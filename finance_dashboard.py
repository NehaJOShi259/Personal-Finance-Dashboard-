# finance_dashboard.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Personal Finance Dashboard", layout="wide")
st.title("💰 Personal Finance Dashboard")

DATA_FILE = "transactions.csv"

# --- Load existing data ---
if os.path.exists(DATA_FILE):
    data = pd.read_csv(DATA_FILE, parse_dates=["Date"])
else:
    data = pd.DataFrame(columns=["Date", "Type", "Category", "Amount"])

# Store in session state
if "data" not in st.session_state:
    st.session_state.data = data

# --- Sidebar for user input ---
st.sidebar.header("Add Transaction")
transaction_type = st.sidebar.selectbox("Transaction Type", ["Income", "Expense"])
category = st.sidebar.text_input("Category (e.g., Rent, Salary)")
amount = st.sidebar.number_input("Amount", min_value=0.0, step=0.01)
date = st.sidebar.date_input("Date")

# Add new transaction
if st.sidebar.button("Add Transaction"):
    new_entry = {"Date": pd.to_datetime(date), "Type": transaction_type, 
                 "Category": category, "Amount": amount}
    st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_entry])], ignore_index=True)
    st.session_state.data.to_csv(DATA_FILE, index=False)  # Save to CSV
    st.sidebar.success("Transaction added and saved!")

# --- Main dashboard ---
data = st.session_state.data

if not data.empty:
    # Transaction Table
    st.subheader("📊 Transaction Table")
    st.dataframe(data.sort_values(by="Date", ascending=False))

    # Summary Metrics
    st.subheader("💵 Summary")
    income_total = data.loc[data["Type"]=="Income", "Amount"].sum()
    expense_total = data.loc[data["Type"]=="Expense", "Amount"].sum()
    balance = income_total - expense_total

    st.metric("Total Income", f"${income_total:,.2f}")
    st.metric("Total Expenses", f"${expense_total:,.2f}")
    st.metric("Balance", f"${balance:,.2f}")

    # Expenses data for charts
    expenses = data[data["Type"]=="Expense"].groupby("Category")["Amount"].sum().sort_values(ascending=False)

    col1, col2 = st.columns(2)

    # Bar Chart
    with col1:
        st.subheader("Expenses by Category (Bar Chart)")
        if not expenses.empty:
            fig, ax = plt.subplots()
            expenses.plot(kind="bar", ax=ax, color='skyblue')
            ax.set_ylabel("Amount ($)")
            ax.set_title("Expenses by Category")
            st.pyplot(fig)
            plt.close(fig)

    # Pie Chart
    with col2:
        st.subheader("Expenses by Category (Pie Chart)")
        if not expenses.empty:
            fig2, ax2 = plt.subplots()
            ax2.pie(expenses, labels=expenses.index, autopct='%1.1f%%', startangle=90)
            ax2.set_title("Expense Distribution by Category")
            st.pyplot(fig2)
            plt.close(fig2)

    # Line Chart: Income vs Expenses over time
    st.subheader("💡 Income vs Expenses Over Time")
    timeline = data.groupby(["Date", "Type"])["Amount"].sum().unstack(fill_value=0)
    if not timeline.empty:
        st.line_chart(timeline)

    # Download CSV
    st.download_button(
        label="Download Transactions CSV",
        data=data.to_csv(index=False).encode('utf-8'),
        file_name='transactions.csv',
        mime='text/csv',
    )

else:
    st.info("No transactions yet. Add some using the sidebar!")
