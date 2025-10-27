import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

st.set_page_config(page_title="Personal Finance Dashboard", layout="wide")
st.title("Personal Finance Dashboard")

DATA_FILE = "transactions.csv"

# --- Load or initialize data ---
if os.path.exists(DATA_FILE):
    data = pd.read_csv(DATA_FILE, parse_dates=["Date"])
else:
    data = pd.DataFrame(columns=["Date", "Type", "Category", "Amount"])

# Ensure correct dtypes if file existed
if not data.empty:
    data["Date"] = pd.to_datetime(data["Date"])

# Store in session state
if "data" not in st.session_state:
    st.session_state.data = data

# --- Sidebar: Budget & Add Transaction ---
st.sidebar.header("Settings & Add Transaction")

# Monthly budget (apply per month-year)
monthly_budget = st.sidebar.number_input("Monthly Budget (₹)", min_value=0.0, step=100.0, value=0.0)

st.sidebar.markdown("---")
st.sidebar.subheader("Add Transaction")
transaction_type = st.sidebar.selectbox("Type", ["Income", "Expense"])

# Common categories for dropdown
common_categories = [
    "Salary", "Bonus", "Investment",
    "Rent", "Groceries", "Food", "Travel", "Utilities", "Shopping", "Health", "Education", "Other"
]

selected_category = st.sidebar.selectbox("Select Category", sorted(set(common_categories)))
custom_category = st.sidebar.text_input("Or enter a custom category (optional)")

# Choose final category: prefer custom if provided
category_input = custom_category.strip() if custom_category.strip() != "" else selected_category

amount = st.sidebar.number_input("Amount (₹)", min_value=0.0, step=0.01)
date = st.sidebar.date_input("Date", value=datetime.today())

# Optional: allow forcing an over-budget add
allow_force = st.sidebar.checkbox("Allow adding even if it exceeds monthly budget (force)", value=False)

def category_has_digit(cat: str) -> bool:
    return any(ch.isdigit() for ch in cat)

if st.sidebar.button("Add Transaction"):
    # Basic validations
    if category_input == "" or category_input is None:
        st.sidebar.error("Category is required. Select or type a category.")
    elif category_has_digit(category_input):
        st.sidebar.error("Category should not contain numbers. Please enter a valid category (letters and symbols allowed).")
    elif amount <= 0:
        st.sidebar.error("Amount must be greater than 0.")
    else:
        # Check budget (only relevant for Expense)
        new_date = pd.to_datetime(date)
        month = new_date.month
        year = new_date.year

        # compute current month expenses from existing data
        existing = st.session_state.data
        if not existing.empty:
            existing_dates = pd.to_datetime(existing["Date"])
            same_month_mask = (existing_dates.dt.month == month) & (existing_dates.dt.year == year) & (existing["Type"] == "Expense")
            current_month_expenses = existing.loc[same_month_mask, "Amount"].sum()
        else:
            current_month_expenses = 0.0

        will_total = current_month_expenses + (amount if transaction_type == "Expense" else 0.0)

        if monthly_budget > 0 and transaction_type == "Expense" and (will_total > monthly_budget) and (not allow_force):
            st.sidebar.error(
                f"Cannot add: this expense would exceed the monthly budget.\n"
                f"Budget: ₹{monthly_budget:,.2f} | Current month expenses: ₹{current_month_expenses:,.2f} | After add: ₹{will_total:,.2f}"
            )
        else:
            new_entry = {
                "Date": new_date,
                "Type": transaction_type,
                "Category": category_input,
                "Amount": amount,
            }
            st.session_state.data = pd.concat(
                [st.session_state.data, pd.DataFrame([new_entry])], ignore_index=True
            )
            st.session_state.data.to_csv(DATA_FILE, index=False)
            st.sidebar.success("Transaction added successfully!")
            st.experimental_rerun()

# --- Main Dashboard ---
data = st.session_state.data

if not data.empty:
    st.subheader("Transactions")

    # Show current month/year selection and remaining budget info
    col_a, col_b = st.columns([2, 1])
    with col_a:
        show_month = st.selectbox("View month", options=sorted(
            list({(d.month, d.year) for d in pd.to_datetime(data["Date"])}),
            key=lambda x: (x[1], x[0])
        ), format_func=lambda t: f"{t[0]:02d}-{t[1]}")
    with col_b:
        # compute for selected month-year
        sel_month, sel_year = show_month
        mask_sel = (pd.to_datetime(data["Date"]).dt.month == sel_month) & (pd.to_datetime(data["Date"]).dt.year == sel_year)
        expenses_sel = data.loc[mask_sel & (data["Type"] == "Expense"), "Amount"].sum()
        income_sel = data.loc[mask_sel & (data["Type"] == "Income"), "Amount"].sum()
        remaining = monthly_budget - expenses_sel if monthly_budget > 0 else None

        st.write(f"**Selected:** {sel_month:02d}-{sel_year}")
        st.write(f"Income: ₹{income_sel:,.2f}")
        st.write(f"Expenses: ₹{expenses_sel:,.2f}")
        if monthly_budget > 0:
            st.write(f"Budget: ₹{monthly_budget:,.2f}")
            st.write(f"Remaining: ₹{remaining:,.2f}")

    # Display rows with delete button next to each
    edited_data = data.sort_values(by="Date", ascending=False).reset_index(drop=True)
    for i, row in edited_data.iterrows():
        c1, c2, c3, c4, c5 = st.columns([2, 1, 2, 1, 1])
        c1.write(pd.to_datetime(row["Date"]).date())
        c2.write(row["Type"])
        c3.write(row["Category"])
        c4.write(f"₹{row['Amount']:,.2f}")
        if c5.button("Delete", key=f"del_{i}"):
            # delete by index in the dataframe stored (find actual index)
            actual_index = edited_data.index[i]
            st.session_state.data = st.session_state.data.drop(actual_index).reset_index(drop=True)
            st.session_state.data.to_csv(DATA_FILE, index=False)
            st.success("Transaction deleted.")
            st.experimental_rerun()

    # --- Summary overall ---
    st.subheader("Summary (All time)")
    total_income = data[data["Type"] == "Income"]["Amount"].sum()
    total_expense = data[data["Type"] == "Expense"]["Amount"].sum()
    balance = total_income - total_expense

    st.write(f"**Total Income:** ₹{total_income:,.2f}")
    st.write(f"**Total Expenses:** ₹{total_expense:,.2f}")
    st.write(f"**Balance:** ₹{balance:,.2f}")

    # --- Simple Expense Chart ---
    expenses = data[data["Type"] == "Expense"].groupby("Category")["Amount"].sum()
    if not expenses.empty:
        fig, ax = plt.subplots()
        expenses.plot(kind="bar", ax=ax)
        ax.set_ylabel("Amount (₹)")
        ax.set_title("Expenses by Category")
        st.pyplot(fig)
        plt.close(fig)

    # --- Download CSV ---
    st.download_button(
        label="Download Transactions CSV",
        data=data.to_csv(index=False).encode("utf-8"),
        file_name="transactions.csv",
        mime="text/csv",
    )

else:
    st.info("No transactions yet. Add some using the sidebar.")


