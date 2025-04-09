import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from datetime import timedelta


def plot_busiest_hours_chart(attendance_df):
    slot_counts = {}
    for _, row in attendance_df.iterrows():
        start = row["in_time"]
        end = row["out_time"]
        while start < end:
            slot = start.strftime('%H:00') + '–' + (start + timedelta(hours=1)).strftime('%H:00')
            slot_counts[slot] = slot_counts.get(slot, 0) + 1
            start += timedelta(hours=1)

    slots = list(slot_counts.keys())
    counts = list(slot_counts.values())

    st.subheader("📈 Hourly Gym Traffic (Last Week)")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(slots, counts)
    plt.xticks(rotation=45)
    plt.ylabel("Number of Users")
    plt.xlabel("Time Slots")
    st.pyplot(fig)


def plot_today_attendance_shift(attendance_df):
    today_df = attendance_df[attendance_df["date"].dt.date == pd.to_datetime("today").date()]
    shift_counts = {"Morning (before 12PM)": 0, "Evening (after 12PM)": 0}

    for time in today_df["in_time"]:
        shift = "Morning (before 12PM)" if time.hour < 12 else "Evening (after 12PM)"
        shift_counts[shift] += 1

    st.subheader("☀️ Morning vs Evening Attendance (Today)")
    fig, ax = plt.subplots()
    ax.pie(shift_counts.values(), labels=shift_counts.keys(), autopct='%1.1f%%')
    st.pyplot(fig)


def plot_weekly_attendance_trend(attendance_df):
    daily_count = attendance_df.groupby(attendance_df["date"].dt.date)["name"].nunique()

    st.subheader("📆 Daily Attendance Trend (Last Week)")
    fig, ax = plt.subplots()
    ax.plot(daily_count.index, daily_count.values, marker='o')
    plt.xticks(rotation=45)
    plt.ylabel("Unique Users")
    plt.xlabel("Date")
    st.pyplot(fig)
