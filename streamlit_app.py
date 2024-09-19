import math
import numpy as np
import streamlit as st
from streamlit_echarts import st_echarts

st.set_page_config(page_title="Personal Budget App", layout="wide")

st.title("Personal Budget App")
monthly_income = st.text_input("Input your monthly income: ")

# Initialize an empty list to store expenses
if "expenses" not in st.session_state:
    st.session_state.expenses = []

# Create an expander for adding expenses
with st.expander("Add an expense"):
    expense_name = st.text_input("Expense name")
    expense_amount = st.number_input(
        "Expense amount per month: ", min_value=0.0, step=0.01
    )

    if st.button("Add expense"):
        if expense_name and expense_amount > 0:
            st.session_state.expenses.append(
                {"name": expense_name, "amount": expense_amount}
            )
            st.success(f"Added expense: {expense_name} - ${expense_amount:.2f}")
        else:
            st.warning("Please enter both expense name and a valid amount.")

calculate_budget_button = st.button("Calculate Budget")

if calculate_budget_button:
    # Convert monthly income to float
    try:
        income = float(monthly_income)
    except ValueError:
        st.error("Please enter a valid monthly income.")
        st.stop()

    # Calculate the total expenses
    total_expenses = sum(expense["amount"] for expense in st.session_state.expenses)

    # Display income and expenses
    st.subheader("Budget Summary")
    st.write(f"Monthly Income: ${income:.2f}")

    # Create a pie chart using streamlit_echarts
    options = {
        "title": {"text": "Expense Breakdown", "left": "left"},
        "tooltip": {"trigger": "item"},
        "legend": {"orient": "vertical", "right": "right"},
        "series": [
            {
                "name": "Expenses",
                "type": "pie",
                "radius": "50%",
                "data": [
                    {"value": expense["amount"], "name": expense["name"]}
                    for expense in st.session_state.expenses
                ],
                "emphasis": {
                    "itemStyle": {
                        "shadowBlur": 10,
                        "shadowOffsetX": 0,
                        "shadowColor": "rgba(0, 0, 0, 0.5)",
                    }
                },
            }
        ],
    }
    st_echarts(options=options, height="400px", width="400px")

    st.write(f"Total Expenses: ${total_expenses:.2f}")

    # Perform calculations
    balance = income - total_expenses
    savings_rate = (balance / income) * 100 if income > 0 else 0

    st.write(f"Remaining Balance: ${balance:.2f}")
    st.write(f"Savings Rate: {savings_rate:.2f}%")

    # Additional insights
    if balance > 0:
        st.success("You're within budget! Great job managing your finances.")
    elif balance == 0:
        st.warning("You've broken even. Consider finding ways to increase savings.")
    else:
        st.error("You're over budget. Try to reduce expenses or increase income.")
