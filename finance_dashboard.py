import streamlit as st
import pandas as pd

DATA_FILE = "expense_data.csv"

def load_data():
    try:
        return pd.read_csv(DATA_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

st.title("Personal Expense Tracker")

if "data" not in st.session_state:
    st.session_state.data = load_data()

st.header("Add New Expense")

with st.form("expense_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    date = col1.date_input("Date")
    category = col2.selectbox("Category", ["Food", "Travel", "Shopping", "Health", "Bills", "Entertainment", "Other"])
    amount = col3.number_input("Amount (₹)", min_value=0.0, step=1.0)
    description = st.text_input("Description")

    submitted = st.form_submit_button("Add Expense")

    if submitted:
        if amount <= 0 or not category:
            st.error("Please enter valid data before submitting.")
        else:
            new_entry = pd.DataFrame([[date, category, amount, description]], columns=st.session_state.data.columns)
            st.session_state.data = pd.concat([st.session_state.data, new_entry], ignore_index=True)
            save_data(st.session_state.data)
            st.success("Expense added successfully.")

st.header("Expense List")

if not st.session_state.data.empty:
    for i, row in st.session_state.data.iterrows():
        with st.container():
            cols = st.columns([1, 1, 1, 2, 0.5])
            cols[0].write(row["Date"])
            cols[1].write(row["Category"])
            cols[2].write(f"₹{row['Amount']}")
            cols[3].write(row["Description"] if row["Description"] else "-")
            if cols[4].button("Delete", key=f"del_{i}"):
                st.session_state.data.drop(i, inplace=True)
                st.session_state.data.reset_index(drop=True, inplace=True)
                save_data(st.session_state.data)
                st.rerun()
else:
    st.info("No expenses recorded yet.")

st.header("Budget Summary")
budget = st.number_input("Enter your total budget (₹)", min_value=0.0, step=500.0)

if not st.session_state.data.empty and budget > 0:
    total_spent = st.session_state.data["Amount"].sum()
    balance = budget - total_spent

    st.write(f"Total Spent: ₹{total_spent:.2f}")
    st.write(f"Remaining Balance: ₹{balance:.2f}")

    if total_spent > budget:
        st.error("Budget exceeded. Control your spending.")
    else:
        st.success("Within budget.")

    st.bar_chart(pd.DataFrame({"Spent": [total_spent], "Remaining": [balance]}).T)

st.download_button("Download Data as CSV", data=st.session_state.data.to_csv(index=False), file_name="expenses.csv", mime="text/csv")
