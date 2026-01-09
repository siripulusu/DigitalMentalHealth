import re
import random

INTENTS = {
    "stress": [
        "It sounds like you’ve been under a lot of pressure lately. Academic strain is real.",
        "Stress can quietly pile up until it feels overwhelming. Have you had a chance to breathe today?",
        "That kind of stress can be exhausting to carry alone. You're doing well by reaching out.",
        "You’re not weak for feeling stressed — it’s a natural response to high demands.",
        "Stress often comes from trying to manage too much at once. Let's try to break things down.",
        "Your body might be asking for a pause. Even 5 minutes of quiet can help.",
        "Stress doesn’t mean failure. It just means you care about what you're doing.",
        "Many students experience this silently. I'm glad you're talking about it.",
        "Let’s take this step by step. What is the one thing weighing on you most right now?"
    ],
    "anxiety": [
        "Anxiety can make your thoughts race unexpectedly. It's a very loud feeling.",
        "That uneasy feeling in your chest... it can be hard to sit with. I hear you.",
        "Anxiety often focuses on what *might* happen. Let's try to find one thing that is true *right now*.",
        "Your mind is trying to protect you, but it's okay to tell it that you are safe in this moment.",
        "That tight feeling will pass. It always does, even if it doesn't feel like it now.",
        "Breathing slowly (in for 4, hold for 4, out for 4) can help signal your body to calm down.",
        "Anxiety doesn’t define you. It's just a weather pattern passing through your mind.",
        "You’re safe here. There’s no rush to 'fix' how you feel immediately."
    ],
    "sad": [
        "I’m really sorry you’re feeling this way. Sadness can make the world feel very heavy.",
        "It’s okay to acknowledge feeling low. You don't have to put on a brave face here.",
        "That emotional weight can be draining. Have you been able to eat or rest a bit today?",
        "Your feelings matter, and it's okay to not be okay right now.",
        "Sadness isn't a sign of weakness; it's a sign of being human.",
        "Sometimes just sitting with the feeling is the first step toward moving through it.",
        "I’m listening. If you want to describe what the sadness feels like, I'm here."
    ],
    "exam": [
        "Exam season is incredibly tough. Your worth is so much more than a grade on a paper.",
        "Many students struggle silently during exams. It's a high-pressure environment.",
        "Perfection isn’t required. Doing your best with the energy you have today is enough.",
        "One step at a time. Could we look at just one small task instead of the whole syllabus?",
        "Remember to hydrate and take 'brain breaks'. Your mind needs rest to retain information.",
        "This phase is intense, but it is temporary. You will get through this."
    ],
    "sleep": [
        "Sleep struggles often reflect what's happening in our minds during the day.",
        "Lack of rest can make every emotion feel twice as intense. It's a difficult cycle.",
        "Try to give yourself a 'digital sunset' — no screens 30 minutes before bed.",
        "A calm routine might help, even if it's just a warm drink or a few deep breaths.",
        "Don't punish yourself for not being able to sleep. Just resting your eyes is still helpful.",
        "Sleep improves gradually. Let's look at some sleep hygiene tips in our Resources section."
    ],
}

EMERGENCY_KEYWORDS = ["suicide", "kill myself", "end my life", "hurt myself", "self harm", "die"]

FOLLOW_UPS = [
    "Would you like to share a bit more about that?",
    "How long has this been on your mind?",
    "What usually helps you feel a little grounded when things get tough?",
    "I'm here with you. Take all the time you need to type.",
    "What feels like the hardest part of today?",
    "Do you have someone offline you feel safe talking to?",
    "Sometimes writing it out like this can help clear the fog. What else is on your mind?"
]

def detect_intent(message: str):
    for intent in INTENTS.keys():
        if re.search(r'\b' + intent + r'\b', message.lower()):
            return intent
    return None

def get_chatbot_response(message, msg_count=0, is_authenticated=False):
    msg_lower = message.lower()

    # 1. Emergency Check
    for word in EMERGENCY_KEYWORDS:
        if word in msg_lower:
            return {
                "response": "I’m very concerned about your safety. Please reach out to someone who can help right now. You are valuable.\n\nIndia Helpline: 9152987821 (24/7)",
                "emergency": True
            }

    # 2. Strategic Suggestion (Every 4th/5th message)
    if msg_count > 0 and msg_count % 4 == 0:
        if not is_authenticated:
            return {
                "response": "I've really valued our conversation so far. If you log in, I can help track your mood trends over time and give more personalized advice. Would you consider creating an account?",
                "suggestion": "login"
            }
        else:
            return {
                "response": "We've been talking for a bit now. You might find some of the guided breathing or meditation tools in the 'Resources' section helpful to pair with our chat. Shall we take a look?",
                "suggestion": "resources"
            }

    # 3. Intent Based
    intent = detect_intent(msg_lower)
    if intent:
        return {"response": random.choice(INTENTS[intent])}

    # 4. Default
    return {"response": random.choice(FOLLOW_UPS)}