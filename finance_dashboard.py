import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# File to store data permanently
DATA_FILE = "finance_data.csv"

# Load existing data
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["Type", "Category", "Amount", "Description", "Date"])

st.title("💰 Income & Expense Tracker")

# Input section
st.subheader("Add Transaction")

type_option = st.selectbox("Type", ["Income", "Expense"])
category = st.text_input("Category")
amount = st.number_input("Amount", min_value=0.0, format="%.2f")
description = st.text_input("Description")
date = st.date_input("Date")

# Define mismatched keywords
mismatch_rules = {
    "Income": ["food", "bill", "travel", "transport"],
    "Expense": ["salary", "bonus", "income"]
}

# Function to check mismatches
def check_mismatch(type_option, description):
    desc_words = description.lower().split()
    for bad_word in mismatch_rules.get(type_option, []):
        if bad_word in desc_words:
            return True
    return False

# Add data
if st.button("Add"):
    if check_mismatch(type_option, description):
        st.error(f"⚠️ Mismatch detected! '{description}' doesn't fit with {type_option}.")
    else:
        new_entry = pd.DataFrame({
            "Type": [type_option],
            "Category": [category],
            "Amount": [amount],
            "Description": [description],
            "Date": [date]
        })
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("✅ Entry added successfully!")

# Show data
st.subheader("All Transactions")
st.dataframe(df)

# --- PIE CHART FOR CATEGORY-WISE EXPENSES ---
st.subheader("📊 Category-wise Expense Breakdown")

if not df.empty and "Expense" in df["Type"].values:
    expense_df = df[df["Type"] == "Expense"]
    if not expense_df.empty:
        category_sum = expense_df.groupby("Category")["Amount"].sum()
        fig, ax = plt.subplots()
        wedges, texts, autotexts = ax.pie(
            category_sum,
            labels=category_sum.index,
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontsize': 10}
        )
        plt.title("Expense Distribution by Category")
        st.pyplot(fig)
    else:
        st.info("No expenses recorded yet.")
else:
    st.info("No data available to display.")

# --- INCOME VS EXPENSE BAR CHART ---
st.subheader("💸 Income vs Expense Comparison")

if not df.empty:
    summary = df.groupby("Type")["Amount"].sum().reindex(["Income", "Expense"], fill_value=0)
    fig2, ax2 = plt.subplots()
    summary.plot(kind='bar', ax=ax2, color=['green', 'red'])
    plt.title("Income vs Expense")
    plt.xlabel("Type")
    plt.ylabel("Amount")
    for i, val in enumerate(summary):
        ax2.text(i, val + 5, f"{val:.0f}", ha='center')
    st.pyplot(fig2)
else:
    st.info("No transactions to show.")
