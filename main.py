import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime


def main():
    

    # ----------------------------
    # 1. Sample decision data set
    # ----------------------------

    data = pd.DataFrame([
        {
            "ID": "D001",
            "Owner": "Maria G.",
            "Team": "Call Center",
            "Decision Date": "2025-07-01",
            "Outcome Date": "2025-07-05",
            "Goal": "Lower ASA",
            "What Was Tried": "Realigned shift start times",
            "Inputs Used": "Call volume trend, shift overlap data",
            "Result": "ASA dropped from 42s to 28s",
            "Effectiveness": "✅ Effective",
            "Repeatable Win": True,
            "STAR Decision": True
        },
        {
            "ID": "D002",
            "Owner": "James K.",
            "Team": "Referral",
            "Decision Date": "2025-07-03",
            "Outcome Date": "2025-07-10",
            "Goal": "Faster Scheduling",
            "What Was Tried": "Removed manual form review",
            "Inputs Used": "Referral approval logs",
            "Result": "Scheduling improved by 2 days",
            "Effectiveness": "⚠️ Somewhat Effective",
            "Repeatable Win": False,
            "STAR Decision": False
        },
        {
            "ID": "D003",
            "Owner": "Linda T.",
            "Team": "Billing",
            "Decision Date": "2025-07-05",
            "Outcome Date": "2025-07-17",
            "Goal": "Lower AR Days",
            "What Was Tried": "Added denial triage in backlog",
            "Inputs Used": "Anecdotal staff complaints",
            "Result": "No measurable impact yet",
            "Effectiveness": "❌ Not Effective",
            "Repeatable Win": False,
            "STAR Decision": False
        },
        {
            "ID": "D004",
            "Owner": "Carlos V.",
            "Team": "QA",
            "Decision Date": "2025-07-06",
            "Outcome Date": "2025-07-11",
            "Goal": "Improve Patient Experience",
            "What Was Tried": "Call empathy scripts",
            "Inputs Used": "Patient survey comments",
            "Result": "Survey scores improved",
            "Effectiveness": "✅ Effective",
            "Repeatable Win": True,
            "STAR Decision": True
        },
        {
            "ID": "D005",
            "Owner": "Maria G.",
            "Team": "Call Center",
            "Decision Date": "2025-07-08",
            "Outcome Date": "2025-07-10",
            "Goal": "Reduce Call Transfers",
            "What Was Tried": "Expanded self-service tree",
            "Inputs Used": "Top 10 call reasons analysis",
            "Result": "Transfers down 12%",
            "Effectiveness": "✅ Effective",
            "Repeatable Win": True,
            "STAR Decision": False
        }
    ])

    # ----------------------------
    # 2. Categorize input sources
    # ----------------------------

    def categorize_input(input_text):
        if any(x in input_text.lower() for x in ["trend", "analysis", "logs"]):
            return "📊 Data Analysis"
        elif any(x in input_text.lower() for x in ["survey", "comment", "complaint"]):
            return "🗣️ Feedback"
        else:
            return "🔍 Observation"

    data["Input Type"] = data["Inputs Used"].apply(categorize_input)
    data["Decision Date"] = pd.to_datetime(data["Decision Date"])
    data["Outcome Date"] = pd.to_datetime(data["Outcome Date"])
    data["Time to Outcome (days)"] = (data["Outcome Date"] - data["Decision Date"]).dt.days

    # ----------------------------
    # 3. Layout
    # ----------------------------

    st.set_page_config(page_title="Decision Intelligence Dashboard", layout="wide")
    st.title("Decision Intelligence Dashboard")
    st.caption("Are we making the right decisions, fast enough, with the right inputs?")

    # ----------------------------
    # 4. Summary Metrics
    # ----------------------------

    st.subheader("📊 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Decisions", len(data))
    col2.metric("Avg Time to Outcome", f"{data['Time to Outcome (days)'].mean():.1f} days")
    col3.metric("Effective Rate", f"{(data['Effectiveness'] == '✅ Effective').mean() * 100:.0f}%")
    col4.metric("Repeatable Wins", f"{data['Repeatable Win'].sum()} ⭐")

    # ----------------------------
    # 5. Filter Controls
    # ----------------------------

    with st.expander("🔍 Filter by Owner, Team, or Effectiveness"):
        f_owner = st.multiselect("Owner", data["Owner"].unique())
        f_team = st.multiselect("Team", data["Team"].unique())
        f_effect = st.multiselect("Effectiveness", data["Effectiveness"].unique())
        filtered = data.copy()
        if f_owner:
            filtered = filtered[filtered["Owner"].isin(f_owner)]
        if f_team:
            filtered = filtered[filtered["Team"].isin(f_team)]
        if f_effect:
            filtered = filtered[filtered["Effectiveness"].isin(f_effect)]

    # ----------------------------
    # 6. STAR Decision Highlight
    # ----------------------------

    st.subheader("🌟 STAR Decisions (High Impact)")
    st.dataframe(filtered[filtered["STAR Decision"]].reset_index(drop=True), use_container_width=True)

    # ----------------------------
    # 7. Full Decision Log
    # ----------------------------

    st.subheader("📋 All Decisions Logged")
    st.dataframe(filtered.reset_index(drop=True), use_container_width=True)

    # ----------------------------
    # 8. Effectiveness Chart
    # ----------------------------

    effectiveness_summary = filtered["Effectiveness"].value_counts().reset_index()
    effectiveness_summary.columns = ["Effectiveness", "Count"]
    fig1 = px.bar(effectiveness_summary, x="Effectiveness", y="Count", color="Effectiveness",
                color_discrete_map={"✅ Effective": "green", "⚠️ Somewhat Effective": "orange", "❌ Not Effective": "red"},
                title="Overall Decision Outcomes", text="Count")
    st.plotly_chart(fig1, use_container_width=True)

    # ----------------------------
    # 9. Time to Outcome Scatter
    # ----------------------------

    st.subheader("⏱ Time to Impact by Owner")
    fig2 = px.scatter(
        filtered,
        x="Owner",
        y="Time to Outcome (days)",
        color="Effectiveness",
        hover_data=["Goal", "Inputs Used", "Result"],
        title="Decision Speed vs Quality",
        color_discrete_map={"✅ Effective": "green", "⚠️ Somewhat Effective": "orange", "❌ Not Effective": "red"}
    )
    st.plotly_chart(fig2, use_container_width=True)

    # ----------------------------
    # 10. Input Type Frequency (with Inputs)
    # ----------------------------

    st.subheader("🧾 What Inputs Were Used and How Often")
    inputs_used = (
        filtered.groupby(["Input Type", "Inputs Used"])
        .size()
        .reset_index(name="Times Used")
        .sort_values("Times Used", ascending=False)
    )
    st.dataframe(inputs_used, use_container_width=True)

    # ----------------------------
    # 11. Owner Performance Summary
    # ----------------------------

    st.subheader("🧑‍💼 Owner Performance Overview")
    owner_summary = filtered.groupby("Owner").agg({
        "ID": "count",
        "Effectiveness": lambda x: (x == "✅ Effective").mean() * 100,
        "Time to Outcome (days)": "mean"
    }).reset_index().rename(columns={
        "ID": "Decisions Made",
        "Effectiveness": "% Effective",
        "Time to Outcome (days)": "Avg Time to Outcome"
    })
    st.dataframe(owner_summary.round(1), use_container_width=True)

    # ----------------------------
    # 12. Recommendations
    # ----------------------------

    st.markdown("### ✅ Recommendations")
    st.markdown("""
    - Track STAR decisions and replicate winning patterns  
    - Use “Avg Time to Outcome” to coach team efficiency  
    - Build a library of “Repeatable Wins” from top contributors  
    - Review inputs used in effective decisions — reinforce with training  
    """)


if __name__ == "__main__":
    main()
