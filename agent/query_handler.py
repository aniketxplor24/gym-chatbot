import pandas as pd
from datetime import date, timedelta
from agent.intent_classifier import detect_intent
import streamlit as st
from agent.visuals import (
    plot_busiest_hours_chart,
    plot_today_attendance_shift,
    plot_weekly_attendance_trend
)


# Load datasets
members_df = pd.read_csv("data/members.csv", parse_dates=["join_date"])
cancellations_df = pd.read_csv("data/cancellations.csv", parse_dates=["cancel_date"])
payments_df = pd.read_csv("data/payments.csv", parse_dates=["date"])
attendance_df = pd.read_csv("data/attendance_last_week.csv", parse_dates=["in_time", "out_time"])



# Ensure date columns are parsed
members_df["join_date"] = pd.to_datetime(members_df["join_date"])
cancellations_df["cancel_date"] = pd.to_datetime(cancellations_df["cancel_date"])
payments_df["date"] = pd.to_datetime(payments_df["date"])
attendance_df["date"] = pd.to_datetime(attendance_df["date"])

today = pd.to_datetime(date.today())

def get_names(df, column="name"):
    names = df[column].tolist()
    return ", ".join(names) if names else "None"

def query_gym_data(user_question: str) -> str:
    intent = detect_intent(user_question)
    print(f"Detected intent: {intent}")

    match intent:
        case "joined_this_month":
            filtered = members_df[
            (members_df["join_date"].dt.month == today.month) & 
            (members_df["join_date"].dt.year == today.year)
            ]
            names = ", ".join(filtered["name"]) if not filtered.empty else "None"
            return f"{len(filtered)} member(s) joined this month: {names}"

        case "joined_last_month":
            target = today - pd.DateOffset(months=1)
            filtered = members_df[
                (members_df["join_date"].dt.month == target.month) & 
                (members_df["join_date"].dt.year == target.year)
            ]
            names = ", ".join(filtered["name"]) if not filtered.empty else "None"
            print(f"Filtered data: {filtered}")  # Log the filtered records
            return f"{len(filtered)} member(s) joined last month : {names} "    

        case "cancelled_last_month":
            target = today - pd.DateOffset(months=1)
            filtered = cancellations_df[
                (cancellations_df["cancel_date"].dt.month == target.month) &
                (cancellations_df["cancel_date"].dt.year == target.year)
            ]
            names = get_names(filtered)
             # Added: Show the cancellation data as a table
            st.write(f"Members who cancelled last month:")
            st.dataframe(filtered)  # Displaying table of cancellations

            return f"{len(filtered)} member(s) cancelled last month: {names}"

        case "joined_today":
            filtered = members_df[members_df["join_date"].dt.date == today.date()]
            names = get_names(filtered)
            return f"{len(filtered)} member(s) joined today: {names}"

        case "cancelled_today":
            filtered = cancellations_df[cancellations_df["cancel_date"].dt.date == today.date()]
            names = get_names(filtered)
        
            return f"{len(filtered)} member(s) cancelled today: {names}"

        case "cancelled_this_week":
            current_week = today.isocalendar().week
            filtered = cancellations_df[cancellations_df["cancel_date"].dt.isocalendar().week == current_week]
            names = get_names(filtered)
            return f"{len(filtered)} member(s) cancelled this week: {names}"

        case "cancelled_this_month":
            filtered = cancellations_df[cancellations_df["cancel_date"].dt.month == today.month]
            names = get_names(filtered)
            st.write(f"Members who cancelled this month:")
            st.dataframe(filtered)  # Displaying table of cancellations
            return f"{len(filtered)} member(s) cancelled this month: {names}"

        case "revenue_yesterday":
            yesterday = today - timedelta(days=1)
            total = payments_df[payments_df["date"].dt.date == yesterday.date()]["amount"].sum()
            return f"Revenue yesterday was ₹{total:.2f}."

        case "revenue_last_month":
            target = today - pd.DateOffset(months=1)
            revenue = payments_df[
                (payments_df["date"].dt.month == target.month) & 
                (payments_df["date"].dt.year == target.year)
            ]["amount"].sum()
            return f"The total revenue for last month was ₹{revenue:.2f}."

        case "busiest_hour":
            from datetime import timedelta

            slot_counts = {}
            for _, row in attendance_df.iterrows():
                start = row["in_time"]
                end = row["out_time"]
                while start < end:
                    slot = start.strftime('%H:00') + '–' + (start + timedelta(hours=1)).strftime('%H:00')
                    slot_counts[slot] = slot_counts.get(slot, 0) + 1
                    start += timedelta(hours=1)
            if slot_counts:
                busiest = max(slot_counts.items(), key=lambda x: x[1])
                plot_busiest_hours_chart(attendance_df) 
                return f"The busiest hour last week was **{busiest[0]}** with {busiest[1]} total check-ins."
            else:
                return "No attendance data found for last week."

        case "full_attendance":
            st.write("📋 Full attendance record for last week:")
            st.dataframe(attendance_df)
            plot_today_attendance_shift(attendance_df)
            return f"Showing all {len(attendance_df)} attendance records."

        case "users_today":
            today_attendance = attendance_df[attendance_df["date"].dt.date == today.date()]
            count = today_attendance["name"].nunique()
            names = ", ".join(today_attendance["name"].unique())
            return f"{count} user(s) attended today: {names}"

        case "user_attendance":
            import re
            match = re.search(r"(?:for|of)\s+([a-zA-Z\s]+)", user_question.lower())
            if match:
                user = match.group(1).strip().title()
                user_data = attendance_df[attendance_df["name"] == user]
                if not user_data.empty:
                    st.write(f"🕒 Attendance history for {user}:")
                    st.dataframe(user_data)
                    return f"{len(user_data)} record(s) found for {user}."
                return f"No attendance records found for {user}."
            return "Please mention the user name like: check-in time for John Smith."

        case "late_checkins":
            yesterday = today - timedelta(days=1)
            late_df = attendance_df[
                (attendance_df["date"].dt.date == yesterday.date()) &
                (attendance_df["in_time"].dt.hour >= 10)
            ]
            if not late_df.empty:
                st.write("⏰ Users who checked in late yesterday (after 10 AM):")
                st.dataframe(late_df)
                return f"{len(late_df)} user(s) checked in late yesterday."
            return "No one checked in late yesterday."

        case "users_on_date":
            import re
            match = re.search(r"on (\d{4}-\d{2}-\d{2})", user_question)
            if match:
                query_date = pd.to_datetime(match.group(1)).date()
                day_df = attendance_df[attendance_df["date"].dt.date == query_date]
                count = day_df["name"].nunique()
                names = ", ".join(day_df["name"].unique())
                return f"{count} user(s) attended on {query_date}: {names}"
            return "Please provide a valid date like: How many users attended on 2025-04-08?"


        case _:
            return (
                "❓ Sorry, I didn't understand that.\n"
                "Try asking things like:\n"
                "- Who joined last month?\n"
                "- Revenue yesterday?\n"
                "- How many cancelled this week?"
            )
