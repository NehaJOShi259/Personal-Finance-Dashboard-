import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Simple Budget Tracker", layout="wide")

DATA_FILE = "budget_data.csv"

# Load or create data
def load_data():
    try:
        return pd.read_csv(DATA_FILE, parse_dates=["Date"])
    except FileNotFoundError:
        return pd.DataFrame(columns=["Date", "Type", "Category", "Amount", "Description"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# Load session data
if "data" not in st.session_state:
    st.session_state.data = load_data()

st.title("💰 Simple Budget Tracker")

# --- Sidebar Input ---
st.sidebar.header("Add Transaction")

t_type = st.sidebar.radio("Type", ["Income", "Expense"])
t_date = st.sidebar.date_input("Date", value=date.today())
t_category = st.sidebar.text_input("Category (e.g. Food, Rent, Salary)")
t_amount = st.sidebar.number_input("Amount (₹)", min_value=0.0, step=100.0)
t_desc = st.sidebar.text_input("Description")

if st.sidebar.button("Add"):
    if t_amount <= 0:
        st.sidebar.error("Enter a valid amount.")
    else:
        new = pd.DataFrame([[t_date, t_type, t_category, t_amount, t_desc]],
                           columns=["Date", "Type", "Category", "Amount", "Description"])
        st.session_state.data = pd.concat([st.session_state.data, new], ignore_index=True)
        save_data(st.session_state.data)
        st.sidebar.success("Transaction added!")

# --- Main Page ---
st.subheader("Transaction History")

if not st.session_state.data.empty:
    st.dataframe(st.session_state.data.sort_values(by="Date", ascending=False), use_container_width=True)
else:
    st.info("No transactions yet.")

# --- Summary ---
st.subheader("Summary")
income = st.session_state.data[st.session_state.data["Type"] == "Income"]["Amount"].sum()
expense = st.session_state.data[st.session_state.data["Type"] == "Expense"]["Amount"].sum()
balance = income - expense

col1, col2, col3 = st.columns(3)
col1.metric("Total Income", f"₹{income:,.2f}")
col2.metric("Total Expenses", f"₹{expense:,.2f}")
col3.metric("Remaining Balance", f"₹{balance:,.2f}")

# --- Download ---
if not st.session_state.data.empty:
    st.download_button(
        label="Download Data as CSV",
        data=st.session_state.data.to_csv(index=False),
        file_name="budget_data.csv",
        mime="text/csv"
    )
