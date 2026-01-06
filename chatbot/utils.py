import re

INTENT_RESPONSES = {
    "stress": "It sounds like you're feeling stressed. Try taking a few deep breaths and focusing on one task at a time.",
    "anxiety": "Anxiety can be overwhelming. Slow breathing and grounding exercises may help you feel calmer.",
    "sad": "I'm sorry you're feeling this way. Talking to someone you trust can sometimes help.",
    "sleep": "Maintaining a regular sleep routine and avoiding screens before bed can improve sleep quality.",
    "exam": "Exam pressure is common. Break your preparation into small, manageable steps."
}

EMERGENCY_KEYWORDS = [
    "suicide", "kill myself", "end my life", "hurt myself", "self harm"
]

def get_chatbot_response(message):
    message = message.lower()

    for keyword in EMERGENCY_KEYWORDS:
        if keyword in message:
            return {
                "response": "If you are in immediate distress, please contact a mental health helpline immediately.",
                "emergency": True
            }

    for intent, response in INTENT_RESPONSES.items():
        if re.search(intent, message):
            return {
                "response": response,
                "emergency": False
            }

    return {
        "response": "Thank you for sharing. Can you tell me a little more about how you're feeling?",
        "emergency": False
    }
