import pandas as pd
from datetime import date, timedelta
from agent.intent_classifier import classify_intent

# Load data once
members_df = pd.read_csv("data/members.csv", parse_dates=["join_date"])
cancellations_df = pd.read_csv("data/cancellations.csv", parse_dates=["cancel_date"])
payments_df = pd.read_csv("data/payments.csv", parse_dates=["date"])

def handle_question(question):
    intent = classify_intent(question)
    today = pd.to_datetime(date.today())

    if intent == "joined_today":
        count = members_df[members_df["join_date"] == today].shape[0]
        return f"🏋️ {count} member(s) joined today."

    elif intent == "cancelled_today":
        count = cancellations_df[cancellations_df["cancel_date"] == today].shape[0]
        return f"❌ {count} member(s) cancelled today."

    elif intent == "joined_last_month":
        last_month = today - pd.DateOffset(months=1)
        filtered = members_df[
            (members_df["join_date"].dt.month == last_month.month) &
            (members_df["join_date"].dt.year == last_month.year)
        ]
        return f"📈 {filtered.shape[0]} member(s) joined last month."

    elif intent == "cancelled_last_month":
        last_month = today - pd.DateOffset(months=1)
        filtered = cancellations_df[
            (cancellations_df["cancel_date"].dt.month == last_month.month) &
            (cancellations_df["cancel_date"].dt.year == last_month.year)
        ]
        return f"📉 {filtered.shape[0]} member(s) cancelled last month."

    elif intent == "revenue_yesterday":
        yesterday = today - timedelta(days=1)
        total = payments_df[payments_df["date"] == yesterday]["amount"].sum()
        return f"💰 Revenue collected yesterday: ₹{total}"

    elif intent == "who_joined_last_month":
        last_month = today - pd.DateOffset(months=1)
        filtered = members_df[
            (members_df["join_date"].dt.month == last_month.month) &
            (members_df["join_date"].dt.year == last_month.year)
        ]
        if filtered.empty:
            return "😕 No one joined last month."
        return "👤 Members joined last month:\n" + "\n".join(filtered["name"].tolist())

    else:
        return "❓ Sorry, I didn't understand. Try asking:\n- Who joined last month?\n- Revenue yesterday?\n- How many cancelled today?"
