import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Goal Inflation SIP Planner", page_icon="🎯")
st.title("🎯 Goal-Inflation Adjusted SIP Planner (by Khushi Jaiswal)")

goal = st.number_input("Enter your Goal Amount (₹):", min_value=1000, value=1000000, step=1000)
years = st.number_input("Enter time period (years):", min_value=1, value=10, step=1)
inflation = st.number_input("Expected annual inflation (%):", min_value=0.0, value=6.0, step=0.1)
returns = st.number_input("Expected annual return (%):", min_value=0.0, value=12.0, step=0.1)

if st.button("Calculate"):
    inflated_goal = goal * ((1 + inflation/100) ** years)
    r = returns / 100 / 12
    n = years * 12
    if r <= 0:
        sip = inflated_goal / n
    else:
        sip = inflated_goal * r / (((1 + r)**n - 1) * (1 + r))

    st.subheader("Results")
    st.write(f"• Inflation adjusted goal after {years} years: **₹{inflated_goal:,.2f}**")
    st.write(f"• Required monthly SIP (approx): **₹{sip:,.2f}**")
    st.write(f"• Total invested over {years} years: **₹{sip * n:,.0f}**")

    months = np.arange(1, n + 1)
    if r <= 0:
        corpus = sip * months
    else:
        corpus = sip * (((1 + r) ** months - 1) / r) * (1 + r)

    fig, ax = plt.subplots()
    ax.plot(months/12, corpus, label="Corpus (₹)", linewidth=2)
    ax.axhline(inflated_goal, color='orange', linestyle='--', label='Inflation Adjusted Goal')
    ax.set_xlabel("Years")
    ax.set_ylabel("Amount (₹)")
    ax.set_title("Projected Corpus vs Goal")
    ax.legend()
    st.pyplot(fig)
