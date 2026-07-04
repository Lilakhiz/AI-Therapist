from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from backend.config import GROQ_API_KEY
from backend.database import get_recent_messages


SYSTEM_PROMPT = """
You are SafeSpace, a compassionate AI therapist.

Your job is to:
- Listen carefully.
- Respond with empathy.
- Help the user explore their feelings.
- Encourage healthy coping strategies.
- Never judge the user.
- Never diagnose mental illnesses.
- Keep responses concise (3-6 sentences unless more detail is needed).
"""


llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.3,
    groq_api_key=GROQ_API_KEY
)


def therapist_chat(user_id, user_message):

    messages = [SystemMessage(content=SYSTEM_PROMPT)]

    # Previous conversation
    messages.extend(
    get_recent_messages(user_id)
)

    # Current user message
    messages.append(
        HumanMessage(content=user_message)
    )

    # AI response
    response = llm.invoke(messages).content


    return response