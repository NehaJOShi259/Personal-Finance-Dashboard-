import streamlit as st
import json
from datetime import date
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Personal Finance Dashboard", layout="wide")

DATA_FILE = "finance_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"budget": None, "transactions": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def compute_totals(transactions):
    income = sum(t["amount"] for t in transactions if t["type"] == "Income")
    expense = sum(t["amount"] for t in transactions if t["type"] == "Expense")
    return income, expense, income - expense

data = load_data()
if "pending" not in st.session_state:
    st.session_state.pending = None

st.title("Personal Finance Dashboard")

with st.sidebar:
    st.header("Budget Setup")
    if data.get("budget") is None:
        entered_budget = st.number_input("Set your monthly budget (₹)", min_value=0.0, step=500.0, format="%.2f")
        if st.button("Save Budget"):
            if entered_budget <= 0:
                st.error("Budget must be greater than zero.")
            else:
                data["budget"] = float(entered_budget)
                save_data(data)
                st.success("Budget saved successfully.")
                st.rerun()
    else:
        st.write(f"Current Budget: ₹{data['budget']:.2f}")
        if st.button("Change Budget"):
            data["budget"] = None
            save_data(data)
            st.rerun()

st.subheader("Add Transaction")

if data.get("budget") is None:
    st.markdown(
        """
        <div style="background-color:#ffdddd;padding:15px;border-radius:10px;border-left:6px solid red;">
        <strong>⚠️ Action Required:</strong> Please set your budget first from the sidebar to begin tracking your finances.
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    col1, col2 = st.columns([1, 1])
    with col1:
        t_type = st.selectbox("Type", ["Income", "Expense"])
    with col2:
        t_date = st.date_input("Date", value=date.today())

    if t_type == "Income":
        category = st.selectbox("Category", ["Salary", "Bonus", "Investment", "Gift", "Other"])
    else:
        category = st.selectbox("Category", ["Food", "Rent", "Shopping", "Travel", "Health", "Bills", "Entertainment", "Other"])

    other_cat = ""
    if category == "Other":
        other_cat = st.text_input("Specify category")

    amount = st.number_input("Amount (₹)", min_value=0.0, step=100.0, format="%.2f")
    description = st.text_area("Journal / Description")

    def detect_mismatch(cat, text):
        if not text:
            return False
        text_l = text.lower()
        keywords = {
            "Food": ["eat", "restaurant", "food", "meal", "coffee", "tea", "lunch", "dinner", "snack", "grocery"],
            "Shopping": ["shirt", "tshirt", "clothes", "dress", "shoe", "bag", "shopping", "purchase"],
            "Travel": ["taxi", "bus", "train", "flight", "ticket", "trip", "travel"],
            "Rent": ["rent", "apartment", "room", "house", "lease"],
            "Health": ["doctor", "medicine", "clinic", "hospital"],
            "Bills": ["electricity", "water", "internet", "phone", "bill"],
            "Entertainment": ["movie", "netflix", "game", "concert"],
            "Salary": ["salary", "pay", "payout"],
            "Investment": ["stock", "mutual", "investment", "dividend"],
            "Gift": ["gift", "present"],
        }
        cat_key = cat if cat != "Other" else None
        if cat_key and cat_key in keywords:
            key_list = keywords[cat_key]
            found_cat_kw = any(k in text_l for k in key_list)
            other_keywords = [k for klist in keywords.values() for k in klist if k not in key_list]
            found_other_kw = any(k in text_l for k in other_keywords)
            if found_other_kw and not found_cat_kw:
                return True
        return False

    if st.button("Add Transaction"):
        if amount <= 0:
            st.error("Amount must be greater than zero.")
        else:
            chosen_category = other_cat.strip() if other_cat else category
            income_total, expense_total, balance = compute_totals(data["transactions"])
            remaining = data["budget"] - expense_total

            if t_type == "Expense":
                if amount > remaining:
                    st.error("Expense exceeds your remaining budget. Please add income or lower the expense amount.")
                else:
                    mismatch = detect_mismatch(chosen_category, description)
                    transaction = {"date": str(t_date), "type": t_type, "category": chosen_category, "amount": float(amount), "description": description}
                    if mismatch:
                        st.warning("The description does not match the category. Please check.")
                    else:
                        data["transactions"].append(transaction)
                        save_data(data)
                        st.success("Transaction added successfully.")
                        st.rerun()
            else:
                transaction = {"date": str(t_date), "type": t_type, "category": chosen_category, "amount": float(amount), "description": description}
                mismatch = detect_mismatch(chosen_category, description)
                if mismatch:
                    st.warning("The description does not match the category. Please check.")
                else:
                    data["transactions"].append(transaction)
                    save_data(data)
                    st.success("Transaction added successfully.")
                    st.rerun()

st.header("Summary")
transactions = data.get("transactions", [])
income_total, expense_total, current_balance = compute_totals(transactions)

if data.get("budget") is not None:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"₹{income_total:,.2f}")
    col2.metric("Total Expenses", f"₹{expense_total:,.2f}")
    col3.metric("Remaining", f"₹{(data['budget'] - expense_total):,.2f}")

    used_percent = (expense_total / data["budget"]) * 100 if data["budget"] > 0 else 0
    if used_percent >= 100:
        st.error("Expenses have reached or exceeded your budget limit.")
    elif used_percent >= 80:
        st.warning("You have used over 80% of your budget — be cautious with further spending.")

st.header("Charts")
if transactions:
    df = pd.DataFrame(transactions)
    if not df.empty:
        type_sums = df.groupby("type")["amount"].sum().reindex(["Income", "Expense"], fill_value=0)
        fig1, ax1 = plt.subplots()
        ax1.bar(type_sums.index, type_sums.values, color=["green", "red"])
        ax1.set_title("Income vs Expense")
        ax1.set_ylabel("Amount (₹)")
        st.pyplot(fig1)

        expense_df = df[df["type"] == "Expense"]
        if not expense_df.empty:
            cat_sums = expense_df.groupby("category")["amount"].sum()
            fig2, ax2 = plt.subplots()
            ax2.pie(cat_sums, labels=cat_sums.index, autopct="%1.1f%%", startangle=90)
            ax2.set_title("Spending by Category")
            st.pyplot(fig2)
else:
    st.info("No transactions to display.")

st.header("Transaction History")
if transactions:
    df = pd.DataFrame(transactions)
    df_display = df.sort_values(by="date", ascending=False)
    st.dataframe(df_display.reset_index(drop=True))
    csv = df_display.to_csv(index=False)
    st.download_button("Download CSV", csv, "transactions.csv", "text/csv")
else:
    st.info("No transactions recorded yet.")
