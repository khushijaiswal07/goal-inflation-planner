import streamlit as st
import matplotlib.pyplot as plt

st.title("🎯 Goal Inflation Adjusted Investment Planner (by Khushi)")

# User Inputs
goal = st.number_input("Enter your Goal Amount (₹):", min_value=1000, step=1000)
years = st.number_input("Enter time period (years):", min_value=1, step=1)
inflation = st.number_input("Enter expected inflation rate (%):", min_value=0.0, step=0.1)
returns = st.number_input("Enter expected return rate (%):", min_value=0.0, step=0.1)

if st.button("Calculate"):
    # Calculate
    inflated_goal = goal * ((1 + inflation/100) ** years)
    r = returns / 100 / 12
    n = years * 12
    sip = inflated_goal * r / (((1 + r)**n - 1) * (1 + r))
    
    st.success(f"🎯 Inflation Adjusted Goal Amount: ₹{inflated_goal:,.2f}")
    st.info(f"💰 Required Monthly SIP: ₹{sip:,.2f}")
    
    # Chart
    years_list = list(range(1, years + 1))
    goal_growth = [goal * ((1 + inflation/100)**i) for i in years_list]
    
    fig, ax = plt.subplots()
    ax.plot(years_list, goal_growth, label="Inflation Adjusted Goal", color='purple')
    ax.set_xlabel("Years")
    ax.set_ylabel("Amount (₹)")
    ax.set_title("Goal vs Inflation Over Time")
    ax.legend()
    st.pyplot(fig)
