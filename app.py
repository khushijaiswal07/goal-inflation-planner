import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd

st.set_page_config(page_title="Goal SIP Planner", page_icon="🎯", layout="wide")
st.title("🎯 Goal Inflation Adjusted SIP Planner (by Khushi)")
st.markdown("**💡 Tip:** Enter realistic values for better results")

# Inputs in two columns
col1, col2 = st.columns(2)

with col1:
    goal = st.number_input("Enter your Goal Amount (₹):", min_value=1000, value=1000000, step=1000)
    years = st.number_input("Enter time period (years):", min_value=1, value=10, step=1)

with col2:
    inflation = st.number_input("Expected annual inflation (%):", min_value=0.0, value=6.0, step=0.1)
    returns = st.number_input("Expected annual return (%):", min_value=0.0, value=12.0, step=0.1)

if st.button("Calculate"):
    # Calculate SIP
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

    # Graph using plotly
    months = np.arange(1, n+1)
    if r <= 0:
        corpus = sip * months
    else:
        corpus = sip * (((1 + r) ** months - 1) / r) * (1 + r)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months/12, y=corpus, mode='lines+markers', name='Corpus', line=dict(color='purple')))
    fig.add_trace(go.Scatter(x=[0, years], y=[inflated_goal, inflated_goal], mode='lines', name='Inflation Adjusted Goal', line=dict(dash='dash', color='orange')))
    fig.update_layout(title='Projected Corpus vs Goal', xaxis_title='Years', yaxis_title='Amount (₹)')
    st.plotly_chart(fig)

    # Download CSV
    df = pd.DataFrame({"Month": months, "Corpus": corpus})
    st.download_button("Download Results as CSV", df.to_csv(index=False), file_name="SIP_results.csv")
