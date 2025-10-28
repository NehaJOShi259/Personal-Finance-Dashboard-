# Personal Finance Tracker (Python Streamlit)

**Personal Finance Tracker** is a simple yet functional web app built using **Python** and **Streamlit**.
It allows users to record, visualize, and manage their income and expenses in a clean and efficient way.

---

## Features

* Add transactions with **Date, Type (Income/Expense), Category, Amount, and Description**
* Prevent invalid or mismatched entries (e.g., writing “food” under salary)
* Block expenses if balance is insufficient
* Automatically calculate **Total Income**, **Total Expenses**, and **Remaining Balance**
* View and manage transaction history
* Delete specific entries or clear all data
* Visualize:

  * **Category-wise Expense Distribution (Pie Chart)**
  * **Income vs Expense Comparison (Bar Chart)**
* Data persists using a local **CSV file**

---

## Technologies Used

* **Python 3.x**
* **Streamlit**
* **Pandas**
* **Matplotlib**

---

## How to Run Locally

1. Clone this repository:

   ```bash
   git clone https://github.com/NehaJOShi259/Personal-Finance-Dashboard-.git
   cd Personal-Finance-Dashboard-
   ```

2. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Run the Streamlit app:

   ```bash
   python -m streamlit run finance_dashboard.py
   ```

4. The dashboard will open automatically in your default browser:

   ```
   http://localhost:8501
   ```

---

## App Logic Overview

* **Income Validation:** Prevents adding expenses before adding income.
* **Description Validation:** Checks for mismatched keywords (e.g., “food” can’t appear in an income entry).
* **Balance Control:** Ensures no expense exceeds the available balance.
* **Visualization:**

  * Pie chart shows spending distribution by category.
  * Bar chart compares total income vs total expenses.

---

## Example Workflow

1. Add your **Salary** as income.
2. Record expenses like **Food**, **Transport**, or **Shopping**.
3. If you try to spend more than your available balance, the app alerts you.
4. View clear visuals and transaction history to understand your spending.

