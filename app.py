# ------------------------------------
# Page Configuration
# ------------------------------------

import streamlit as st
import pandas as pd

from styles import load_css

from charts import (
    show_category_chart,
    show_monthly_chart,
    show_pie_chart
)

from database import (
    add_expense,
    create_database,
    delete_expense,
    get_category_totals,
    get_expenses,
    get_monthly_spending,
    get_summary
)
from utils import (
    create_csv,
    expenses_to_dataframe,
    format_currency
)

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide"
)

create_database()

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:

    st.title("💰 Expense Tracker")

    st.caption(
        "Manage your personal finances with ease."
    )

    st.markdown("---")

    st.subheader("📋 Navigation")

    st.markdown("""
    - 📊 Dashboard
    - ➕ Add Expense
    - 📋 Expense History
    - 📈 Analytics
    """)

    st.markdown("---")

    st.success("🚀 Version 1.0")

    st.info(
        "Track your daily spending and visualize your financial habits."
    )
# -----------------------------
# Theme Styling
# -----------------------------

st.markdown(
    load_css(),
    unsafe_allow_html=True
)

# -----------------------------
# Main Title
# -----------------------------
st.title("💰 Personal Expense Dashboard")

st.caption(
    "Track expenses, monitor spending trends, and gain insights into your finances."
)

# ------------------------------------
# Dashboard Metrics
# ------------------------------------

total_expenses, total_spent, largest_expense, total_categories = get_summary()

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with col1:
   st.metric(
    "💰 Total Spending",
    format_currency(total_spent)
)

with col2:
    st.metric("🧾 Total Expenses", total_expenses)

with col3:
   st.metric(
    "🏆 Largest Expense",
    format_currency(largest_expense)
)

with col4:
    st.metric("📂 Categories", total_categories)

st.divider()

# ------------------------------------
# Add Expense
# ------------------------------------

st.markdown("## ➕ Add New Expense")

amount = st.number_input(
    "Amount (R)",
    min_value=0.0,
    step=1.0
)

category = st.selectbox(
    "Category",
    [
        "Food",
        "Transport",
        "Shopping",
        "Entertainment",
        "Bills",
        "Healthcare",
        "Education",
        "Other"
    ]
)

date = st.date_input("Date")

description = st.text_input("Description")

if st.button("💾 Save Expense"):
    add_expense(
        amount,
        category,
        date,
        description
    )

st.success("✅ Expense saved successfully!")
    
st.divider()

st.markdown("## 🔍 Filter Expenses")

filter_category = st.selectbox(
    "Select Category",
    [
        "All",
        "Food",
        "Transport",
        "Shopping",
        "Entertainment",
        "Bills",
        "Healthcare",
        "Education",
        "Other"
    ]
)

st.markdown("## 📅 Filter by Date Range")

col1, col2 = st.columns(2)

with col1:
    start_date = st.date_input("From")

with col2:
    end_date = st.date_input("To")

# ------------------------------------
# Expense History
# ------------------------------------

st.markdown("## 📋 Expense History")

expenses = get_expenses()

# Filter by category
if filter_category != "All":
    expenses = [
        expense for expense in expenses
        if expense[1] == filter_category
    ]

# ------------------------------------
# Filters
# ------------------------------------

expenses = [
    expense
    for expense in expenses
    if start_date <= pd.to_datetime(expense[2]).date() <= end_date
]

if expenses:

    df = expenses_to_dataframe(expenses)

    st.dataframe(
        df,
        use_container_width=True
    )

    csv = create_csv(df)

    st.download_button(
        label="📥 Download Expenses (CSV)",
        data=csv,
        file_name="expenses.csv",
        mime="text/csv"
    )

    st.markdown("## 🗑️ Delete an Expense")

    expense_options = {
        f"{i + 1}. R{expense[0]} | {expense[1]} | {expense[2]} | {expense[3]}": expense
        for i, expense in enumerate(expenses)
    }

    selected = st.selectbox(
        "Select an expense to delete",
        list(expense_options.keys())
    )

    expense_to_delete = expense_options[selected]

    if st.button("Delete Expense"):
        delete_expense(
            expense_to_delete[0],
            expense_to_delete[1],
            expense_to_delete[2],
            expense_to_delete[3]
        )

        st.success("✅ Expense deleted successfully!")
        st.rerun()

else:
    st.info("No expenses recorded yet.")
    
# ------------------------------------
# Spending by category chart
# ------------------------------------

st.markdown("## 📊 Spending by Category")

category_data = get_category_totals()

show_category_chart(category_data)

st.divider()

# ------------------------------------
# Expense Distribution
# ------------------------------------

st.markdown("## 🥧 Expense Distribution")

show_pie_chart(category_data)

st.divider()

# ------------------------------------
# Monthly Summary
# ------------------------------------

st.markdown("## 📅 Monthly Summary")

monthly_data = get_monthly_spending()

show_monthly_chart(monthly_data)