import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Personal Finance Dashboard")

if "transactions" not in st.session_state:
    st.session_state.transactions = pd.DataFrame(columns=["Type", "Date", "Category", "Amount", "Description"])

with st.form("add_transaction"):
    st.subheader("Add Transaction")
    t_type = st.radio("Type", ["Income", "Expense"], horizontal=True)
    t_date = st.date_input("Date")
    t_category = st.text_input("Category (e.g. Food, Rent, Salary)")
    t_amount = st.number_input("Amount (₹)", min_value=0.0, step=0.01)
    t_desc = st.text_area("Description")
    submitted = st.form_submit_button("Add Transaction")

    if submitted:
        df = st.session_state.transactions
        total_income = df[df["Type"] == "Income"]["Amount"].sum()
        total_expense = df[df["Type"] == "Expense"]["Amount"].sum()
        remaining = total_income - total_expense

        if t_type == "Expense" and t_amount > remaining:
            st.error("Expense exceeds available balance. Please add income first.")
        else:
            new_row = pd.DataFrame([[t_type, t_date, t_category, t_amount, t_desc]],
                                   columns=df.columns)
            st.session_state.transactions = pd.concat([df, new_row], ignore_index=True)
            st.success("Transaction added!")

st.subheader("Transaction History")
st.dataframe(st.session_state.transactions, use_container_width=True)

df = st.session_state.transactions
total_income = df[df["Type"] == "Income"]["Amount"].sum()
total_expense = df[df["Type"] == "Expense"]["Amount"].sum()
remaining = total_income - total_expense

st.subheader("Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Income", f"₹{total_income:.2f}")
col2.metric("Total Expenses", f"₹{total_expense:.2f}")
col3.metric("Remaining Balance", f"₹{remaining:.2f}")

if not df.empty:
    st.subheader("Expense vs Income Chart")
    summary = df.groupby("Type")["Amount"].sum()
    fig, ax = plt.subplots()
    ax.bar(summary.index, summary.values, color=["green", "red"])
    ax.set_ylabel("Amount (₹)")
    st.pyplot(fig)
