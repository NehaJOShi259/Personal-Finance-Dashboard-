# Personal Finance Tracker (Python Streamlit)

**Personal Finance Tracker** is a simple yet functional web app built using **Python** and **Streamlit**.
It helps you record, visualize, and manage your **income and expenses** effectively — all through an interactive web dashboard.



## 🌐 Live Demo

👉 [Open Personal Finance Tracker](https://nehajoshi259-personal-finance-dashboar-finance-dashboard-u2wtzy.streamlit.app/)



## Features

* Add transactions with **Date, Type (Income/Expense), Category, Amount, and Description**
* Prevent mismatched entries (e.g., “food” under salary)
* Stop spending if your balance is insufficient
* Automatically calculate:

  * **Total Income**
  * **Total Expenses**
  * **Remaining Balance**
* View and manage all transactions in one place
* Delete individual entries or clear all data
* Visualize:

  * **Category-wise Expense Distribution (Pie Chart)**
  * **Income vs Expense Comparison (Bar Chart)**
* All data is saved locally in a **CSV file** for persistence



## Technologies Used

* **Python 3.x**
* **Streamlit**
* **Pandas**
* **Matplotlib**



## How to Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/NehaJOShi259/Personal-Finance-Dashboard-.git
   cd Personal-Finance-Dashboard-
   ```

2. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   python -m streamlit run finance_dashboard.py
   ```

4. Open the link shown in your terminal (usually):

   ```
   http://localhost:8501
   ```



## App Logic Overview

* **Income Validation:** Prevents adding expenses before income.
* **Description Validation:** Detects mismatched words (e.g., “food” under income).
* **Balance Check:** Stops you from overspending beyond your current balance.
* **Visual Insights:**

  * Pie chart for category-wise spending distribution.
  * Bar chart comparing total income vs expenses.



## Example Usage

1. Add your **Salary** as income.
2. Record expenses like **Food**, **Bills**, or **Shopping**.
3. The app prevents overspending and mismatched entries.
4. View total balance, category spending, and bar/pie charts.
5. Manage entries easily with delete and clear options.
