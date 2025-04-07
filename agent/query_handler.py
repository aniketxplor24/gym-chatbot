import pandas as pd
from datetime import date, timedelta
from agent.intent_classifier import detect_intent

# Load datasets
members_df = pd.read_csv("data/members.csv", parse_dates=["join_date"])
cancellations_df = pd.read_csv("data/cancellations.csv", parse_dates=["cancel_date"])
payments_df = pd.read_csv("data/payments.csv", parse_dates=["date"])

# Ensure date columns are parsed
members_df["join_date"] = pd.to_datetime(members_df["join_date"])
cancellations_df["cancel_date"] = pd.to_datetime(cancellations_df["cancel_date"])
payments_df["date"] = pd.to_datetime(payments_df["date"])

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

        case "cancelled_last_month":
            target = today - pd.DateOffset(months=1)
            filtered = cancellations_df[
                (cancellations_df["cancel_date"].dt.month == target.month) &
                (cancellations_df["cancel_date"].dt.year == target.year)
            ]
            names = get_names(filtered)
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
            return f"{len(filtered)} member(s) cancelled this month: {names}"

        case "revenue_yesterday":
            yesterday = today - timedelta(days=1)
            total = payments_df[payments_df["date"].dt.date == yesterday.date()]["amount"].sum()
            return f"Revenue yesterday was ₹{total:.2f}."

        case _:
            return (
                "❓ Sorry, I didn't understand that.\n"
                "Try asking things like:\n"
                "- Who joined last month?\n"
                "- Revenue yesterday?\n"
                "- How many cancelled this week?"
            )
