from fastapi import FastAPI
from pydantic import BaseModel

from backend.therapist import therapist_chat
from backend.crisis import detect_crisis
from backend.location import extract_city
from backend.therapist_locator import find_therapists
from backend.emergency import call_emergency
from backend.cbt import get_cbt
from backend.emergency import call_emergency



app = FastAPI()

class Query(BaseModel):
    user_id: int
    message: str


@app.post("/ask")
async def ask(query: Query):

    user_message = query.message

    # Generate therapist response
    response = therapist_chat(
                                query.user_id,
                                query.message
                            )

    # Detect crisis
    crisis = detect_crisis(user_message)

    # Therapist recommendations
    therapists = []

    #cbt recommendations
    cbt = get_cbt(query.message)

    if "therapist" in user_message.lower() or \
       "psychologist" in user_message.lower() or \
       "counsellor" in user_message.lower() or \
       "counselor" in user_message.lower():

        city = extract_city(user_message)

        if city:
            therapists = find_therapists(city)
        
    # Emergency call
    if crisis:
        call_emergency(query.user_id)

    return {
        "response": response,
        "crisis": crisis,
        "therapists": therapists,
        "cbt" : cbt
    }

