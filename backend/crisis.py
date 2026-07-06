from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from backend.config import GROQ_API_KEY


SYSTEM_PROMPT = """
You are an expert mental health crisis detector.

Your ONLY task is to determine whether the user's message
indicates an immediate risk of suicide or self-harm.

Reply with ONLY one word:

YES
or
NO

Reply YES if the user expresses:
- wanting to die
- suicide
- self-harm
- ending their life
- immediate danger
- a clear plan or intent to kill themselves

Reply NO for:
- stress
- anxiety
- sadness
- loneliness
- depression without suicidal intent
- relationship problems
- academic pressure

Do not explain your answer.
Do not output anything except YES or NO.
"""


llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0,
    groq_api_key=GROQ_API_KEY
)


def detect_crisis(user_message: str) -> bool:

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_message),
    ]

    response = llm.invoke(messages).content.strip().upper()

    return response.startswith("YES")
