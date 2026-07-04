from datetime import date

CARDS = [

    "💛 It's okay to have bad days. Healing isn't linear.",

    "🌱 Progress is still progress, even if it's small.",

    "☀️ You don't have to control every thought. Just notice them.",

    "💙 Asking for help is a sign of strength, not weakness.",

    "🌸 Rest is productive too.",

    "🧠 Your thoughts are not always facts.",

    "🌈 One difficult day doesn't define your life.",

    "💚 Be as kind to yourself as you are to others.",

    "✨ Celebrate small wins today.",

    "🌻 You survived 100% of your hardest days.",

    "🌊 Feelings come and go like waves. Let them pass.",

    "🤍 It's okay to pause before reacting.",

    "🌙 Sleep is part of self-care.",

    "💪 Growth often feels uncomfortable.",

    "🌼 Breathe. You don't have to solve everything today."

]

def get_daily_card():

    day = date.today().toordinal()

    return CARDS[day % len(CARDS)]