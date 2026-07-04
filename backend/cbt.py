CBT_EXERCISES = {

    "anxiety": {
        "title": "🌬 5-4-3-2-1 Grounding",

        "exercise": """
5 things you can see

4 things you can touch

3 things you can hear

2 things you can smell

1 thing you can taste
"""
    },

    "stress": {
        "title": "📋 Circle of Control",

        "exercise": """
Write two lists.

✔ Things I can control

❌ Things I cannot control
"""
    },

    "sad": {
        "title": "☀ Behavioural Activation",

        "exercise": """
Choose ONE:

• Take a 10 minute walk

• Listen to your favourite song

• Drink a glass of water

• Message someone you trust
"""
    },

    "anger": {
        "title": "🫁 STOP Technique",

        "exercise": """
S — Stop

T — Take a breath

O — Observe

P — Proceed mindfully
"""
    },

    "default": {
        "title": "💚 Self Check-in",

        "exercise": """
Take one slow breath.

Ask yourself:

"What do I need right now?"
"""
    }

}

def get_cbt(message):

    message = message.lower()

    if any(word in message for word in [
        "anxious",
        "anxiety",
        "panic",
        "worried",
        "fear"
    ]):
        return CBT_EXERCISES["anxiety"]

    if any(word in message for word in [
        "stress",
        "overwhelmed",
        "pressure",
        "exam"
    ]):
        return CBT_EXERCISES["stress"]

    if any(word in message for word in [
        "sad",
        "depressed",
        "cry",
        "lonely"
    ]):
        return CBT_EXERCISES["sad"]

    if any(word in message for word in [
        "angry",
        "mad",
        "furious"
    ]):
        return CBT_EXERCISES["anger"]

    return None