from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from backend.config import GROQ_API_KEY


SYSTEM_PROMPT = """
You extract city names from user messages.

Rules:
- Reply ONLY with the city name.
- If there is no city mentioned, reply ONLY:
NONE

Examples:

User:
Recommend a therapist in Bangalore.
Reply:
Bangalore

User:
I'm from Mumbai.
Reply:
Mumbai

User:
Can you help me?
Reply:
NONE

User:
I live in Whitefield, Bangalore.
Reply:
Bangalore

User:
Recommend a psychologist near Koramangala.
Reply:
Bangalore

Do not explain your answer.
"""


llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0,
    groq_api_key=GROQ_API_KEY,
)


def extract_city(user_message: str):

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_message),
    ]

    city = llm.invoke(messages).content.strip()

    if city.upper() == "NONE":
        return None

    return city

