import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

DATA_FILE = "finance_data.csv"

if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["Type", "Category", "Amount", "Description", "Date"])

st.title("Income and Expense Tracker")

income_categories = ["Salary", "Bonus", "Investment", "Other"]
expense_categories = ["Food", "Transport", "Bills", "Entertainment", "Shopping", "Other"]

st.subheader("Add New Transaction")

type_option = st.selectbox("Type", ["Income", "Expense"])
if type_option == "Income":
    category = st.selectbox("Category", income_categories)
else:
    category = st.selectbox("Category", expense_categories)

amount = st.number_input("Amount", min_value=0.0, format="%.2f")
description = st.text_input("Description")
date = st.date_input("Date")

income_related_words = ["salary", "bonus", "pay", "investment", "profit", "interest", "income"]
expense_related_words = ["food", "bill", "travel", "transport", "rent", "shopping", "grocery", "movie", "fun"]

def check_mismatch(type_option, description):
    desc = description.lower()
    if type_option == "Income":
        for word in expense_related_words:
            if word in desc:
                return True
    elif type_option == "Expense":
        for word in income_related_words:
            if word in desc:
                return True
    return False

if st.button("Add"):
    if amount <= 0:
        st.error("Amount must be greater than zero.")
    elif check_mismatch(type_option, description):
        st.error(f"'{description}' does not match with {type_option}. Please correct it.")
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
        st.success("Entry added successfully.")

st.subheader("All Transactions")
st.dataframe(df)

delete_index = st.number_input("Enter row number to delete", min_value=0, step=1, format="%d")
if st.button("Delete Entry"):
    if 0 <= delete_index < len(df):
        df = df.drop(delete_index).reset_index(drop=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Entry deleted.")
    else:
        st.error("Invalid row number.")

if st.button("Clear All Data"):
    df = pd.DataFrame(columns=["Type", "Category", "Amount", "Description", "Date"])
    df.to_csv(DATA_FILE, index=False)
    st.success("All data cleared.")

st.subheader("Category-wise Expense Breakdown")
if not df.empty:
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
        st.info("No expenses recorded.")
else:
    st.info("No data available.")

st.subheader("Income vs Expense Comparison")
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
