# agent/intent_classifier.py
import spacy

nlp = spacy.load("en_core_web_sm")
INTENTS = {
    "joined_last_month": [
        "how many joined last month",
        "who joined last month",
        "members joined last month"
    ],
    "joined_this_month": [
        "who joined this month",
        "how many joined this month",
        "members joined this month",
        "joining stats this month"
    ],
    "cancelled_last_month": [
        "how many cancelled last month",
        "members cancelled last month",
        "who cancelled last month"
    ],
    "cancelled_this_month": [
        "how many cancelled this month",
        "who cancelled this month",
        "cancellations this month",
        "members cancelled this month"
    ],
    "joined_today": [
        "who joined today",
        "how many joined today",
        "joined on today","members joined today", "members who joined today ?"
    ],
    "cancelled_today": [
        "who cancelled today",
        "how many cancelled today",
        "cancellations today"
    ],
    "cancelled_this_week": [
        "cancellations this week",
        "who cancelled this week",
        "how many cancelled this week"
    ],
    "revenue_yesterday": [
        "what is the revenue yesterday",
        "yesterday's revenue",
        "Revenue yesterday",
        "how much did we earn yesterday"
    ],
      "revenue_last_month": ["what is the revenue last month", "revenue last month", "how much revenue was generated last month", "total revenue for last month"],
       "busiest_hour": [
        "what was the busiest hour last week",
        "when was the gym most crowded last week",
        "which hour had most people",
        "peak hour last week",
        "most crowded time last week"
    ],

    "full_attendance": [
        "can you show me the full attendance record for this week",
        "show me the attendance report",
        "give me a list of all attendance records",
        "full attendance report"
    ],

    "users_today": [
        "how many users attended today",
        "who all attended today",
        "users checked in today"
    ],

    "late_checkins": [
        "which users checked in late last day",
        "who came late yesterday",
        "who checked in after 10 am yesterday"
    ],

    "user_attendance": [
        "can you show me the check-in and check-out times for",
        "what is the attendance history for",
        "show attendance of"
    ],

    "users_on_date": [
        "how many users were present on",
        "how many users attended on"
    ],
    "full_attendance": [
    "can you show me the full attendance record",
    "show me the full attendance record",
    "full attendance report",
    "show attendance report",
    "display all attendance",
    "give me all check-in records",
    "attendance history",
    "i want to see all attendance records",
    "list attendance of all members",
    "complete attendance data"
]

}


def detect_intent(question: str):
    doc = nlp(question.lower())
    best_intent = None
    best_score = 0

    for intent, phrases in INTENTS.items():
        for phrase in phrases:
            score = nlp(phrase).similarity(doc)
            if score > best_score:
                best_score = score
                best_intent = intent
    
    print(f"[DEBUG] Best Intent: {best_intent}, Score: {best_score}")

    return best_intent if best_score > 0.80 else None


