import streamlit as st
import pandas as pd
from datetime import datetime

# -----------------------------
# Configuration
# -----------------------------
st.set_page_config(page_title="Expense Tracker", layout="wide")

DATA_FILE = "expense_data.csv"

# -----------------------------
# Data helpers
# -----------------------------

def load_data():
    try:
        df = pd.read_csv(DATA_FILE, parse_dates=["Date"])
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=["Date", "Category", "Amount", "Description"]) 


def save_data(df):
    df.to_csv(DATA_FILE, index=False)


# -----------------------------
# Initialize
# -----------------------------
st.title("Personal Expense Tracker")

if "data" not in st.session_state:
    st.session_state.data = load_data()

# -----------------------------
# Sidebar: Inputs & Budget
# -----------------------------
st.sidebar.header("Add Expense")

transaction_date = st.sidebar.date_input("Date", value=datetime.today())

default_categories = [
    "Food", "Travel", "Shopping", "Health", "Bills", "Entertainment", "Other"
]

selected_category = st.sidebar.selectbox("Category", default_categories)
custom_category = st.sidebar.text_input("Or enter custom category (no numbers)")

# choose category: prefer custom if provided
category = custom_category.strip() if custom_category.strip() != "" else selected_category

amount = st.sidebar.number_input("Amount (₹)", min_value=0.0, step=0.01)
description = st.sidebar.text_input("Description (optional)")

monthly_budget = st.sidebar.number_input("Total Budget (₹)", min_value=0.0, step=100.0, value=0.0)

allow_force = st.sidebar.checkbox("Allow adding if it exceeds budget", value=False)


# Validation helpers
ndef is_valid_category(cat: str) -> bool:
    if not cat:
        return False
    return not any(ch.isdigit() for ch in cat)


if st.sidebar.button("Add Expense"):
    # Basic validation
    if amount <= 0:
        st.sidebar.error("Amount must be greater than 0.")
    elif not is_valid_category(category):
        st.sidebar.error("Category invalid — do not include numbers.")
    else:
        # Budget check
        data = st.session_state.data
        if data.empty:
            current_spent = 0.0
        else:
            current_spent = data["Amount"].sum()

        projected = current_spent + amount

        if monthly_budget > 0 and projected > monthly_budget and not allow_force:
            st.sidebar.error(
                f"Cannot add: budget exceeded. Budget: ₹{monthly_budget:,.2f} | Current: ₹{current_spent:,.2f} | After add: ₹{projected:,.2f}"
            )
        else:
            new_row = {"Date": pd.to_datetime(transaction_date), "Category": category, "Amount": float(amount), "Description": description}
            st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_row])], ignore_index=True)
            save_data(st.session_state.data)
            st.sidebar.success("Expense added.")
            st.experimental_rerun()


# -----------------------------
# Main layout: Summary + Table + Chart
# -----------------------------

st.header("Summary")

data = st.session_state.data

if data.empty:
    st.info("No expenses yet. Add an expense from the left.")
else:
    total_spent = data["Amount"].sum()
    remaining = monthly_budget - total_spent if monthly_budget > 0 else None

    col1, col2, col3 = st.columns([1, 1, 1])
    col1.metric("Total Spent", f"₹{total_spent:,.2f}")
    if monthly_budget > 0:
        col2.metric("Budget", f"₹{monthly_budget:,.2f}")
        col3.metric("Remaining", f"₹{remaining:,.2f}")
    else:
        col2.write("")
        col3.write("")

    # Visual: spent vs remaining
    if monthly_budget > 0:
        chart_df = pd.DataFrame({"Amount": [total_spent, max(0, remaining)]}, index=["Spent", "Remaining"])
        st.bar_chart(chart_df)

    st.markdown("---")
    st.subheader("Expenses")

    # Show table with delete button next to each row
    df_display = data.copy().reset_index(drop=True)
    for idx, row in df_display.iterrows():
        c_date, c_cat, c_amt, c_desc, c_del = st.columns([2, 2, 1, 3, 0.7])
        c_date.write(pd.to_datetime(row["Date"]).date())
        c_cat.write(row["Category"])
        c_amt.write(f"₹{row['Amount']:,.2f}")
        c_desc.write(row["Description"] if row["Description"] else "-")

        if c_del.button("Delete", key=f"del_{idx}"):
            # remove the exact matching row by index in the stored dataframe
            actual_idx = df_display.index[idx]
            st.session_state.data = data.drop(actual_idx).reset_index(drop=True)
            save_data(st.session_state.data)
            st.experimental_rerun()

# Download option
st.download_button("Download CSV", data=st.session_state.data.to_csv(index=False), file_name="expenses.csv", mime="text/csv")
