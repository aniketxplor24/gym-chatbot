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
        "cancellations this month",
        "members cancelled this month"
    ],
    "joined_today": [
        "who joined today",
        "how many joined today",
        "joined on today"
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
        "how much did we earn yesterday"
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

    return best_intent if best_score > 0.85 else None


